"""Thin glue: locate the data folder, load the plugins listed in plugins.txt, run."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from kernel import Kernel  # noqa: E402


def find_root():
    env = os.environ.get("WACE_MATHS_ROOT")
    if env and os.path.isfile(os.path.join(env, "wace.db")):
        return env
    return os.path.dirname(HERE)


def plugin_names(path=os.path.join(HERE, "plugins.txt")):
    names = (line.split("#")[0].strip() for line in open(path, encoding="utf-8"))
    return [n for n in names if n]


def main():
    k = Kernel(find_root())
    k.load(plugin_names())
    k.get("ui.run")()


if __name__ == "__main__":
    main()
