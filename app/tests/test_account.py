"""WTF account sign-in and the "wtf" provider against a fake account server (docs/account_api.md). No network beyond
127.0.0.1; settings go to a temporary file (tests.safe_runtime.isolate)."""
import json, os, sys, threading, unittest, urllib.parse, urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from tests.safe_runtime import isolate  # noqa: E402
isolate()
from kernel import Kernel  # noqa: E402

SEEN = {}


class Fake(BaseHTTPRequestHandler):
    state = {"codes": {}, "tokens": {}, "used": 0, "limit": 2, "pending": {}}

    def reply(self, status, body):
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def user(self):
        auth = self.headers.get("authorization", "")
        return self.state["tokens"].get(auth.removeprefix("Bearer "))

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        if u.path == "/v1/auth/google/start":
            self.state["pending"]["g-code"] = (q["state"][0], q["redirect_uri"][0])
            self.send_response(302)
            self.send_header("location", q["redirect_uri"][0] + "?" + urllib.parse.urlencode(
                {"code": "g-code", "state": q["state"][0]}))
            self.end_headers()
        elif u.path == "/v1/me":
            if not self.user():
                return self.reply(401, {"error": "signed out"})
            self.reply(200, {"email": self.user(), "plan": "pilot",
                             "quota": {"used": self.state["used"], "limit": self.state["limit"], "unit": "题"}})
        else:
            self.reply(404, {"error": "no such path"})

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("content-length", 0))) or b"{}")
        p = self.path
        if p == "/v1/auth/email/start":
            self.state["codes"][body["email"]] = "123456"
            self.reply(200, {})
        elif p == "/v1/auth/email/verify":
            if self.state["codes"].get(body["email"]) != body["code"]:
                return self.reply(400, {"error": "验证码不对或已过期"})
            self.state["tokens"]["tok-mail"] = body["email"]
            self.reply(200, {"token": "tok-mail", "email": body["email"]})
        elif p == "/v1/auth/exchange":
            if self.state["pending"].get(body["code"]) != (body["state"], body["redirect_uri"]):
                return self.reply(400, {"error": "bad exchange"})
            self.state["tokens"]["tok-google"] = "g@school.edu.sg"
            self.reply(200, {"token": "tok-google", "email": "g@school.edu.sg"})
        elif p == "/v1/auth/logout":
            self.state["tokens"].pop(self.headers.get("authorization", "").removeprefix("Bearer "), None)
            self.reply(200, {})
        elif p == "/v1/chat/completions":
            SEEN["model"], SEEN["auth"] = body.get("model"), self.headers.get("authorization")
            if not self.user():
                return self.reply(401, {"error": "signed out"})
            if self.state["used"] >= self.state["limit"]:
                return self.reply(429, {"error": "今日 AI 额度已用完"})
            self.state["used"] += 1
            self.reply(200, {"choices": [{"message": {"content": "ok from wtf"}}],
                             "usage": {"prompt_tokens": 10, "completion_tokens": 3}})
        else:
            self.reply(404, {"error": "no such path"})

    def log_message(self, *a):
        pass


class Account(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = HTTPServer(("127.0.0.1", 0), Fake)
        threading.Thread(target=cls.httpd.serve_forever, daemon=True).start()
        cls.url = f"http://127.0.0.1:{cls.httpd.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()

    def setUp(self):
        self.k = Kernel(HERE)
        self.k.load(["config", "llm", "llm_openai", "account", "llm_wtf"])
        self.cfg = self.k.get("config")
        self.k.provide("config.save", lambda: None)
        self.usage = []
        self.k.on("llm.usage", lambda model, u: self.usage.append(u))

    def test_flow(self):
        k, Error, ProviderError = self.k, self.k.get("account.Error"), self.k.get("llm.ProviderError")
        with self.assertRaisesRegex(Error, "尚未开通"):
            k.get("account.request_code")("a@school.edu.sg")
        self.cfg["account"]["server"] = self.url
        k.get("account.request_code")("a@school.edu.sg")
        with self.assertRaisesRegex(Error, "验证码"):
            k.get("account.verify_code")("a@school.edu.sg", "000000")
        self.assertTrue(k.get("account.verify_code")("a@school.edu.sg", "123456")["signed_in"])
        self.assertEqual(k.get("account.me")()["quota"]["limit"], 2)

        self.cfg["provider"] = "wtf"
        self.assertEqual(k.get("llm.chat")("system", "user"), "ok from wtf")
        self.assertEqual((SEEN["model"], SEEN["auth"]), ("default", "Bearer tok-mail"))
        self.assertEqual(self.usage[-1]["completion_tokens"], 3)
        k.get("llm.chat")("system", "user")
        with self.assertRaisesRegex(ProviderError, "额度已用完"):
            k.get("llm.chat")("system", "user")

        def browser(url):  # what a browser does: follow the server's redirect back to the loopback port
            urllib.request.urlopen(url, timeout=10).read()
        info = k.get("account.google")(timeout=10, open_browser=browser)
        self.assertEqual((info["email"], self.cfg["account"]["token"]), ("g@school.edu.sg", "tok-google"))

        k.get("account.logout")()
        self.assertFalse(k.get("account.info")()["signed_in"])
        with self.assertRaisesRegex(ProviderError, "尚未登录"):
            k.get("llm.chat")("system", "user")


if __name__ == "__main__":
    unittest.main()
