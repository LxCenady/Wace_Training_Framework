"""Window shell. One job: root window, theme, left pane + tabbed right pane, and small widget helpers.

post(fn) is the only thread-safe entry: worker threads hand callables to the Tk thread through a queue.
"""
import queue
import tkinter as tk
from tkinter import ttk

C = dict(bg="#f3eee4", panel="#fbf8f2", ink="#1f1d1a", muted="#7a7368", accent="#1f3a73", line="#d8d0c2",
         warn="#8c2626", ok="#2f6b3a")
FONT = "Microsoft YaHei UI"


def setup(k):
    root = tk.Tk()
    root.title("WACE Maths 学习系统")
    root.geometry("1600x900")
    root.configure(bg=C["bg"])
    st = ttk.Style(root)
    st.theme_use("clam")
    st.configure(".", background=C["bg"], foreground=C["ink"], font=(FONT, 10), bordercolor=C["line"],
                 lightcolor=C["bg"], darkcolor=C["line"], troughcolor=C["bg"])
    st.configure("Treeview", background=C["panel"], fieldbackground=C["panel"], rowheight=25, borderwidth=0)
    st.map("Treeview", background=[("selected", C["accent"])], foreground=[("selected", "#ffffff")])
    st.configure("TNotebook", background=C["bg"], borderwidth=0)
    st.configure("TNotebook.Tab", padding=(14, 5), background=C["bg"])
    st.map("TNotebook.Tab", background=[("selected", C["panel"])])
    st.configure("TButton", padding=(10, 4), background=C["panel"])
    st.configure("Accent.TButton", foreground="#ffffff", background=C["accent"])
    st.map("Accent.TButton", background=[("active", "#2d4f94"), ("disabled", C["line"])])
    st.configure("Muted.TLabel", foreground=C["muted"])
    st.configure("H.TLabel", font=(FONT, 13, "bold"))
    st.configure("Panel.TFrame", background=C["panel"])

    menubar = tk.Menu(root)
    root.config(menu=menubar)
    pane = ttk.PanedWindow(root, orient="horizontal")
    pane.pack(fill="both", expand=True)
    left, tabs = ttk.Frame(pane, width=440), ttk.Notebook(pane)
    pane.add(left, weight=0)
    pane.add(tabs, weight=1)

    def first_layout(e):  # ttk.PanedWindow ignores child width; place the sashes once it has a real size
        if e.width > 900:
            pane.sashpos(0, 460)
            pane.unbind("<Configure>")
            k.emit("ui.layout", pane, e.width)  # plugins that added panes (e.g. the formula sheet) place theirs

    pane.bind("<Configure>", first_layout)
    status = tk.StringVar()
    ttk.Label(root, textvariable=status, style="Muted.TLabel", anchor="w").pack(fill="x", padx=10, pady=3)

    jobs = queue.Queue()

    def pump():
        while not jobs.empty():
            jobs.get_nowait()()
        root.after(60, pump)

    pages = {}

    def tab(key, title):
        """Get (or create) the tab `key`, select it, and return a fresh empty frame inside it."""
        if key not in pages:
            pages[key] = ttk.Frame(tabs)
            tabs.add(pages[key], text=title)
        page = pages[key]
        for w in page.winfo_children():
            w.destroy()
        tabs.select(page)
        return page

    def scroll(parent):
        """A vertically scrolling frame (mouse wheel while hovered); returns the inner frame."""
        canvas = tk.Canvas(parent, bg=C["panel"], highlightthickness=0)
        bar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        inner = ttk.Frame(canvas, style="Panel.TFrame")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=bar.set)
        bar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        wheel = lambda e: canvas.yview_scroll(int(-e.delta / 120), "units")  # noqa: E731
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", wheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        return inner

    def text(parent, height=10, **kw):
        """Read-only rich text with tags h, sub, muted, accent, warn, ok, mono; returns the Text widget."""
        frame = ttk.Frame(parent)
        t = tk.Text(frame, wrap="word", height=height, bg=C["panel"], fg=C["ink"], relief="flat", padx=14, pady=10,
                    font=(FONT, 11), spacing1=2, spacing3=2, insertwidth=0, **kw)
        bar = ttk.Scrollbar(frame, orient="vertical", command=t.yview)
        t.configure(yscrollcommand=bar.set)
        bar.pack(side="right", fill="y")
        t.pack(side="left", fill="both", expand=True)
        t.tag_configure("h", font=(FONT, 14, "bold"), foreground=C["accent"], spacing3=6)
        t.tag_configure("sub", font=(FONT, 11, "bold"), spacing1=8)
        for name in ("muted", "accent", "warn", "ok"):
            t.tag_configure(name, foreground=C[name])
        t.tag_configure("mono", font=("Consolas", 10))
        t.configure(state="disabled")
        t.frame = frame
        return t

    def write(t, s, *tags):
        t.configure(state="normal")
        t.insert("end", s, tags)
        t.configure(state="disabled")

    def clear(t):
        t.configure(state="normal")
        t.delete("1.0", "end")
        t.configure(state="disabled")

    k.provide("ui.root", root)
    k.provide("ui.menu", menubar)
    k.provide("ui.left", left)
    k.provide("ui.tab.frame", lambda key: pages.get(key))
    k.provide("ui.tabs", tabs)
    k.provide("ui.pane", pane)  # horizontal PanedWindow: [left, tabs, …panes added by plugins]
    k.provide("ui.tab", tab)
    k.provide("ui.post", jobs.put)
    k.provide("ui.status", status.set)
    k.provide("ui.scroll", scroll)
    k.provide("ui.text", text)
    k.provide("ui.write", write)
    k.provide("ui.clear", clear)
    k.provide("ui.colors", C)

    root.after(60, pump)

    def run():
        k.emit("ui.ready")
        root.mainloop()

    k.provide("ui.run", run)
