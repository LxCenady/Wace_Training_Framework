"""Thin glue: locate the data folder, load the plugins listed in plugins.txt (or setup.txt before the
question bank exists), run."""
import os, sys

FROZEN = getattr(sys, "frozen", False)  # packaged by tools/package_win.py
HERE = getattr(sys, "_MEIPASS", None) or os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from kernel import Kernel  # noqa: E402


def find_root():
    env = os.environ.get("WACE_MATHS_ROOT")
    if env and os.path.isfile(os.path.join(env, "sources.tsv")):
        return env
    return os.path.dirname(sys.executable) if FROZEN else os.path.dirname(HERE)


def plugin_names(path=None):
    path = path or os.path.join(HERE, "plugins.txt")
    names = (line.split("#")[0].strip() for line in open(path, encoding="utf-8"))
    return [n for n in names if n]


def headless(root, args):
    """WTF --import DIR [--import DIR …] [--build]: import papers / build the bank without the GUI; log to WTF.log."""
    import fetch, build_all
    with open(os.path.join(root, "WTF.log"), "a", encoding="utf-8") as log:
        say = lambda m: (print(m), log.write(m + "\n"), log.flush())  # noqa: E731
        for i, a in enumerate(args):
            if a == "--import" and i + 1 < len(args):
                for rel in fetch.import_dir(args[i + 1], root):
                    say(f"imported {rel}")
        say(f"{len(fetch.missing(root))} paper(s) still missing")
        if "--build" in args:
            problems = build_all.run(log=say)
            say(f"built wace.db ({len(problems)} notes)")


def log_errors(root):
    """Any uncaught error (main thread, worker threads, Tk callbacks) goes to WTF.log with its traceback."""
    import threading, traceback

    def write(kind, tb):
        with open(os.path.join(root, "WTF.log"), "a", encoding="utf-8") as f:
            f.write(f"\n--- {kind} ---\n{''.join(tb)}")

    sys.excepthook = lambda t, v, tb: write("error", traceback.format_exception(t, v, tb))
    threading.excepthook = lambda a: write("thread error", traceback.format_exception(a.exc_type, a.exc_value,
                                                                                      a.exc_traceback))
    return write


def main():
    root = find_root()
    write = log_errors(root)
    os.environ["WACE_MATHS_ROOT"] = root  # tools/*.py read it at import time
    sys.path.insert(0, os.path.join(HERE, "tools") if FROZEN else os.path.join(root, "tools"))
    if any(a in ("--import", "--build") for a in sys.argv[1:]):
        try:
            return headless(root, sys.argv[1:])
        except Exception:
            import traceback
            write("build error", traceback.format_exc())
            sys.exit(1)
    k = Kernel(root)
    ready = os.path.isfile(os.path.join(root, "wace.db"))
    k.load(plugin_names(None if ready else os.path.join(HERE, "setup.txt")))
    k.get("ui.run")()


if __name__ == "__main__":
    if sys.argv[1:2] == ["--symcheck"]:  # child process of plugins/symcheck.py: no GUI, no data folder needed
        from plugins.symcheck import worker
        worker()
    else:
        main()
