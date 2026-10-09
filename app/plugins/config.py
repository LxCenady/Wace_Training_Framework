"""User settings. One job: load/save a JSON file in the user's profile.

API keys are supplied by the user and stored only here (never in the shared data folder).
If a key field is empty, the provider falls back to the OPENAI_API_KEY / ANTHROPIC_API_KEY env var.
"""
import json, os

PATH = os.path.join(os.environ.get("APPDATA") or os.path.expanduser("~"), "wace-maths", "config.json")
DEFAULTS = {
    "provider": "mock",
    "openai": {"base_url": "https://api.openai.com/v1", "model": "", "api_key": ""},
    "anthropic": {"base_url": "https://api.anthropic.com", "model": "claude-sonnet-5-5", "api_key": ""},
    "retries": 2,
    "timeout": 180,
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
