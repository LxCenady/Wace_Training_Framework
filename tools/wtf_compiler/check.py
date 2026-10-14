"""Small packaged-runtime check using self-authored PDFs and temporary data only."""
import asyncio
from pathlib import Path
import tempfile
import pymupdf
from .service import Compiler
from .mcp import server


def run():
    from mcp.client.streamable_http import streamable_http_client
    import uvicorn
    with tempfile.TemporaryDirectory(prefix='wtf-compiler-selftest-') as folder:
        root=Path(folder);documents=[]
        for role in ('exam','key','syllabus'):
            path=root/(role+'.pdf')
            with pymupdf.open() as pdf:
                pdf.new_page().insert_text((40,50),'Synthetic Compiler '+role)
                pdf.save(path)
            documents.append(dict(path=str(path),roles=[role]))
        compiler=Compiler(root/'data')
        project=compiler.projects.create(dict(id='selftest',name={'zh':'selftest','en':'selftest'}),documents)
        mcp=server(compiler,project['id'])
        tools=asyncio.run(mcp.list_tools())
        assert 'compiler.submit_parse_chunk' in {t.name for t in tools}
        image=compiler.projects.resource(project['id'],dict(document='d1',page=0,bbox=[0,0,1,1]),True)
        assert image.startswith(b'\x89PNG')
        return f'protocol 2, {len(tools)} MCP tools, temporary library and PDF rendering'
