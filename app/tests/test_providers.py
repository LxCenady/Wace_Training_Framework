"""Provider adapters against a local fake server: checks request shape (path, auth header, body) and reply parsing.
Usage: python tests/test_providers.py"""
import json, os, sys, threading
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import Kernel, find_root  # noqa: E402

seen = []


class Fake(BaseHTTPRequestHandler):
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["content-length"])))
        seen.append((self.path, {h.lower(): v for h, v in self.headers.items()}, body))
        if self.path == "/v1/chat/completions":
            reply = {"choices": [{"message": {"role": "assistant", "content": '{"ok": "openai"}'}}]}
        elif self.path == "/v1/messages":
            reply = {"content": [{"type": "text", "text": '{"ok": "anthropic"}'}]}
        else:
            self.send_response(404), self.end_headers(), self.wfile.write(b'{"error": "bad path"}')
            return
        data = json.dumps(reply).encode()
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):
        pass


srv = HTTPServer(("127.0.0.1", 0), Fake)
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{srv.server_port}"

k = Kernel(find_root())
k.load(["config", "llm", "llm_openai", "llm_anthropic"])
cfg = k.get("config")
cfg["openai"].update(base_url=base + "/v1", model="test-model", api_key="test-key-openai")
cfg["anthropic"].update(base_url=base, model="test-claude", api_key="test-key-anthropic")
chat = k.get("llm.chat")

cfg["provider"] = "openai"
assert chat("SYS", "USER") == '{"ok": "openai"}'
path, headers, body = seen[-1]
assert path == "/v1/chat/completions" and headers["authorization"] == "Bearer test-key-openai"
assert body["model"] == "test-model" and body["messages"][0] == {"role": "system", "content": "SYS"}

cfg["provider"] = "anthropic"
assert chat("SYS", "USER") == '{"ok": "anthropic"}'
path, headers, body = seen[-1]
assert path == "/v1/messages" and headers["x-api-key"] == "test-key-anthropic"
assert headers["anthropic-version"] == "2023-06-01" and body["system"] == "SYS" and body["max_tokens"] > 0

cfg["anthropic"]["base_url"] = base + "/wrong"
try:
    chat("SYS", "USER")
    raise SystemExit("expected HTTP error")
except RuntimeError as e:
    assert "HTTP 404" in str(e), e

cfg["openai"]["api_key"] = ""
os.environ.pop("OPENAI_API_KEY", None)
cfg["provider"] = "openai"
try:
    chat("SYS", "USER")
    raise SystemExit("expected missing-key error")
except RuntimeError as e:
    assert "API key" in str(e)
print("providers OK:", [p for p, _, _ in seen])
