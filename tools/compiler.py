"""Local Compiler CLI. JSON files/stdin are data; stdio MCP is scoped to one project."""
import argparse
import json
from pathlib import Path
import sys
from wtf_compiler.service import Compiler


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',required=True,help='Independent Compiler data directory')
    parser.add_argument('action',choices=['list','create','status','task','submit','review','bind','import','build','export','mcp'])
    parser.add_argument('--project');parser.add_argument('--file');parser.add_argument('--decision',choices=['accept','retry'])
    parser.add_argument('--note');args=parser.parse_args();c=Compiler(args.root)
    def payload():
        return json.loads(Path(args.file).read_text(encoding='utf-8') if args.file else sys.stdin.read())
    if args.action=='mcp':
        from wtf_compiler.mcp import server
        server(c,args.project).run(transport='stdio');return
    actions={'list':c.projects.list,'create':lambda:c.projects.create(**payload()),
             'status':lambda:c.status(args.project),'task':lambda:c.projects.task(args.project),
             'submit':lambda:c.projects.submit(args.project,**payload()),
             'review':lambda:c.projects.resolve(args.project,args.decision,args.note),
             'bind':lambda:c.bind(args.project,args.file),'import':lambda:c.library.import_pack(args.file),
             'build':lambda:c.library.build(args.project),'export':lambda:c.export(args.project,args.file)}
    print(json.dumps(actions[args.action](),ensure_ascii=False,indent=2))


if __name__=='__main__':main()
