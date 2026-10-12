"""Settings dialog. One job: let the user plug in their own provider, base URL, model and API key — and the
few app-wide choices (language, update check, where exported PDFs go).

Provides export.target(file name, title) -> path and export.folder(title) -> folder: with an export folder set,
exports go straight there (a number is added instead of overwriting); without one, the usual save dialog."""
import json, os, re, threading
import tkinter as tk
from tkinter import filedialog, ttk

PROVIDERS = {"anthropic": "Anthropic 格式 (/v1/messages)", "openai": "OpenAI 格式 (/chat/completions，默认 DeepSeek)",
             "wtf": "WTF 账号（学校/订阅，无需 API key；在「设置 → 账号」登录）", "mock": "离线测试 (不调用 API)"}


def setup(k):
    cfg = k.get("config")

    def export_folder(title="选择保存的文件夹"):
        fixed = cfg.get("export_dir", "")
        if fixed:
            os.makedirs(fixed, exist_ok=True)
            return fixed
        return filedialog.askdirectory(title=title) or None

    def export_target(name, title="导出 PDF"):
        """Where an export goes: <export folder>/<name> (never overwriting: "name (2).pdf" …), else ask."""
        name = re.sub(r'[\\/:*?"<>|]+', "_", name)
        fixed = cfg.get("export_dir", "")
        if not fixed:
            return filedialog.asksaveasfilename(title=title, defaultextension=".pdf", filetypes=[("PDF", "*.pdf")],
                                                initialfile=name) or None
        os.makedirs(fixed, exist_ok=True)
        stem, ext = os.path.splitext(name)
        path, n = os.path.join(fixed, name), 1
        while os.path.exists(path):
            n += 1
            path = os.path.join(fixed, f"{stem} ({n}){ext}")
        return path

    k.provide("export.target", export_target)
    k.provide("export.folder", export_folder)

    def describe():
        name = cfg["provider"]
        model = cfg.get(name, {}).get("model", "") if name not in ("mock", "wtf") else ""
        k.get("ui.status")(f"模型：{PROVIDERS[name]} {model}" + ("   — 在「设置」里接入你自己的 API key" if name == "mock" else ""))

    def dialog():
        top = tk.Toplevel(k.get("ui.root"))
        top.title("模型与 API key")
        top.resizable(False, False)
        f = ttk.Frame(top, padding=16)
        f.pack(fill="both")
        prov = tk.StringVar(value=cfg["provider"])
        restricted = bool(k.get("edition", {}).get("providers"))  # e.g. WTF Studio: the WTF account only
        shown = {p: label for p, label in PROVIDERS.items()
                 if k.get("edition.allows", lambda _: True)(p) and not (restricted and p == "mock")}
        ttk.Label(f, text="接口格式").grid(row=0, column=0, sticky="w")
        for i, (key, label) in enumerate(shown.items()):
            ttk.Radiobutton(f, text=label, value=key, variable=prov).grid(row=i, column=1, sticky="w")
        vars_, row = {}, 3
        for name in [p for p in ("anthropic", "openai") if p in shown]:
            row += 1
            ttk.Label(f, text=PROVIDERS[name], style="H.TLabel").grid(row=row, column=0, columnspan=2, sticky="w",
                                                                    pady=(12, 2))
            for field, label in (("base_url", "Base URL"), ("model", "模型名"), ("api_key", "API key"),
                                 ("extra_body", "额外参数 JSON")):
                row += 1
                value = cfg[name].get(field, "")
                v = tk.StringVar(value=json.dumps(value or {}, ensure_ascii=False) if field == "extra_body" else value)
                vars_[(name, field)] = v
                ttk.Label(f, text=label).grid(row=row, column=0, sticky="w")
                ttk.Entry(f, textvariable=v, width=56, show="•" if field == "api_key" else "").grid(row=row, column=1,
                                                                                                   pady=2)
        row += 1
        retries = tk.IntVar(value=cfg.get("retries", 2))
        ttk.Label(f, text="验证失败重试次数").grid(row=row, column=0, sticky="w", pady=(12, 0))
        ttk.Spinbox(f, from_=0, to=5, textvariable=retries, width=4).grid(row=row, column=1, sticky="w", pady=(12, 0))
        row += 1
        updates = tk.BooleanVar(value=cfg.get("update_check", True))
        ttk.Checkbutton(f, text="启动时检查 GitHub 上的新版本（每天最多一次）", variable=updates).grid(
            row=row, column=0, columnspan=2, sticky="w", pady=(8, 0))
        row += 1
        languages = {"中文": "zh", "English": "en"}
        language = tk.StringVar(value=next(n for n, c in languages.items() if c == cfg.get("language", "zh")))
        ttk.Label(f, text="界面语言 / Language").grid(row=row, column=0, sticky="w", pady=(8, 0))
        ttk.Combobox(f, textvariable=language, values=list(languages), state="readonly", width=10).grid(
            row=row, column=1, sticky="w", pady=(8, 0))
        row += 1
        ttk.Label(f, text="切换语言后重启生效 / restart to apply", style="Muted.TLabel").grid(
            row=row, column=1, sticky="w")
        row += 1
        export_dir = tk.StringVar(value=cfg.get("export_dir", ""))
        ttk.Label(f, text="导出文件夹").grid(row=row, column=0, sticky="w", pady=(8, 0))
        pick = ttk.Frame(f)
        pick.grid(row=row, column=1, sticky="w", pady=(8, 0))
        ttk.Entry(pick, textvariable=export_dir, width=44).pack(side="left")
        ttk.Button(pick, text="选择…", command=lambda: export_dir.set(
            filedialog.askdirectory(title="导出的 PDF 存到哪里") or export_dir.get())).pack(side="left", padx=4)
        row += 1
        ttk.Label(f, text="设置后导出的 PDF 直接存进这个文件夹（重名自动加序号）；留空 = 每次导出时询问",
                  style="Muted.TLabel").grid(row=row, column=1, sticky="w")
        row += 1
        if not restricted:  # an edition without API keys (WTF Studio) has nothing to explain here
            ttk.Label(f, text=f"API key 只保存在本机：{k.get('config.path')}\n留空则读取环境变量 DEEPSEEK_API_KEY / OPENAI_API_KEY / "
                              "ANTHROPIC_API_KEY。Base URL 可改成任何兼容该格式的服务。\n"
                              "额外参数会并入每次请求，例如 DeepSeek 思考强度："
                              '{"thinking": {"type": "enabled"}, "reasoning_effort": "high"}',
                      style="Muted.TLabel", justify="left").grid(row=row, column=0, columnspan=2, sticky="w", pady=8)
        row += 1
        result = tk.StringVar()
        ttk.Label(f, textvariable=result, wraplength=520).grid(row=row + 1, column=0, columnspan=2, sticky="w")

        def apply():
            """Copy the form into cfg; returns False (and says why) if an extra-parameters field is not JSON."""
            for (name, field), v in vars_.items():
                if field == "extra_body":
                    try:
                        json.loads(v.get().strip() or "{}")
                    except ValueError as e:
                        result.set(f"✗ {name} 的额外参数不是合法 JSON：{e}")
                        return False
            cfg["provider"] = prov.get()
            for (name, field), v in vars_.items():
                text = v.get().strip()
                cfg[name][field] = json.loads(text or "{}") if field == "extra_body" else text
            cfg["retries"] = retries.get()
            cfg["language"] = languages[language.get()]
            cfg["update_check"] = updates.get()
            cfg["export_dir"] = export_dir.get().strip()
            return True

        def save():
            if not apply():
                return
            k.get("config.save")()
            describe()
            top.destroy()

        def test():
            if not apply():
                return
            result.set("测试中…")
            post = k.get("ui.post")

            def work():
                try:
                    reply = k.get("llm.chat")("[STAGE:PING] Reply with the JSON {\"ok\": true} only.", "ping")
                    post(lambda: result.set("✓ 连接成功：" + reply.strip()[:200]))
                except Exception as e:
                    msg = f"✗ {e}"
                    post(lambda: result.set(msg[:400]))

            threading.Thread(target=work, daemon=True).start()

        btns = ttk.Frame(f)
        btns.grid(row=row, column=0, columnspan=2, sticky="e")
        ttk.Button(btns, text="测试连接", command=test).pack(side="left", padx=4)
        ttk.Button(btns, text="保存", style="Accent.TButton", command=save).pack(side="left")

    menu = tk.Menu(k.get("ui.menu"), tearoff=False)
    menu.add_command(label="模型与 API key…", command=dialog)
    k.get("ui.menu").add_cascade(label="设置", menu=menu)
    k.provide("ui.menu.settings", menu)  # e.g. 设置 → 账号… (plugins/ui_account.py)
    k.on("ui.ready", describe)
