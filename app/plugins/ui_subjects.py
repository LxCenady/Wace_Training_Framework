"""管理科目. One job: reopen the import wizard over the existing bank to add or drop subjects.

题库 → 管理科目… restarts the app with --setup (main.py), which loads the wizard instead of the study system;
the wizard downloads what newly chosen subjects need, rebuilds for the chosen subjects, or returns unchanged.
"""
import os, subprocess, sys


def setup(k):
    def manage():
        main = [] if getattr(sys, "frozen", False) else [os.path.abspath(sys.modules["__main__"].__file__)]
        subprocess.Popen([sys.executable, *main, "--setup"], close_fds=True)
        k.get("ui.root").destroy()

    menu = k.get("ui.menu.bank", None)
    if menu is not None:
        menu.add_separator()
        menu.add_command(label="管理科目（添加或移除 MAM / MAS / MAA）…", command=manage)
    k.provide("subjects.manage", manage)
