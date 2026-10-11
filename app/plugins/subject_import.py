"""Local subject-pack import dialog. Validate before confirmation; then return to the wizard."""
from pathlib import Path
from tkinter import filedialog, messagebox
import pack


def setup(k):
    def import_pack():
        file = filedialog.askopenfilename(title='导入学科包', filetypes=[('WTF subject pack', '*.wtfpack')])
        if not file:
            return
        try:
            version = Path(__file__).resolve().parents[1] / 'version.txt'
            app_version = version.read_text(encoding='utf-8').strip() if version.exists() else '1.8.0'
            profile, _ = pack.inspect(file, app_version)
            subject = profile['subject']
            current = Path(k.root) / subject / 'pack.json'
            detail = f"{profile['name']['zh']} · {profile['version']}\n"
            detail += '这是本地学科包，来源未经官方索引验证。是否导入？'
            if profile.get('quality') == 'draft':
                detail += '\n此包尚未通过完整学科验收，仅用于本地测试。'
            if current.exists():
                import json
                old = json.loads(current.read_text(encoding='utf-8'))
                detail += f"\n将替换已安装版本：{old.get('version', '?')} → {profile['version']}"
            if not messagebox.askyesno('确认导入学科包', detail):
                return
            pack.install(file, k.root, overwrite=current.exists(), app_version=app_version)
            cfg = k.get('config')
            active = cfg.get('subjects')
            if active is None:
                import fetch
                active = [s for s in fetch.subjects(k.root) if any(
                    fetch.is_pdf(Path(k.root) / row[0]) for row in fetch.sources(k.root, [s]))]
            cfg['subjects'] = list(dict.fromkeys([*active, subject]))
            k.get('config.save')()
            k.get('subjects.manage')()
        except Exception as error:
            messagebox.showerror('学科包导入失败', str(error))
    k.provide('subjects.import', import_pack)
