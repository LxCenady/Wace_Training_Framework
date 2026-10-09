"""Settings dialog. One job: let the user plug in their own provider, base URL, model and API key."""
import json, threading
import tkinter as tk
from tkinter import ttk

PROVIDERS = {"anthropic": "Anthropic 格式 (/v1/messages)", "openai": "OpenAI 格式 (/chat/completions，默认 DeepSeek)",
             "mock": "离线测试 (不调用 API)"}


def setup(k):
    cfg = k.get("config")

    def describe():
        name = cfg["provider"]
        model = cfg.get(name, {}).get("model", "") if name != "mock" else ""
        k.get("ui.status")(f"模型：{PROVIDERS[name]} {model}" + ("   — 在「设置」里接入你自己的 API key" if name == "mock" else ""))

    def dialog():
        top = tk.Toplevel(k.get("ui.root"))
        top.title("模型与 API key")
        top.resizable(False, False)
        f = ttk.Frame(top, padding=16)
        f.pack(fill="both")
        prov = tk.StringVar(value=cfg["provider"])
        ttk.Label(f, text="接口格式").grid(row=0, column=0, sticky="w")
        for i, (key, label) in enumerate(PROVIDERS.items()):
            ttk.Radiobutton(f, text=label, value=key, variable=prov).grid(row=i, column=1, sticky="w")
        vars_, row = {}, 3
        for name in ("anthropic", "openai"):
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
        ttk.Label(f, text=f"API key 只保存在本机：{k.get('config.path')}\n留空则读取环境变量 DEEPSEEK_API_KEY / OPENAI_API_KEY / "
                          "ANTHROPIC_API_KEY。Base URL 可改成任何兼容该格式的服务。\n"
                          "额外参数会并入每次请求，例如 DeepSeek 思考强度："
                          '{"thinking": {"type": "enabled"}, "reasoning_effort": "max"}',
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
    k.on("ui.ready", describe)
