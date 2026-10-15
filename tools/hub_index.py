"""The WTF Hub index. One job: the .wtfpack files of a folder -> hub/index.json (what the app lists and installs).

Each pack is described by its own manifest (name, version, minimum WTF) plus where it is downloaded, its size and its
SHA-256 (tools/hub.py entry_for). Newer versions of the same pack replace older ones in the index.

  python tools/hub_index.py packs --base https://raw.githubusercontent.com/LxCenady/Wace_Training_Framework/main/packs
                            [--tier CAIE9709=experimental] [--out hub/index.json]
"""
import argparse, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hub  # noqa: E402


def version_key(v):
    return tuple(int(x) if x.isdigit() else x for x in str(v).replace("-", ".").split("."))


def build(folder, base, tiers=None):
    best = {}
    for path in sorted(Path(folder).glob("*.wtfpack")):
        entry = hub.entry_for(path, f"{base.rstrip('/')}/{path.name}", (tiers or {}).get(path.name.split("-")[0], "official"))
        if entry["id"] not in best or version_key(entry["version"]) > version_key(best[entry["id"]]["version"]):
            best[entry["id"]] = entry
    return {"hub": 1, "packs": sorted(best.values(), key=lambda e: (e["tier"] != "official", e["id"]))}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("folder")
    p.add_argument("--base", required=True, help="the HTTPS folder the pack files are downloaded from")
    p.add_argument("--tier", action="append", default=[], help="ID=tier for packs that are not official")
    p.add_argument("--out", default="hub/index.json")
    a = p.parse_args(argv)
    index = build(a.folder, a.base, dict(t.split("=", 1) for t in a.tier))
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"{out}: {len(index['packs'])} packs")


if __name__ == "__main__":
    main()
