"""Source-preserving PDF exports and images for installed question snapshots."""
import pymupdf
from .schema import require


def images(assets,snapshot,answers=False):
    sources={s['id']:s for s in snapshot['sources']};q=snapshot['question']
    refs=q['key_source'] if answers else q.get('shared_source',[])+q['source']
    return [assets.render(sources[r['document']],r) for r in refs]


def export(assets,snapshots,target,answers=False):
    require(bool(snapshots),'Select at least one question')
    out=pymupdf.open()
    try:
        for snap in snapshots:
            q=snap['question'];sources={s['id']:s for s in snap['sources']}
            for ref in q['key_source'] if answers else q.get('shared_source',[])+q['source']:
                doc=sources[ref['document']];require(assets.bound(doc),'Missing original PDF')
                with pymupdf.open(assets.path(doc['sha256'])) as src:
                    page=src[ref['page']];a,b,c,d=ref['bbox'];w,h=page.rect.width,page.rect.height
                    box=pymupdf.Rect(a*w,b*h,c*w,d*h)*page.derotation_matrix
                    rotate=(page.rotation+ref.get('rotate',0))%360
                    # show_pdf_page rotates counter-clockwise, while displayed PDF rotation is clockwise.
                    # Normalize the in-memory source page first so its /Rotate is not applied twice.
                    page.set_rotation(0)
                    dw,dh=box.width,box.height
                    if rotate in (90,270):dw,dh=dh,dw
                    dest=out.new_page(width=dw,height=dh)
                    dest.show_pdf_page(dest.rect,src,ref['page'],clip=box,rotate=(-rotate)%360)
        out.save(target)
    finally:out.close()
    return str(target)
