"""Opt-in project-scoped MCP. No filesystem browsing, model calls or human approval."""
import secrets
import socket
import threading
from .schema import require


def server(compiler,pid,active=lambda:True):
    from mcp.server.fastmcp import FastMCP, Image
    compiler.projects.get(pid)
    mcp=FastMCP('WTF Compiler',host='127.0.0.1',stateless_http=True,json_response=True)

    def check():
        require(active(),'Compiler session is disabled')

    @mcp.tool(name='compiler.get_task')
    def task()->dict:
        check();return compiler.projects.task(pid) or {'available':False,'status':compiler.status(pid),'instructions':'No agent task is active. Do not submit or approve; report the current state to the user.'}

    @mcp.tool(name='compiler.status')
    def status()->dict:
        check();return compiler.status(pid)

    @mcp.tool(name='compiler.read_text')
    def text(document:str,page:int,bbox:list[float])->str:
        check();return compiler.projects.resource(pid,dict(document=document,page=page,bbox=bbox))

    @mcp.tool(name='compiler.read_image')
    def image(document:str,page:int,bbox:list[float],rotate:int=0)->Image:
        check();return Image(data=compiler.projects.resource(pid,dict(document=document,page=page,bbox=bbox,rotate=rotate),True),format='png')

    @mcp.tool(name='compiler.submit_result')
    def submit(task_id:str,revision:int,result:dict)->dict:
        check();return compiler.projects.submit(pid,task_id,revision,result)

    @mcp.tool(name='compiler.validate')
    def validate()->dict:
        check();recipe,_=compiler.projects.finalized(pid)
        return dict(valid=True,questions=len(recipe['questions']))

    @mcp.tool(name='compiler.submit_parse_chunk')
    def parse_chunk(task_id:str,revision:int,exam_id:str,result:dict)->dict:
        check();return compiler.projects.parse_chunk(pid,task_id,revision,exam_id,result)

    @mcp.tool(name='compiler.build')
    def build()->dict:
        check();return compiler.library.build(pid)

    @mcp.tool(name='compiler.export')
    def export()->dict:
        check();return {'path':compiler.export(pid)}

    return mcp


class Session:
    def __init__(self,compiler):
        self.compiler=compiler;self.state={'enabled':False};self.server=None;self.lock=threading.Lock()

    def enable(self,pid):
        with self.lock:
            require(self.server is None,'Disable the current session first')
            token=secrets.token_urlsafe(32);sock=socket.socket();sock.bind(('127.0.0.1',0))
            port=sock.getsockname()[1];origin=f'http://127.0.0.1:{port}'
            mcp=server(self.compiler,pid,lambda:self.state.get('enabled') and self.state.get('token')==token)
            app=mcp.streamable_http_app()

            async def protected(scope,receive,send):
                if scope['type']=='http':
                    headers={k.decode().lower():v.decode() for k,v in scope['headers']}
                    allowed=(self.state.get('enabled') and self.state.get('token')==token and
                             headers.get('host')==f'127.0.0.1:{port}' and headers.get('origin',origin)==origin and
                             secrets.compare_digest(headers.get('authorization',''),'Bearer '+token))
                    if not allowed:
                        await send({'type':'http.response.start','status':403,'headers':[]})
                        await send({'type':'http.response.body','body':b'Forbidden'});return
                    size=0
                    original_receive=receive
                    async def bounded_receive():
                        nonlocal size
                        message=await original_receive();size+=len(message.get('body',b''))
                        require(size<=16*1024*1024,'Request too large')
                        return message
                    receive=bounded_receive
                await app(scope,receive,send)

            import uvicorn
            self.server=uvicorn.Server(uvicorn.Config(protected,host='127.0.0.1',port=port,log_level='error',access_log=False))
            self.state=dict(enabled=True,project_id=pid,url=origin+'/mcp',token=token)
            threading.Thread(target=self.server.run,kwargs={'sockets':[sock]},daemon=True).start()
            return self.state.copy()

    def disable(self):
        with self.lock:
            if self.server:self.server.should_exit=True
            self.server=None;self.state={'enabled':False}
            return self.state.copy()
