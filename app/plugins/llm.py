"""Provider registry. One job: chat(system, user) -> text via the provider chosen in config.

A provider plugin registers fn(settings, system, user, timeout) -> str in k.get("llm.providers").
"""
import json, os, urllib.error, urllib.request

ENV_KEYS = {"openai": "OPENAI_API_KEY", "anthropic": "ANTHROPIC_API_KEY"}


def post_json(url, headers, body, timeout):
    """Stdlib HTTP POST; raises RuntimeError with the server's message on HTTP errors."""
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"content-type": "application/json", **headers})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode(errors='replace')[:500]}") from None


def setup(k):
    providers = k.provide("llm.providers", {})

    def chat(system, user):
        cfg = k.get("config")
        name = cfg["provider"]
        settings = dict(cfg.get(name, {}))
        if name in ENV_KEYS and not settings.get("api_key"):
            settings["api_key"] = os.environ.get(ENV_KEYS[name], "")
        if name in ENV_KEYS and not settings.get("api_key"):
            raise RuntimeError(f"未设置 {name} API key（设置 → 模型与 API key）")
        if name in ENV_KEYS and not settings.get("model"):
            raise RuntimeError(f"未设置 {name} 模型名（设置 → 模型与 API key）")
        return providers[name](settings, system, user, cfg.get("timeout", 180))

    k.provide("llm.chat", chat)
    k.provide("llm.post_json", post_json)
