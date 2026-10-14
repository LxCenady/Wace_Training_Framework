"""Open the actual Tk Compiler workbench in an isolated empty data root."""
from pathlib import Path
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'app'),str(ROOT/'tools')]
from tests.safe_runtime import isolate
isolate()
from kernel import Kernel


def main():
    output=ROOT/'evidence/runtime/compiler-regression';output.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output,prefix='ui-') as temp:
        from plugins import config
        original=config.load
        config.load=lambda:dict(original(),language='en',provider='mock')
        k=Kernel(temp);k.load(['config','edition','i18n','ui_shell','compiler','ui_compiler'])
        root=k.get('ui.root');k.get('compiler.open')()
        for _ in range(10):root.update();time.sleep(.03)
        compiler=next(c for c in root.winfo_children() if c.winfo_class()=='Toplevel')
        import re
        found=[]
        def scan(w):
            try:
                text=w.cget('text')
                if re.search('[一-鿿]',str(text)):found.append(str(text))
            except Exception:pass
            if w.winfo_class()=='TNotebook':
                for tab in w.tabs():
                    if re.search('[一-鿿]',w.tab(tab,'text')):found.append(w.tab(tab,'text'))
            for child in w.winfo_children():scan(child)
        scan(compiler);assert not found,found
        assert k.get('compiler.calls')['compiler_list']()==[]
        assert not (Path(temp)/'generated.db').exists()
        root.destroy()
    print('Compiler Tk workbench: 0 CJK, isolated data, no model calls')


if __name__=='__main__':main()
