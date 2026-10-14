"""Tk workbench for local projects and independently installed recipe packs."""
import json
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox


def setup(k):
    calls=k.get('compiler.calls');root=k.get('ui.root')
    def open_workbench():
        window=tk.Toplevel(root);window.title('WTF Compiler');window.geometry('1000x760')
        bar=ttk.Frame(window);bar.pack(fill='x')
        body=ttk.PanedWindow(window,orient='horizontal');body.pack(fill='both',expand=True)
        left=ttk.Frame(body);right=ttk.Frame(body);body.add(left,weight=1);body.add(right,weight=3)
        listing=tk.Listbox(left);listing.pack(fill='both',expand=True)
        tabs=ttk.Notebook(right);tabs.pack(fill='both',expand=True)
        progress=tk.Text(tabs,wrap='word');taskbox=tk.Text(tabs,wrap='none')
        tabs.add(progress,text='进度与复核');tabs.add(taskbox,text='外部代理任务')
        rows=[];selected=[None]
        ttk.Label(window,text='制作学科包请连接自己的 agent；Compiler 不使用订阅额度或内置模型。',wraplength=950).pack(fill='x',padx=10,pady=6)

        def invoke(fn):
            try:fn()
            except Exception as exc:messagebox.showerror('Compiler',str(exc),parent=window)

        def pid():
            if not selected[0]:raise ValueError('请先选择制作项目')
            return selected[0]

        def show():
            state=calls['compiler_status'](pid());task=calls['compiler_task'](pid())
            progress.delete('1.0','end');progress.insert('end',json.dumps(state,ensure_ascii=False,indent=2))
            taskbox.delete('1.0','end');taskbox.insert('end',json.dumps(task,ensure_ascii=False,indent=2))

        def refresh():
            rows[:]=calls['compiler_list']();listing.delete(0,'end')
            for row in rows:listing.insert('end',f"{next(iter(row['course']['name'].values()))} · {row['stage']} · {row['state']}")
            if selected[0]:show()

        def select(event):
            if listing.curselection():selected[0]=rows[listing.curselection()[0]]['id'];invoke(show)
        listing.bind('<<ListboxSelect>>',select)

        def create():
            name=simpledialog.askstring('制作学科包','学科名称',parent=window)
            if not name:return
            code=simpledialog.askstring('制作学科包','学科 ID（字母、数字、短横线）',parent=window)
            if not code:return
            docs=[]
            for role,title in [('exam','选择试卷 PDF'),('key','选择评分标准 PDF'),('syllabus','选择大纲 PDF')]:
                files=filedialog.askopenfilenames(title=title,filetypes=[('PDF','*.pdf')],parent=window)
                if not files:return
                docs.extend(dict(path=f,roles=[role]) for f in files)
            selected[0]=calls['compiler_create']({'id':code,'name':{'zh':name,'en':name}},docs)['id'];refresh()

        def import_pack():
            path=filedialog.askopenfilename(filetypes=[('WTF recipe','*.wtfpack')],parent=window)
            if path:selected[0]=calls['compiler_import'](path)['id'];refresh()

        def submit():
            task=calls['compiler_task'](pid())
            if not task:raise ValueError('当前没有等待提交的任务')
            path=filedialog.askopenfilename(title='选择代理输出 JSON',filetypes=[('JSON','*.json')],parent=window)
            if path:
                with open(path,encoding='utf-8') as f:output=json.load(f)
                calls['compiler_submit'](pid(),task['task_id'],task['revision'],output);refresh()

        def review(decision):
            note=simpledialog.askstring('疑难复核','填写复核理由',parent=window)
            if note:calls['compiler_review'](pid(),decision,note);refresh()

        def bind():
            for path in filedialog.askopenfilenames(title='绑定原始 PDF',filetypes=[('PDF','*.pdf')],parent=window):calls['compiler_bind'](pid(),path)
            refresh()

        def export():
            path=filedialog.asksaveasfilename(defaultextension='.wtfpack',filetypes=[('WTF recipe','*.wtfpack')],parent=window)
            if path:calls['compiler_export'](pid(),path)

        def enable():
            state=calls['compiler_mcp_enable'](pid())
            value=json.dumps({'url':state['url'],'headers':{'Authorization':'Bearer '+state['token']}},indent=2)
            taskbox.delete('1.0','end');taskbox.insert('end',value);tabs.select(taskbox)
            window.clipboard_clear();window.clipboard_append(value)

        def browse():
            installed=calls['compiler_installed']()
            page=ttk.Frame(tabs);tabs.add(page,text='独立学科包');tabs.select(page)
            packs=ttk.Combobox(page,state='readonly',values=[next(iter(p['course']['name'].values())) for p in installed]);packs.pack(fill='x')
            query=tk.StringVar();ttk.Entry(page,textvariable=query).pack(fill='x')
            tags=ttk.Combobox(page,state='readonly');tags.pack(fill='x');tagrows=[]
            questions=tk.Listbox(page);questions.pack(fill='x');viewer=tk.Text(page,wrap='word');viewer.pack(fill='both',expand=True)
            qrows=[];images=[]
            def load(event=None):
                pack=installed[packs.current()]['pack_id']
                qrows[:]=calls['compiler_questions'](pack,query.get(),[tagrows[tags.current()-1]['id']] if tags.current()>0 else []);questions.delete(0,'end')
                for q in qrows:questions.insert('end',f"{q['label']} · {q['marks']}")
            def choose_pack(event=None):
                taxonomy=calls['compiler_profile'](installed[packs.current()]['pack_id'])['taxonomy']
                tagrows[:]=taxonomy['knowledge']+taxonomy['patterns'];tags['values']=['全部']+[v['id']+' · '+v['name'] for v in tagrows];tags.current(0);load()
            def view(event=None):
                if not questions.curselection():return
                import base64
                snap=calls['compiler_question'](installed[packs.current()]['pack_id'],qrows[questions.curselection()[0]]['id'])
                viewer.delete('1.0','end');images.clear()
                for data in snap['images']:
                    image=tk.PhotoImage(data=base64.b64decode(data.split(',',1)[1]));images.append(image)
                    viewer.image_create('end',image=image);viewer.insert('end','\n')
                viewer.insert('end',snap['content']['solution'])
            def export_pdf():
                if not questions.curselection():return
                path=filedialog.asksaveasfilename(defaultextension='.pdf',parent=window)
                if path:calls['compiler_pdf'](installed[packs.current()]['pack_id'],[qrows[questions.curselection()[0]]['id']],path)
            def practice():
                if not questions.curselection():return
                pack=installed[packs.current()]['pack_id'];qid=qrows[questions.curselection()[0]]['id']
                snap=calls['compiler_question'](pack,qid);form=tk.Toplevel(window);form.title('记录自评分');values={};conditions={}
                def visit(node,part):
                    if node['kind']=='award':
                        ttk.Label(form,text=snap['content']['criteria'][node['id']]).pack(anchor='w')
                        var=tk.StringVar(value='0');values[node['id']]=var
                        if node.get('levels'):
                            ttk.Combobox(form,textvariable=var,state='readonly',values=sorted({0,*[v['score'] for v in node['levels']]})).pack(fill='x')
                        else:ttk.Spinbox(form,from_=0,to=node['max_marks'],increment=node.get('credit_step',1),textvariable=var).pack(fill='x')
                    for ident in node.get('conditions',[])+[c['condition'] for c in node.get('conditional_caps',[])]:
                        if ident in conditions.setdefault(part,{}):continue
                        ttk.Label(form,text=ident).pack(anchor='w');var=tk.StringVar(value='?');conditions[part][ident]=var
                        ttk.Combobox(form,textvariable=var,state='readonly',values=['?','True','False']).pack(fill='x')
                    for child in node.get('children',[]):visit(child,part)
                for part in snap['question']['parts']:visit(part['rubric'],part['id'])
                def save():
                    result=calls['compiler_practice'](pack,qid,{i:float(v.get()) for i,v in values.items()},
                        {p:{i:None if v.get()=='?' else v.get()=='True' for i,v in rows.items()} for p,rows in conditions.items()})
                    messagebox.showinfo('记录自评分',f"{result['earned']} / {result['possible']}",parent=form);form.destroy()
                ttk.Button(form,text='保存自评分',command=lambda:invoke(save)).pack()
            packs.bind('<<ComboboxSelected>>',lambda e:invoke(choose_pack));tags.bind('<<ComboboxSelected>>',lambda e:invoke(load))
            query.trace_add('write',lambda *args:invoke(load) if packs.current()>=0 else None)
            questions.bind('<<ListboxSelect>>',lambda e:invoke(view))
            ttk.Button(page,text='导出题目 PDF',command=lambda:invoke(export_pdf)).pack()
            ttk.Button(page,text='记录自评分',command=lambda:invoke(practice)).pack()
            if installed:packs.current(0);choose_pack()

        actions=[('新建项目',create),('导入配方包',import_pack),('刷新',refresh),('绑定 PDF',bind),('提交代理结果',submit),
                 ('认可疑难项',lambda:review('accept')),('退回重做',lambda:review('retry')),('建库并激活',lambda:calls['compiler_build'](pid())),
                 ('导出配方包',export),('连接 MCP',enable),('关闭 MCP',calls['compiler_mcp_disable']),('浏览学科包',browse)]
        for i,(text,fn) in enumerate(actions):ttk.Button(bar,text=text,command=lambda f=fn:invoke(f)).grid(row=i//6,column=i%6,sticky='ew')
        window.protocol('WM_DELETE_WINDOW',lambda:(calls['compiler_mcp_disable'](),window.destroy()))
        refresh()
    k.provide('compiler.open',open_workbench)
    k.get('ui.menu').add_command(label='WTF Compiler',command=open_workbench)
