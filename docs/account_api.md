# WTF account server — API contract (v1, reserved)

The app side is implemented (`app/plugins/account.py`, `llm_wtf.py`, `ui_account.py`; test: `app/tests/test_account.py`
against a fake server). No server exists yet. A server that implements this contract works with WTF ≥ 2.1 unchanged.

Why a server: students sign in instead of configuring a model API key. The server holds the model key (e.g. DeepSeek),
counts each user's daily quota, and forwards requests. The app is open source, so nothing secret can live in it —
not the model key and not the Google OAuth client secret.

All bodies are JSON. Errors: an HTTP status and `{"error": "message shown to the student, in Chinese"}`.
Authenticated calls send `Authorization: Bearer <session token>`; `401` means the session is gone (the app signs
out locally and asks to sign in again).

## Sign-in

| Method | Path | Body → reply | Notes |
|---|---|---|---|
| POST | `/v1/auth/email/start` | `{email}` → `{}` | mail a short one-time code; the server decides who may join (e.g. only the school's domain, or an invite list) |
| POST | `/v1/auth/email/verify` | `{email, code}` → `{token, email}` | codes expire (≈10 min) and are single use; rate-limit attempts |
| GET | `/v1/auth/google/start?redirect_uri=…&state=…` | browser redirect | `redirect_uri` is always `http://127.0.0.1:<port>/callback` (loopback, any port — accept only that form). Server runs Google OAuth (authorization code + PKCE, scopes `openid email`), then redirects the browser to `redirect_uri?code=<one-time code>&state=<state>` |
| POST | `/v1/auth/exchange` | `{code, state, redirect_uri}` → `{token, email}` | one-time code (≈60 s) for a session token; check `state` and `redirect_uri` match the start request |
| POST | `/v1/auth/logout` | `{}` → `{}` | revoke the session token |

Session tokens: opaque random strings (store a hash server-side), long-lived (e.g. 90 days), revocable per device.

## Account and quota

`GET /v1/me` → `{email, plan, quota: {used, limit, unit, resets_at}}`
- `unit`: what the quota counts, e.g. `"题"` (generated questions) or `"k tokens"`; the app shows it as is.
- `resets_at`: local time text for display, e.g. `"00:00 (SGT)"`.

## Model access (OpenAI-compatible)

`POST /v1/chat/completions` — the OpenAI chat-completions request the app already sends to DeepSeek
(`model`, `messages`); `model` is `"default"` unless the user set one. The server:
1. checks the session and the quota; over quota → `429 {"error": "今日 AI 额度已用完"}` (the app tells the student it resets tomorrow);
2. replaces `model` with the real model, adds its own `extra_body` (e.g. DeepSeek thinking mode), forwards with its key;
3. returns the upstream reply unchanged (including `usage`), and charges the quota from `usage`.

One AI question is several calls (setter, solver, checker, examiner — see `app/plugins/generator.py`). If the quota is
counted in questions rather than tokens, count a question when the app reports it: reserved
`POST /v1/usage/question {kind: "similar"|"mistakes"|"unit"|"mc", subject}` (not sent by the app yet).

## Privacy and safety (pilot)

- Collect only the e-mail; keep request logs only as long as needed for the quota and abuse checks.
- Never log message content beyond what debugging needs; students' questions and answers are personal data (PDPA).
- No SCSA past-paper text should be stored server-side; the app sends past questions only as generation context.
- Budget cap per month on the server side, so a bug or abuse cannot run up the model bill.
