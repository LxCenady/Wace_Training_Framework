"""WTF account. One job: sign in to a WTF account server and keep this computer's session.

The account server (docs/account_api.md) holds the model API key and each user's daily quota, so students sign in
instead of configuring an API key. Sign-in methods are a registry (account.methods) so a school SSO can be added
later; built in: e-mail code and Google. Google OAuth runs on the server (it keeps the client secret, which an
open-source app cannot): the app opens the browser at the server's start URL with a loopback redirect, receives a
one-time code on 127.0.0.1 and exchanges it for the session token — the token itself never passes the browser.

Services: account.methods, account.info() -> {email, server, signed_in}, account.request_code(email),
account.verify_code(email, code), account.google(timeout), account.me() -> server's /v1/me, account.logout().
Event: account.changed(info).
"""
import json, secrets, threading, urllib.error, urllib.parse, urllib.request, webbrowser
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


class AccountError(RuntimeError):
    """Something the user can act on (no service yet, wrong code, signed out)."""


def setup(k):
    global AGENT
    ed = k.get("edition", {})
    here = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "version.txt")
    ver = open(here, encoding="utf-8").read().strip() if os.path.isfile(here) else "0"
    AGENT = f"{(ed.get('short') or 'WTF').replace(' ', '-')}/{ver} (+https://wtf-academy.org)"
    cfg = k.get("config")
    acct = cfg.setdefault("account", {"server": "", "email": "", "token": ""})

    def server():
        url = (acct.get("server") or "").rstrip("/")
        if not url:
            raise AccountError("账号服务尚未开通：在「设置 → 账号」里填写学校提供的服务器地址")
        return url

    def call(method, path, body=None, auth=True, timeout=30):
        headers = {"content-type": "application/json", "user-agent": AGENT}  # named: Cloudflare turns away anonymous scripts
        if auth:
            if not acct.get("token"):
                raise AccountError("尚未登录 WTF 账号")
            headers["authorization"] = f"Bearer {acct['token']}"
        req = urllib.request.Request(server() + path, method=method, headers=headers,
                                     data=json.dumps(body).encode() if body is not None else None)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read() or b"{}")
        except urllib.error.HTTPError as e:
            try:
                msg = json.loads(e.read()).get("error", "")
            except ValueError:
                msg = ""
            if e.code == 401 and auth:
                signed_out()
                raise AccountError("登录已过期，请重新登录 WTF 账号") from None
            raise AccountError(msg or f"账号服务返回 HTTP {e.code}") from None
        except urllib.error.URLError as e:
            raise AccountError(f"连不上账号服务：{e.reason}") from None

    def info():
        return {"server": acct.get("server", ""), "email": acct.get("email", ""), "signed_in": bool(acct.get("token"))}

    def signed_in(token, email):
        acct.update(token=token, email=email)
        k.get("config.save", lambda: None)()
        k.emit("account.changed", info())

    def signed_out():
        acct.update(token="")
        k.get("config.save", lambda: None)()
        k.emit("account.changed", info())

    def request_code(email):
        """E-mail sign-in, step 1: the server mails a short code (and decides whether this address may join)."""
        call("POST", "/v1/auth/email/start", {"email": email.strip()}, auth=False)

    def verify_code(email, code):
        """E-mail sign-in, step 2: the code for a session token."""
        r = call("POST", "/v1/auth/email/verify", {"email": email.strip(), "code": code.strip()}, auth=False)
        signed_in(r["token"], r.get("email", email.strip()))
        return info()

    def google(timeout=180, open_browser=webbrowser.open):
        """Google sign-in through the server, with a loopback redirect to this computer. Blocks until done."""
        state, got = secrets.token_urlsafe(16), {}

        class Callback(BaseHTTPRequestHandler):
            def do_GET(self):
                q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
                ok = q.get("state", [""])[0] == state and "code" in q
                if ok:
                    got["code"] = q["code"][0]
                self.send_response(200 if ok else 400)
                self.send_header("content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(("<p>已登录 WTF，可以关闭这个页面回到程序。</p>" if ok
                                  else "<p>登录未完成，请回到 WTF 重试。</p>").encode())

            def log_message(self, *a):
                pass

        httpd = HTTPServer(("127.0.0.1", 0), Callback)  # loopback only, any free port
        httpd.timeout = timeout
        redirect = f"http://127.0.0.1:{httpd.server_port}/callback"
        url = server() + "/v1/auth/google/start?" + urllib.parse.urlencode({"redirect_uri": redirect, "state": state})
        threading.Thread(target=open_browser, args=(url,), daemon=True).start()
        try:
            httpd.handle_request()  # one request: the redirect back from the server
        finally:
            httpd.server_close()
        if "code" not in got:
            raise AccountError("Google 登录未完成（超时或被取消）")
        r = call("POST", "/v1/auth/exchange", {"code": got["code"], "state": state, "redirect_uri": redirect}, auth=False)
        signed_in(r["token"], r.get("email", ""))
        return info()

    def me():
        """{email, plan, quota: {used, limit, unit, resets_at}} from the server."""
        return call("GET", "/v1/me")

    def checkout(plan):
        """A payment page for `plan` (student / teacher) -> its URL; while online subscription is not open the server
        answers why and whom to write to (raised as AccountError with that message)."""
        return call("POST", "/v1/billing/checkout", {"plan": plan})["url"]

    def logout():
        try:
            call("POST", "/v1/auth/logout", {})
        except AccountError:
            pass  # signing out locally is enough when the server cannot be reached
        signed_out()

    k.provide("account.methods", {"email": "邮箱验证码", "google": "Google 账号"})
    k.provide("account.info", info)
    k.provide("account.request_code", request_code)
    k.provide("account.verify_code", verify_code)
    k.provide("account.google", google)
    k.provide("account.me", me)
    k.provide("account.checkout", checkout)
    k.provide("account.logout", logout)
    k.provide("account.call", call)
    k.provide("account.Error", AccountError)
