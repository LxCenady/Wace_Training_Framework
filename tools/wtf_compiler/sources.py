"""Local fingerprinted PDF assets, normalized extraction and bounded rendering."""
import hashlib
from pathlib import Path
import shutil
import uuid
import pymupdf
from .schema import require, region

MAX_BYTES = 128 * 1024 * 1024


class Assets:
    def __init__(self, root):
        self.root = Path(root).resolve() / 'assets'
        self.root.mkdir(parents=True, exist_ok=True)

    def path(self, sha):
        require(isinstance(sha, str) and len(sha) == 64 and all(c in '0123456789abcdef' for c in sha), 'Invalid source hash')
        path = self.root / (sha + '.pdf')
        require(path.resolve().is_relative_to(self.root), 'Asset escaped scope')
        return path

    def register(self, path):
        path = Path(path)
        require(path.is_file() and 0 < path.stat().st_size <= MAX_BYTES, 'PDF missing or too large')
        with path.open('rb') as stream:
            sha = hashlib.file_digest(stream, 'sha256').hexdigest()
        with pymupdf.open(path) as doc:
            require(not doc.needs_pass and 0 < len(doc) <= 2000, 'Unreadable, encrypted or oversized PDF')
            pages = len(doc)
        dest = self.path(sha)
        valid=False
        if dest.exists():
            with dest.open('rb') as stream:valid=hashlib.file_digest(stream,'sha256').hexdigest()==sha
        if not valid:
            temp = dest.with_suffix('.'+uuid.uuid4().hex+'.tmp')
            try:
                shutil.copyfile(path, temp)
                with temp.open('rb') as stream:
                    require(hashlib.file_digest(stream, 'sha256').hexdigest() == sha, 'Source changed during import')
                temp.replace(dest)
            finally:temp.unlink(missing_ok=True)
        return dict(sha256=sha, pages=pages)

    def bound(self, doc):
        path = self.path(doc['sha256'])
        if not path.is_file():
            return False
        with path.open('rb') as stream:
            if hashlib.file_digest(stream, 'sha256').hexdigest() != doc['sha256']:
                return False
        with pymupdf.open(path) as pdf:
            return not pdf.needs_pass and len(pdf) == doc['pages']

    def extract(self, doc, ref):
        region(ref, {doc['id']: doc})
        require(self.bound(doc), 'Source missing or hash differs')
        with pymupdf.open(self.path(doc['sha256'])) as pdf:
            page = pdf[ref['page']]
            a,b,c,d = ref['bbox'];w,h = page.rect.width,page.rect.height
            box = pymupdf.Rect(a*w,b*h,c*w,d*h)
            return page.get_text('text', clip=box * page.derotation_matrix).strip()

    def render(self, doc, ref, width=1200):
        region(ref, {doc['id']: doc})
        require(self.bound(doc), 'Source missing or hash differs')
        with pymupdf.open(self.path(doc['sha256'])) as pdf:
            page = pdf[ref['page']];a,b,c,d = ref['bbox'];w,h=page.rect.width,page.rect.height
            scale = min(2, max(200,min(int(width),2400))/max(w,h))
            raw = page.get_pixmap(matrix=pymupdf.Matrix(scale,scale), clip=pymupdf.Rect(a*w,b*h,c*w,d*h)).tobytes('png')
        if ref.get('rotate'):
            with pymupdf.open('png',raw) as image:
                raw=image[0].get_pixmap(matrix=pymupdf.Matrix(1,1).prerotate(ref['rotate'])).tobytes('png')
        return raw
