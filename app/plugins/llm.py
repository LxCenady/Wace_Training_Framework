"""Provider registry. One job: chat(system, user) -> text via the provider chosen in config.

A provider plugin registers fn(settings, system, user, timeout) -> str in k.get("llm.providers").
"""
import json, os, urllib.error, urllib.request

class ProviderError(RuntimeError):
    """The provider refuses every request until the user acts (top up, fix the key): retrying cannot help."""


FATAL = {401: "API key 无效或已失效，请在「设置」里检查", 402: "API 账户余额不足，请到服务商后台充值",
         403: "API key 没有权限使用这个模型"}

ENV_KEYS ={"openai": ("DEEPSEEK_API_KEY", "OPENAI_API_KEY"), "anthropic": ("ANTHROPIC_API_KEY",)}


def post_json(url, headers, body, timeout):
    """Stdlib HTTP POST; raises RuntimeError with the server's message on HTTP errors."""
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"content-type": "application/json", **headers})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:300]
        if e.code in FATAL:
            raise ProviderError(f"{FATAL[e.code]}（HTTP {e.code}）：{body}") from None
        raise RuntimeError(f"HTTP {e.code}: {body}") from None


def setup(k):
    providers = k.provide("llm.providers", {})

    def chat(system, user):
        cfg = k.get("config")
        name = cfg["provider"]
        settings = dict(cfg.get(name, {}))
        if name in ENV_KEYS and not settings.get("api_key"):
            settings["api_key"] = next((os.environ[v] for v in ENV_KEYS[name] if os.environ.get(v)), "")
        if name in ENV_KEYS and not settings.get("api_key"):
            raise RuntimeError(f"未设置 {name} API key（设置 → 模型与 API key）")
        if name in ENV_KEYS and not settings.get("model"):
            raise RuntimeError(f"未设置 {name} 模型名（设置 → 模型与 API key）")
        return providers[name](settings, system, user, cfg.get("timeout", 180))

    k.provide("llm.chat", chat)
    k.provide("llm.post_json", post_json)
    k.provide("llm.ProviderError", ProviderError)
