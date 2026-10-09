"""Rebuild every derived file from the papers. One job: run the pipeline steps in order.

papers -> questions.json -> topic PDFs + question banks -> wace.db (methods notes and tags are hand-written inputs)
Runs in-process (importable as build_all.run) so the packaged app can call it without a Python on PATH.
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run(subjects=("MAM", "MAS"), log=print):
    import segment, build_docs, build_bank, build_db  # noqa: E401 (import late: ROOT is read at import time)
    for name, step in (("segment", segment.main), ("topic PDFs", build_docs.build), ("question banks", build_bank.build)):
        for s in subjects:
            log(f"{name}: {s}")
            step(s)
    log("database")
    db, problems = build_db.build(os.path.join(build_db.ROOT, "wace.db"))
    db.close()
    for p in problems:
        log("  " + p)
    return problems


if __name__ == "__main__":
    run(sys.argv[1:] or ("MAM", "MAS"))
