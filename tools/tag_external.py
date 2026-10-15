"""Tag one imported external paper using the user's configured API; preserve confirmed human labels.

Usage: .venv/Scripts/python tools/tag_external.py --list
       .venv/Scripts/python tools/tag_external.py --paper ID
"""
import argparse
from pathlib import Path
import sqlite3
import sys


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--list", action="store_true")
    choice.add_argument("--paper")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if not (root / "external.db").is_file():
        parser.error("No external library: import a paper and its answer in WTF first.")
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))
    from kernel import Kernel
    k = Kernel(str(root))
    k.load(["external_pdf", "external_store"])
    store = k.get("external.store")()
    if args.list:
        try:
            for paper in store.papers():
                print(paper["id"], paper["subject"], paper["section"], paper["title"], paper["source"], paper["count"])
        finally:
            store.close()
        return 0
    import subjects  # tools/ (this folder)
    db = sqlite3.connect(Path(subjects.bank_path(root)).as_uri() + "?mode=ro", uri=True)

    class Catalogue:
        def q(self, query, *parameters):
            return db.execute(query, parameters).fetchall()

    k.provide("store", Catalogue())
    k.load(["config", "llm", "llm_openai", "llm_anthropic", "llm_mock", "external_tagger"])
    done = 0
    try:
        store.paper(args.paper)  # reject a typo before any API calls
        for q in store.search(paper=args.paper):
            if q["confirmed"]:
                continue
            result = k.get("external.tag.propose")(q["id"])
            store.save_proposal(q["id"], result, q)
            done += 1
            print(q["id"], q["label"], ",".join(result["tags"]), "uncertain" if result["uncertain"] else "draft", flush=True)
    except Exception as exc:
        print(f"Stopped after {done} saved drafts: {exc}", file=sys.stderr)
        return 1
    finally:
        store.close()
        db.close()
    print(f"Saved {done} drafts; review and confirm them in the external library.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
