"""WTF Hub in the app. One job: list the Hub's packs and install one the way any .wtfpack is installed.

WTF ships no subject: every course is a pack from the Hub (or a local file). A data pack is installed and then needs
its original papers (the subject wizard fetches and recognises them); a recipe pack is installed from a folder of
its originals (wtf_compiler). Downloads are verified against the Hub's SHA-256 (tools/hub.py).

  hub.index()                       -> {"packs": [entry + installed, compatible]}
  hub.install(pack_id, folder=None) -> {"kind", "subject", "next": "papers" | "restart" | "bind", ...}
"""
from pathlib import Path

import hub
import pack
import subjects


def setup(k):
    root = Path(k.root)
    version_file = Path(__file__).resolve().parents[1] / "version.txt"
    app_version = version_file.read_text(encoding="utf-8").strip() if version_file.exists() else "0.0.0"

    def url():
        return k.get("config").get("hub_url") or k.get("edition", {}).get("hub") or hub.DEFAULT

    def compatible(entry):
        need = str(entry.get("requires_wtf", ">=0.0.0"))
        try:
            return need.startswith(">=") and pack.version(need[2:]) <= pack.version(app_version)
        except ValueError:
            return False

    def index():
        data = hub.load(url())
        installed = {s: p.get("version") or (p.get("compiler") or {}).get("version")
                     for s, p in subjects.profiles(k.root).items()}
        for e in data["packs"]:
            e["installed"] = installed.get(e["id"])
            e["compatible"] = compatible(e)
        return data

    def install(pack_id, folder=None):
        entry = next((e for e in hub.load(url())["packs"] if e["id"] == pack_id), None)
        if entry is None:
            raise hub.HubError(f"{pack_id} is not on the Hub")
        if not compatible(entry):
            raise hub.HubError(f"{pack_id} needs WTF {entry.get('requires_wtf')}: update WTF first")
        path = hub.download(entry, root / "downloads")
        if entry["kind"] == "recipe":
            result = k.get("compiler.calls")["compiler_install"](str(path), folder)
            built = result.get("built") or {}
            ok = bool(built.get("subject")) and not built.get("error")
            return dict(kind="recipe", subject=built.get("subject") or pack_id, next="restart" if ok else "bind",
                        missing=result.get("missing", []), questions=built.get("questions"))
        current = root / entry["id"] / "pack.json"
        pack.install(str(path), k.root, overwrite=current.exists(), app_version=app_version)
        cfg = k.get("config")
        cfg["subjects"] = list(dict.fromkeys([*(cfg.get("subjects") or []), entry["id"]]))
        k.get("config.save")()
        return dict(kind="data", subject=entry["id"], next="papers")

    k.provide("hub.index", index)
    k.provide("hub.install", install)
    k.provide("hub.Error", hub.HubError)
