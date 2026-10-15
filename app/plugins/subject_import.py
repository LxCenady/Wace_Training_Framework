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
            if profile.get('wtf_pack')==2:  # a recipe pack: installed from the originals the user points at
                import plat
                folder = plat.pick_folder('选择这门课原卷 PDF 所在的文件夹')
                result = k.get('compiler.calls')['compiler_install'](file, folder)
                built = result.get('built') or {}
                if built.get('subject') and not built.get('error'):
                    messagebox.showinfo('学科包已安装', f"{built['subject']} 已安装：{built['questions']} 道题。重启 WTF 后出现在知识树。")
                else:
                    messagebox.showwarning('还缺原卷', f"那个文件夹里没有找到 {len(result.get('missing', []))} 份原卷：请在 WTF Compiler 里绑定。")
                    k.get('compiler.open')()
                return
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
