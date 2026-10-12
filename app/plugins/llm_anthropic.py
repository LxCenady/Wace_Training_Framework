"""Anthropic messages format (also any compatible endpoint: set base_url)."""


def setup(k):
    post = k.get("llm.post_json")

    def chat(s, system, user, timeout):
        body = {"model": s["model"], "max_tokens": 8000, "system": system,
                "messages": [{"role": "user", "content": user}]}
        body.update(s.get("extra_body") or {})
        r = post(s["base_url"].rstrip("/") + "/v1/messages",
                 {"x-api-key": s["api_key"], "anthropic-version": "2023-06-01"}, body, timeout)
        k.emit("llm.usage", s["model"], r.get("usage") or {})  # token counts: cost estimates, daily quotas
        return "".join(b.get("text", "") for b in r["content"] if b.get("type") == "text")

    k.get("llm.providers")["anthropic"] = chat
