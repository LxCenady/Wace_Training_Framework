"""Manual PDF rectangle picker for external question/answer crops."""
import base64
import tkinter as tk
from tkinter import ttk


def setup(k):
    def open_crop(path, regions, save):
        pages = k.get("external.pdf.inspect")(path)
        dlg = tk.Toplevel(k.get("ui.root"))
        dlg.title("外源切块：拖动框选，跨页可添加多个区域")
        dlg.transient(k.get("ui.root"))
        picked = [list(r) for r in regions]
        state = dict(page=regions[0][0] if regions else 0, start=None, image=None, rect=None)
        bar = ttk.Frame(dlg, padding=6)
        bar.pack(fill="x")
        ttk.Button(bar, text="上一页", command=lambda: turn(-1)).pack(side="left")
        ttk.Button(bar, text="下一页", command=lambda: turn(1)).pack(side="left")
        count = ttk.Label(bar)
        count.pack(side="left", padx=8)
        ttk.Label(dlg, text="在原件上拖动框选；松开鼠标即添加切块。原始 PDF 坐标自动保存。", wraplength=620).pack(padx=8)
        canvas = tk.Canvas(dlg, background="#ffffff", highlightthickness=0)
        canvas.pack(padx=8, pady=4)
        listing = tk.Listbox(dlg, height=4, exportselection=False)
        listing.pack(fill="x", padx=8)
        foot = ttk.Frame(dlg, padding=8)
        foot.pack(fill="x")

        def refresh():
            listing.delete(0, "end")
            for p, x0, y0, x1, y1 in picked:
                listing.insert("end", f"{p + 1} : ({x0:.1f}, {y0:.1f}) – ({x1:.1f}, {y1:.1f})")

        def draw():
            x0, y0, x1, y1 = pages[state["page"]]
            width, height = x1 - x0, y1 - y0
            zoom = min(680 / width, max(220, dlg.winfo_screenheight() - 350) / height)
            state.update(zoom=zoom, start=None, rect=None)
            png = k.get("external.pdf.render")(path, state["page"], zoom=zoom)
            state["image"] = tk.PhotoImage(data=base64.b64encode(png))
            canvas.configure(width=state["image"].width(), height=state["image"].height())
            canvas.delete("all")
            canvas.create_image(0, 0, image=state["image"], anchor="nw")
            for p, a, b, c, d in picked:
                if p == state["page"]:
                    canvas.create_rectangle((a-x0)*zoom, (b-y0)*zoom, (c-x0)*zoom, (d-y0)*zoom, outline="#2f6b3a", width=2)
            count.configure(text=f"{state['page'] + 1} / {len(pages)}")

        def turn(delta):
            state["page"] = max(0, min(len(pages) - 1, state["page"] + delta))
            draw()

        def position(e):
            return max(0, min(e.x, state["image"].width())), max(0, min(e.y, state["image"].height()))

        def press(e):
            state["start"] = position(e)
            state["rect"] = canvas.create_rectangle(*state["start"], *state["start"], outline="#1f3a73", width=2)

        def drag(e):
            if state["start"]:
                canvas.coords(state["rect"], *state["start"], *position(e))

        def release(e):
            if not state["start"]:
                return
            a, b = state["start"]
            c, d = position(e)
            x0, y0, x1, y1 = pages[state["page"]]
            z = state["zoom"]
            if abs(c-a) > 3 and abs(d-b) > 3:
                picked.append([state["page"], max(x0, x0+min(a,c)/z), max(y0, y0+min(b,d)/z),
                               min(x1, x0+max(a,c)/z), min(y1, y0+max(b,d)/z)])
            refresh()
            draw()

        def remove():
            for index in reversed(listing.curselection()):
                picked.pop(index)
            refresh()
            draw()

        def done():
            save(picked)
            dlg.destroy()

        ttk.Button(foot, text="删除选中区域", command=remove).pack(side="left")
        ttk.Button(foot, text="应用切块", style="Accent.TButton", command=done).pack(side="right")
        ttk.Button(foot, text="取消", command=dlg.destroy).pack(side="right", padx=6)
        canvas.bind("<ButtonPress-1>", press)
        canvas.bind("<B1-Motion>", drag)
        canvas.bind("<ButtonRelease-1>", release)
        refresh()
        draw()
        return dlg

    k.provide("external.crop.open", open_crop)
