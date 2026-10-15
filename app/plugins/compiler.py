"""Shared local Compiler services, loaded lazily and independent of account/LLM."""
from pathlib import Path


CALL_NAMES = frozenset(('compiler_list','compiler_create','compiler_status','compiler_task','compiler_submit',
    'compiler_review','compiler_restart','compiler_bind','compiler_import','compiler_build','compiler_export',
    'compiler_preview','compiler_installed','compiler_questions','compiler_question','compiler_pdf','compiler_grade',
    'compiler_activate','compiler_install','compiler_mcp_enable','compiler_mcp_disable','compiler_mcp_info','compiler_download','compiler_practice','compiler_pick','compiler_profile','compiler_versions'))


def setup(k):
    instance=[];session=[]
    data_root=k.get('compiler.data_root',Path(k.root)/'compiler')
    def get():
        if not instance:
            from wtf_compiler.service import Compiler
            instance.append(Compiler(data_root))
        return instance[0]
    def mcp():
        if not session:
            from wtf_compiler.mcp import Session
            session.append(Session(get()))
        return session[0]
    def pick(kind='pdf',save=False):
        if kind not in ('pdf','pack') or type(save)is not bool:raise ValueError('Invalid file picker')
        import plat
        return plat.pick_files(kind,save)
    calls=dict(compiler_pick=pick,compiler_list=lambda:get().projects.list(),compiler_create=lambda course,documents:get().projects.create(course,documents),
        compiler_status=lambda pid:get().status(pid),compiler_task=lambda pid:get().projects.task(pid),
        compiler_submit=lambda pid,task,revision,output:get().projects.submit(pid,task,revision,output),
        compiler_review=lambda pid,decision,note:get().projects.resolve(pid,decision,note),
        compiler_download=lambda pid,document:get().download(pid,document),
        compiler_restart=lambda pid,stage,note:get().restart(pid,stage,note),compiler_bind=lambda pid,path:get().bind(pid,path),
        compiler_import=lambda path:get().library.import_pack(path),compiler_install=lambda path,folder=None:get().install(path,folder),compiler_build=lambda pid:get().library.build(pid),
        compiler_export=lambda pid,path=None:get().export(pid,path),compiler_preview=lambda pid,ref:get().preview(pid,ref),
        compiler_installed=lambda:get().library.list(),compiler_questions=lambda pack,text='',codes=None:get().library.questions(pack,text,codes=codes),
        compiler_profile=lambda pack:get().library.profile(pack),compiler_versions=lambda pack:get().library.versions(pack),
        compiler_question=lambda pack,qid,version=None:get().question(pack,qid,version),compiler_pdf=lambda pack,qids,path,answers=False:get().export_questions(pack,qids,path,answers),
        compiler_grade=lambda pack,qid,proposals,evidence_count:get().grade(pack,qid,proposals,evidence_count),
        compiler_practice=lambda pack,qid,credits,conditions=None:get().practice(pack,qid,credits,conditions),
        compiler_activate=lambda pack,version:get().library.activate(pack,version),compiler_mcp_enable=lambda pid:mcp().enable(pid),
        compiler_mcp_disable=lambda:mcp().disable(),compiler_mcp_info=lambda:mcp().state.copy())
    k.provide('compiler',get)
    def marking():
        from wtf_compiler import marking as adapter
        return adapter
    k.provide('compiler.assignment.snapshot',lambda pack,qid,version=None:marking().snapshot(get().library,pack,qid,version))
    k.provide('compiler.assignment.score_rows',lambda item,value:marking().score_rows(item,value))
    k.provide('compiler.calls',calls)
    k.provide('compiler.public_calls',CALL_NAMES)
    k.provide('web.calls.compiler',calls)
    k.on('ui.closed',lambda:session and session[0].disable())
