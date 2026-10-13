"""设置 → 账号… One job: the dialog for signing in to a WTF account (plugins/account.py) and using it for AI questions.

Server address (WTF Academy's by default; a school may run its own), e-mail code sign-in, Google sign-in, the
plan (student / teacher subscription) and today's quota, sign-out, a link to the plans, and "use my WTF account for
AI questions" (provider "wtf"). Network calls run in a thread; the window never blocks. The account is optional:
WTF works with the user's own API key without it.
"""
import threading, webbrowser

OFFICIAL = "https://api.wtf-academy.org"  # WTF Academy's account server (behind Cloudflare)
PLANS_PAGE = "https://wtf-academy.org/pricing"
PLAN_NAMES = {"student": "学生档", "teacher": "教师档"}
import tkinter as tk
from tkinter import ttk


def setup(k):
    cfg, post = k.get("config"), k.get("ui.post")
    Error = k.get("account.Error")

    def dialog():
        top = tk.Toplevel(k.get("ui.root"))
        top.title("WTF 账号")
        top.resizable(False, False)
        f = ttk.Frame(top, padding=16)
        f.pack(fill="both")
        acct = cfg.setdefault("account", {})
        server = tk.StringVar(value=acct.get("server") or OFFICIAL)
        email, code = tk.StringVar(value=acct.get("email", "")), tk.StringVar()
        use = tk.BooleanVar(value=cfg.get("provider") == "wtf")
        status, quota = tk.StringVar(), tk.StringVar()

        ttk.Label(f, text="账号服务器").grid(row=0, column=0, sticky="w")
        ttk.Entry(f, textvariable=server, width=44).grid(row=0, column=1, columnspan=2, sticky="w", pady=2)
        ttk.Label(f, text="默认是 WTF Academy 官方服务器；学校自建的服务器可在这里改。登录后 AI 出题不需要自己的 API key，按套餐的每日额度使用。",
                  style="Muted.TLabel", wraplength=440).grid(row=1, column=1, columnspan=2, sticky="w")
        ttk.Label(f, textvariable=status, style="H.TLabel").grid(row=2, column=0, columnspan=3, sticky="w", pady=(10, 2))
        ttk.Label(f, textvariable=quota, style="Muted.TLabel").grid(row=3, column=0, columnspan=3, sticky="w")

        ttk.Label(f, text="邮箱").grid(row=4, column=0, sticky="w", pady=(10, 0))
        ttk.Entry(f, textvariable=email, width=30).grid(row=4, column=1, sticky="w", pady=(10, 0))
        send = ttk.Button(f, text="发送验证码")
        send.grid(row=4, column=2, sticky="w", padx=4, pady=(10, 0))
        ttk.Label(f, text="验证码").grid(row=5, column=0, sticky="w", pady=2)
        ttk.Entry(f, textvariable=code, width=12).grid(row=5, column=1, sticky="w", pady=2)
        login = ttk.Button(f, text="邮箱登录", style="Accent.TButton")
        login.grid(row=5, column=2, sticky="w", padx=4)
        row = ttk.Frame(f)
        row.grid(row=6, column=0, columnspan=3, sticky="w", pady=(10, 0))
        google = ttk.Button(row, text="用 Google 账号登录")
        google.pack(side="left")
        out = ttk.Button(row, text="退出登录")
        out.pack(side="left", padx=8)
        ttk.Button(row, text="订阅套餐（学生 / 教师）…", command=lambda: webbrowser.open(PLANS_PAGE)).pack(side="left")
        ttk.Checkbutton(f, text="AI 出题使用 WTF 账号（不用自己的 API key）", variable=use).grid(
            row=7, column=0, columnspan=3, sticky="w", pady=(10, 0))
        msg = tk.StringVar()
        ttk.Label(f, textvariable=msg, wraplength=440).grid(row=8, column=0, columnspan=3, sticky="w", pady=(8, 0))
        ttk.Button(f, text="保存", style="Accent.TButton", command=lambda: save(close=True)).grid(row=9, column=2, sticky="e")

        def save(close=False):
            acct["server"] = server.get().strip()
            if use.get():
                cfg["provider"] = "wtf"
            elif cfg.get("provider") == "wtf":
                cfg["provider"] = "openai"
            k.get("config.save")()
            if close:
                top.destroy()

        def refresh():
            i = k.get("account.info")()
            status.set(f"已登录：{i['email']}" if i["signed_in"] else "未登录")
            quota.set("")
            if i["signed_in"]:
                def work():
                    try:
                        me = k.get("account.me")()
                        q = me.get("quota", {})
                        plan = PLAN_NAMES.get(me.get("plan"), me.get("plan") or "")
                        text = (f"套餐：{plan} · " if plan else "") +                             f"今日 AI 额度：已用 {q.get('used', '?')} / {q.get('limit', '?')} {q.get('unit', '')}"
                        post(lambda: quota.set(text + (f"，{q['resets_at']} 重置" if q.get("resets_at") else "")))
                    except Exception as e:  # the dialog stays usable without the server
                        post(lambda e=e: quota.set(str(e)))
                threading.Thread(target=work, daemon=True).start()

        def run(fn, done):
            save()
            msg.set("请稍候…")

            def work():
                try:
                    result = fn()
                    post(lambda: (msg.set(done), refresh()))
                except Error as e:
                    post(lambda e=e: msg.set(f"✗ {e}"))
                except Exception as e:
                    post(lambda e=e: msg.set(f"✗ {type(e).__name__}: {e}"))
            threading.Thread(target=work, daemon=True).start()

        send.configure(command=lambda: run(lambda: k.get("account.request_code")(email.get()), "验证码已发送，请查收邮箱"))
        login.configure(command=lambda: run(lambda: k.get("account.verify_code")(email.get(), code.get()), "✓ 已登录"))
        google.configure(command=lambda: run(lambda: k.get("account.google")(), "✓ 已用 Google 账号登录"))
        out.configure(command=lambda: run(lambda: k.get("account.logout")(), "已退出登录"))
        refresh()

    menu = k.get("ui.menu.settings", None)
    if menu is not None:
        menu.add_command(label="账号…", command=dialog)
    k.provide("account.dialog", dialog)
