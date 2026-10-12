"""Provider "wtf": the model behind the user's WTF account. One job: send chat requests to the account server.

The account server speaks the OpenAI chat-completions format at <server>/v1 (docs/account_api.md), authenticates
with the session token from plugins/account.py, charges the daily quota and forwards to the model it holds the key
for. So no API key on the student's computer. Must load after llm_openai and account.
"""


def setup(k):
    openai_chat = k.get("llm.providers")["openai"]
    ProviderError = k.get("llm.ProviderError")
    cfg = k.get("config")

    def chat(s, system, user, timeout):
        acct = cfg.get("account", {})
        if not (acct.get("server") and acct.get("token")):
            raise ProviderError("尚未登录 WTF 账号：在「设置 → 账号」里登录，或在「模型与 API key」里改用自己的 API key")
        settings = {"base_url": acct["server"].rstrip("/") + "/v1", "api_key": acct["token"],
                    "model": s.get("model") or "default", "extra_body": {}}
        try:
            return openai_chat(settings, system, user, timeout)
        except ProviderError as e:  # 401/402/403 from the account server mean the account, not a key
            raise ProviderError("WTF 账号登录已过期或无权使用 AI 出题，请重新登录（" + str(e).split("：", 1)[-1][:120] + "）") from None
        except RuntimeError as e:
            if str(e).startswith("HTTP 429"):
                raise ProviderError("今日 AI 额度已用完，明天会自动恢复（" + str(e)[9:150] + "）") from None
            raise

    k.get("llm.providers")["wtf"] = chat
