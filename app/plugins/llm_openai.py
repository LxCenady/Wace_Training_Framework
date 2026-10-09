"""OpenAI chat-completions format (also any compatible endpoint: set base_url)."""


def setup(k):
    post = k.get("llm.post_json")

    def chat(s, system, user, timeout):
        body = {"model": s["model"], "messages": [{"role": "system", "content": system},
                                                  {"role": "user", "content": user}]}
        body.update(s.get("extra_body") or {})
        r = post(s["base_url"].rstrip("/") + "/chat/completions",
                 {"authorization": f"Bearer {s['api_key']}"}, body, timeout)
        return r["choices"][0]["message"]["content"]

    k.get("llm.providers")["openai"] = chat
