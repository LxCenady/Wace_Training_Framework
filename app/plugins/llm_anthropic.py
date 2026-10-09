"""Anthropic messages format (also any compatible endpoint: set base_url)."""


def setup(k):
    post = k.get("llm.post_json")

    def chat(s, system, user, timeout):
        body = {"model": s["model"], "max_tokens": 8000, "system": system,
                "messages": [{"role": "user", "content": user}]}
        r = post(s["base_url"].rstrip("/") + "/v1/messages",
                 {"x-api-key": s["api_key"], "anthropic-version": "2023-06-01"}, body, timeout)
        return "".join(b.get("text", "") for b in r["content"] if b.get("type") == "text")

    k.get("llm.providers")["anthropic"] = chat
