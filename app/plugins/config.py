"""User settings. One job: load/save a JSON file in the user's profile.

API keys are supplied by the user and stored only here (never in the shared data folder).
If a key field is empty, the provider falls back to the DEEPSEEK_API_KEY / OPENAI_API_KEY / ANTHROPIC_API_KEY env var.
"""
import json, os
import plat

PATH = os.path.join(plat.user_dir("wace-maths"), "config.json")
# Default: DeepSeek through its OpenAI-compatible endpoint, thinking mode at max effort.
# extra_body is merged into every request body (provider-specific switches such as reasoning effort).
DEFAULTS = {
    "provider": "openai",
    "openai": {"base_url": "https://api.deepseek.com", "model": "deepseek-flash", "api_key": "",
               "extra_body": {"thinking": {"type": "enabled"}, "reasoning_effort": "max"}},
    "anthropic": {"base_url": "https://api.anthropic.com", "model": "claude-sonnet-5-5", "api_key": "",
                  "extra_body": {}},
    "retries": 2,
    "timeout": 900,
    "parallel": 4,  # questions generated at the same time in a batch
    "update_check": True,  # look for a newer GitHub release at start-up (at most once a day)
}


def load():
    cfg = json.loads(json.dumps(DEFAULTS))
    if os.path.exists(PATH):
        saved = json.load(open(PATH, encoding="utf-8"))
        for key, val in saved.items():
            if isinstance(val, dict) and isinstance(cfg.get(key), dict):
                cfg[key].update(val)
            else:
                cfg[key] = val
    return cfg


def save(cfg):
    os.makedirs(os.path.dirname(PATH), exist_ok=True)
    tmp = PATH + ".tmp"
    json.dump(cfg, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, PATH)


def setup(k):
    k.provide("config", load())
    k.provide("config.save", lambda: save(k.get("config")))
    k.provide("config.path", PATH)
