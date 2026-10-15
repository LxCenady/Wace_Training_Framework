"""WTF Hub window. One job: show the Hub's packs and install the chosen one (hub_install does the work).

题库 → 管理科目 → WTF Hub 学科包… opens it; so does the first-run wizard when no subject is installed yet. A data pack
continues in the subject wizard (its papers); a recipe pack asks for the folder of its originals.
"""
import threading
import tkinter as tk
from tkinter import messagebox, ttk


def setup(k):
    def open_hub():
        root = k.get("ui.root")
        win = tk.Toplevel(root)
        win.title("WTF Hub")
        win.geometry("760x420")
        top = ttk.Frame(win, padding=10)
        top.pack(fill="both", expand=True)
        ttk.Label(top, text="WTF Hub 上的学科包：装好后按提示提供这门课的原卷 PDF（原卷不在包里）。",
                  style="Muted.TLabel", wraplength=720).pack(anchor="w", pady=(0, 8))
        cols = ("name", "exam", "version", "state")
        tree = ttk.Treeview(top, columns=cols, show="headings", height=12, selectmode="browse")
        for c, title, width in zip(cols, ("学科", "考试", "版本", "状态"), (330, 150, 100, 130)):
            tree.heading(c, text=title)
            tree.column(c, width=width, anchor="w")
        tree.pack(fill="both", expand=True)
        bar = ttk.Frame(top)
        bar.pack(fill="x", pady=(8, 0))
        note = ttk.Label(bar, text="正在读取 WTF Hub…", style="Muted.TLabel")
        note.pack(side="left")
        button = ttk.Button(bar, text="安装所选学科包", style="Accent.TButton", state="disabled")
        button.pack(side="right")
        entries = {}
        post = k.get("ui.post")
        lang = k.get("config").get("language", "zh")

        def show(data):
            for e in data["packs"]:
                state = ("需要更新 WTF" if not e["compatible"] else
                         "已安装 " + str(e["installed"]) if e.get("installed") else "可安装")
                exam = " ".join(x for x in (e.get("board"), e.get("exam")) if x) or e.get("tier", "")
                tree.insert("", "end", iid=e["id"], values=(e["name"].get(lang) or next(iter(e["name"].values())),
                                                              exam, e["version"], state))
                entries[e["id"]] = e
            note.configure(text=f"{len(entries)} 个学科包")
            button.configure(state="normal")

        def failed(error):
            note.configure(text="读取失败：" + str(error))

        def load():
            try:
                data = k.get("hub.index")()
                post(lambda: show(data))
            except Exception as e:  # offline, blocked, malformed index: say so, change nothing
                post(lambda: failed(e))

        def install():
            pick = tree.selection()
            if not pick:
                return
            e = entries[pick[0]]
            folder = None
            if e["kind"] == "recipe":
                import plat
                folder = plat.pick_folder("选择这门课原卷 PDF 所在的文件夹")
                if not folder:
                    return
            button.configure(state="disabled")
            note.configure(text=f"正在下载并安装 {e['id']}…")

            def work():
                try:
                    result = k.get("hub.install")(e["id"], folder)
                    post(lambda: done(result))
                except Exception as err:
                    post(lambda: (failed(err), button.configure(state="normal")))
            threading.Thread(target=work, daemon=True).start()

        def done(result):
            win.destroy()
            if result["kind"] == "data":
                messagebox.showinfo("学科包已安装", f"{result['subject']} 已安装。接下来在科目向导里提供这门课的原卷并建库。")
                k.get("subjects.manage")()
            elif result["next"] == "restart":
                messagebox.showinfo("学科包已安装", f"{result['subject']} 已安装：{result['questions']} 道题。重启 WTF 后出现在知识树。")
            else:
                messagebox.showwarning("还缺原卷", f"那个文件夹里没有找到 {len(result['missing'])} 份原卷：请在 WTF Compiler 里绑定。")
                k.get("compiler.open")()

        button.configure(command=install)
        threading.Thread(target=load, daemon=True).start()

    k.provide("hub.open", open_hub)
