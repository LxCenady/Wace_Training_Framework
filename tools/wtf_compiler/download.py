"""Explicit user-selected HTTPS source downloads; verify before binding."""
import hashlib
import ipaddress
import socket
import uuid
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from .schema import require, url
from .sources import MAX_BYTES


def public_url(value):
    url(value);host=urlsplit(value).hostname
    require(all(ipaddress.ip_address(row[4][0]).is_global for row in socket.getaddrinfo(host,443,type=socket.SOCK_STREAM)), 'Download URL must resolve to a public address')


class Redirects(HTTPRedirectHandler):
    def redirect_request(self,request,fp,code,message,headers,newurl):
        public_url(newurl)
        return super().redirect_request(request,fp,code,message,headers,newurl)


def bind(assets,doc):
    require(bool(doc.get('url')),'No download URL for this source');public_url(doc['url'])
    temp=assets.root/(uuid.uuid4().hex+'.download')
    try:
        with build_opener(Redirects()).open(Request(doc['url'],headers={'User-Agent':'WTF-Compiler/0.1'}),timeout=30) as response, temp.open('wb') as f:
            size=0;sha=hashlib.sha256()
            while data:=response.read(64*1024):
                size+=len(data);require(size<=MAX_BYTES,'Downloaded source too large');sha.update(data);f.write(data)
        require(sha.hexdigest()==doc['sha256'],'Downloaded PDF hash differs')
        info=assets.register(temp);require(info['pages']==doc['pages'],'Downloaded PDF page count differs')
    finally:temp.unlink(missing_ok=True)
