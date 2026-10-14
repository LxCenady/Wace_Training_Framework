"""Reviewed English fragments for the Compiler workbench; no model call needed."""
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
translations={
    '记录自评分':'Record self assessment','保存自评分':'Save self assessment',
    '进度与复核':'Progress and review','外部代理任务':'External agent task',
    '制作学科包请连接自己的':'To build a subject pack, connect your own ',
    '不使用订阅额度或内置模型。':' uses neither subscription credits nor built-in models.',
    '请先选择制作项目':'Select a Compiler project first','制作学科包':'Build a subject pack',
    '学科名称':'Course name','学科':'Course ','（字母、数字、短横线）':' (letters, digits, hyphens)',
    '选择评分标准':'Select marking key ','选择大纲':'Select syllabus ',
    '当前没有等待提交的任务':'No task awaiting submission','选择代理输出':'Select agent output ',
    '疑难复核':'Review uncertain results','填写复核理由':'Enter your review explanation',
    '绑定原始':'Bind original ','独立学科包':'Independent subject packs','导出题目':'Export question ',
    '新建项目':'New project','导入配方包':'Import recipe pack','刷新':'Refresh','绑定':'Bind ',
    '提交代理结果':'Submit agent result','认可疑难项':'Accept reviewed result','退回重做':'Request retry',
    '建库并激活':'Build and activate','导出配方包':'Export recipe pack','连接':'Connect ','关闭':'Close ',
    '浏览学科包':'Browse subject packs','测试':'Test','原创技巧。':'Original guidance.',
    '默认是':'Default: ','官方服务器；学校自建的服务器可在这里改。登录后':' official server; set your school server here. After signing in, ',
    '，按套餐的每日额度使用。':', using your plan\'s daily allowance.',
}
path=root/'app/i18n/en.json';table=json.loads(path.read_text(encoding='utf-8'));table.update(translations)
path.write_text(json.dumps(table,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Reviewed',len(translations),'fragments')
