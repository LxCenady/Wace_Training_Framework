"""Edition. One job: which product this build is — name, update repository, allowed AI providers.

Reads app/edition.json if present; without it this is plain WTF (every provider allowed). A derived product such as
WTF Studio ships its own edition.json instead of patching plugins, so it can keep merging WTF unchanged:
  {"name": "WTF Studio", "repo": "owner/WTF-Studio", "providers": ["wtf"], "default_provider": "wtf"}
"""
import json, os

DEFAULT = {"name": "WACE Maths 学习系统", "short": "WTF", "repo": "LxCenady/Wace_Training_Framework",
           "providers": None, "default_provider": None}


def load(app_dir):
    path = os.path.join(app_dir, "edition.json")
    data = dict(DEFAULT)
    if os.path.isfile(path):
        data.update(json.load(open(path, encoding="utf-8")))
    return data


def setup(k):
    import sys
    app_dir = getattr(sys, "_MEIPASS", None) or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ed = load(app_dir)
    cfg = k.get("config")
    allowed = ed["providers"]
    if allowed and cfg.get("provider") not in allowed + ["mock"]:  # mock: the offline test provider, never shown
        cfg["provider"] = ed["default_provider"] or allowed[0]

    k.provide("edition", ed)
    k.provide("edition.allows", lambda provider: not allowed or provider in allowed or provider == "mock")
