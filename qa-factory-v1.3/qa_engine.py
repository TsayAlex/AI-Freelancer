"""ALEX AI QA Factory: evidence-oriented safe, dependency-free scanning core.
No uploaded project source is executed; browser preview is opt-in, locally sandboxed.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import html
from html.parser import HTMLParser
import http.client
import ipaddress
import io
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import shutil
import socket
import ssl
import subprocess
import tempfile
import uuid
import zipfile
from urllib.parse import urlsplit, urljoin, unquote, urldefrag

MAX_ZIP_BYTES = 25 * 1024 * 1024
MAX_TOTAL_UNCOMPRESSED = 90 * 1024 * 1024
MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_ENTRIES = 1500
MAX_HTML_PAGES = 12
SOURCE_EXT = {'.html', '.htm', '.js', '.mjs', '.cjs', '.jsx', '.ts', '.tsx', '.css', '.json', '.txt', '.md', '.yml', '.yaml', '.xml', '.svg', '.webmanifest'}
PREVIEW_EXT = SOURCE_EXT | {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.ico', '.woff', '.woff2', '.ttf', '.webm', '.mp3', '.mp4'}
SEVERITIES = ('critical', 'major', 'minor', 'info')

class ScanError(Exception):
    pass

class DocParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.elements=[]; self.links=[]; self.images=[]; self.resources=[]; self.forms=[]; self.inputs=[]; self.labels=[]; self.headings=[]; self.has_title=False; self.title_text=''; self.in_title=False
        self.meta=[]; self.html_attrs={}; self.ids=set()
    def handle_starttag(self, tag, attrs):
        a=dict(attrs); line=self.getpos()[0]
        if tag=='html': self.html_attrs=a
        if a.get('id'): self.ids.add(a['id'])
        if tag=='title': self.has_title=True; self.in_title=True
        if tag=='meta': self.meta.append(a)
        if tag=='a': self.links.append((a,line))
        if tag=='img': self.images.append((a,line))
        if tag in ('script','link','source','iframe'):
            k='src' if tag in ('script','source','iframe') else 'href'
            if a.get(k): self.resources.append((a[k],line,tag))
        if tag=='form': self.forms.append((a,line))
        if tag in ('input','textarea','select'): self.inputs.append((a,line,tag))
        if tag=='label': self.labels.append((a,line))
        if tag in ('h1','h2','h3'): self.headings.append((tag,line))
    def handle_endtag(self,tag):
        if tag=='title': self.in_title=False
    def handle_data(self,data):
        if self.in_title: self.title_text+=data


def make_report(kind, name):
    return {'id':uuid.uuid4().hex[:12], 'kind':kind, 'name':name[:200],
            'started_at':dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'),
            'status':'COMPLETED', 'findings':[], 'checked':[], 'warnings':[], 'metrics':{},
            'evidence':[], 'disclaimer':'Automated checks are partial. Findings need human validation; no absence-of-bugs guarantee.'}

def add(report, code, severity, title, location, expected, actual, recommendation, evidence=None, confidence='high'):
    # Stable per-report dedup.
    key=(code,location,actual)
    for f in report['findings']:
        if (f['code'],f['location'],f['actual'])==key: return
    fid='BUG-'+str(len(report['findings'])+1).zfill(3)
    report['findings'].append({'id':fid,'code':code,'severity':severity,'title':title,'location':str(location)[:240],
      'expected':expected,'actual':str(actual)[:500], 'recommendation':recommendation,'confidence':confidence,
      'review':'candidate','evidence':evidence or []})

def safe_path(raw):
    raw=raw.replace('\\','/')
    if not raw or '\x00' in raw or raw.startswith('/') or re.match(r'^[A-Za-z]:',raw): return False
    p=PurePosixPath(raw)
    return '..' not in p.parts and len(raw)<=300

def normalize_local(doc, ref):
    if not ref or ref.startswith(('#','mailto:','tel:','data:','javascript:')): return None
    bits=urlsplit(ref)
    if bits.scheme or bits.netloc: return None
    local=unquote(bits.path)
    if not local: return None
    if local.startswith('/'):
        candidate=posixpath.normpath(local.lstrip('/'))
    else:
        candidate=posixpath.normpath(posixpath.join(posixpath.dirname(doc),local))
    if candidate=='..' or candidate.startswith('../'): return '__OUTSIDE__'
    return candidate

def scan_html(report, filename, content, present, is_remote=False):
    parser=DocParser()
    try: parser.feed(content)
    except Exception as e:
        add(report,'HTML_PARSE','major','HTML could not be parsed',filename,'Valid HTML',str(e),'Fix malformed HTML.')
        return
    report['checked'].append(filename)
    loc=lambda line: f'{filename}:{line}'
    if not parser.title_text.strip():
        add(report,'SEO_TITLE','minor','Page title missing',filename,'Nonempty <title> in head','No meaningful page title','Add a short, descriptive title.')
    if not any(x.get('name','').lower()=='viewport' for x in parser.meta):
        add(report,'MOBILE_VIEWPORT','major','Mobile viewport not declared',filename,'Viewport meta tag','Missing viewport meta','Add <meta name="viewport" content="width=device-width, initial-scale=1">.')
    if not parser.html_attrs.get('lang'):
        add(report,'LANG','minor','Page language missing',filename,'Language declared on <html>','No lang attribute','Set the main document language (en, ru, uk, etc.).')
    if not any(x.get('name','').lower()=='description' and x.get('content','').strip() for x in parser.meta):
        add(report,'SEO_DESCRIPTION','minor','Meta description missing',filename,'Useful page description','No description meta tag','Write a short description of this page.')
    if not any(tag=='h1' for tag,_ in parser.headings):
        add(report,'H1_MISSING','minor','Primary heading missing',filename,'A descriptive H1 heading','No H1 was found','Add one meaningful primary heading.')
    label_for={a.get('for') for a,_ in parser.labels if a.get('for')}
    for a,line in parser.images:
        if 'alt' not in a:
            add(report,'IMAGE_ALT','minor','Image has no alt attribute',loc(line),'alt attribute present','No alt attribute', 'Use meaningful alternative text; decorative images may use alt="".')
    for a,line,tag in parser.inputs:
        t=a.get('type','text').lower()
        if t in ('hidden','submit','button','reset','image'): continue
        if not (a.get('aria-label') or a.get('aria-labelledby') or a.get('title') or (a.get('id') in label_for)):
            # A wrapping <label> is not detected statically; flag as candidate for review.
            add(report,'INPUT_LABEL','minor','Field may lack accessible label',loc(line),'Accessible field name','No explicit label linkage / aria-label','Associate a label with the field, or verify an enclosing <label>.',confidence='medium')
        if ('email' in (a.get('name','')+' '+a.get('id','')).lower()) and t not in ('email','hidden'):
            add(report,'EMAIL_TYPE','minor','Email field uses non-email input type',loc(line),'type="email" for basic browser validation',f'type="{t}"','Use type="email" plus server-side validation.')
    for a,line in parser.links:
        if a.get('target','').lower()=='_blank' and not {'noopener','noreferrer'} & set(a.get('rel','').lower().split()):
            add(report,'TARGET_BLANK','minor','External tab missing rel protection',loc(line),'rel="noopener" for target="_blank"','rel does not include noopener','Add rel="noopener noreferrer".')
    if not is_remote:
        refs=[(a.get('href'),line,'link') for a,line in parser.links]
        refs += [(a.get('src'),line,'image') for a,line in parser.images]
        refs += parser.resources
        for ref,line,role in refs:
            candidate=normalize_local(filename,ref or '')
            if candidate=='__OUTSIDE__':
                add(report,'PATH_OUTSIDE','major','Local reference escapes project directory',loc(line),'Local project path',str(ref),'Correct the path; avoid ../ beyond the project root.')
            elif candidate:
                choices={candidate,candidate.rstrip('/')+'/index.html'}
                if not any(c in present for c in choices):
                    add(report,'BROKEN_REFERENCE','major','Missing local file referenced',loc(line),'Referenced file exists in ZIP',str(ref),f'Provide missing asset/page or correct path ({role}).')
            elif ref and ref.startswith('#') and ref[1:] and ref[1:] not in parser.ids:
                add(report,'BROKEN_ANCHOR','minor','Anchor target not found',loc(line),'An element matching the anchor ID',ref,'Create the target ID or fix the link.',confidence='medium')


def scan_zip_bytes(data, name='uploaded.zip', browser=False, on_browser=None):
    if len(data)>MAX_ZIP_BYTES: raise ScanError('ZIP exceeds 25 MB upload limit.')
    report=make_report('zip',name)
    try: zf=zipfile.ZipFile(io.BytesIO(data))
    except (zipfile.BadZipFile,ValueError): raise ScanError('Invalid ZIP archive.')
    with zf:
        entries=zf.infolist()
        if len(entries)>MAX_ENTRIES: raise ScanError('ZIP contains too many files (limit: 1500).')
        total=sum(x.file_size for x in entries)
        if total>MAX_TOTAL_UNCOMPRESSED: raise ScanError('Uncompressed ZIP exceeds 90 MB limit.')
        files={}; preview_files={}; skipped=0
        for i in entries:
            if i.is_dir(): continue
            if not safe_path(i.filename): raise ScanError('Unsafe ZIP path detected: '+i.filename[:100])
            # Reject symlinks (Unix mode).
            if (i.external_attr >> 16)&0o170000 == 0o120000: raise ScanError('ZIP symlink not permitted.')
            if i.flag_bits & 1: raise ScanError('Encrypted ZIP not supported.')
            if i.file_size>MAX_FILE_BYTES: skipped+=1; continue
            if i.file_size and i.compress_size and i.file_size / max(1,i.compress_size)>200: raise ScanError('Suspicious ZIP compression ratio.')
            suffix=Path(i.filename).suffix.lower()
            if suffix not in PREVIEW_EXT: skipped+=1; continue
            body=zf.read(i)
            if suffix in SOURCE_EXT:
                files[i.filename]=body.decode('utf-8',errors='replace')
            if suffix in PREVIEW_EXT:
                preview_files[i.filename]=body
        report['metrics']={'files_total':len([x for x in entries if not x.is_dir()]),'files_read':len(files),'files_skipped':skipped,'html_pages':sum(f.lower().endswith(('.html','.htm')) for f in files),'archive_kb':round(len(data)/1024,1)}
        if skipped: report['warnings'].append(f'{skipped} unsupported or large files were not analysed.')
        present=set(i.filename for i in entries if not i.is_dir())
        if not any(x.lower().endswith(('.html','.htm')) for x in files):
            report['warnings'].append('No built HTML pages found. Source-only frameworks need a separately built dist/ output for browser tests.')
        for filename,content in files.items():
            ext=Path(filename).suffix.lower()
            if ext in ('.html','.htm'): scan_html(report,filename,content,present)
            if ext=='.json':
                try: json.loads(content)
                except json.JSONDecodeError as e:
                    add(report,'INVALID_JSON','major','Invalid JSON syntax',f'{filename}:{e.lineno}','Valid JSON',e.msg,'Correct the JSON structure.')
                    report['checked'].append(filename)
            if ext in ('.js','.mjs','.cjs'):
                if shutil.which('node'):
                    with tempfile.TemporaryDirectory() as td:
                        path=Path(td)/('check'+ext);path.write_text(content,encoding='utf-8')
                        try:
                            checked=subprocess.run(['node','--check',str(path)],capture_output=True,text=True,timeout=4)
                            if checked.returncode:
                                add(report,'JS_SYNTAX','major','JavaScript syntax check failed',filename,'JavaScript parses successfully',checked.stderr[-250:],'Review syntax near indicated error.')
                            report['checked'].append(filename+' [node --check]')
                        except (OSError, subprocess.TimeoutExpired): report['warnings'].append(f'Could not syntax-check {filename}.')
            if re.search(r'(?i)(secret|token|api[_-]?key)',filename) and Path(filename).name.lower() in ('.env','.env.local','secrets.json','credentials.json'):
                add(report,'SECRET_FILE','major','Possible sensitive configuration included in ZIP',filename,'Secrets are excluded from distributable builds','Suspicious filename included in archive','Remove secret configuration; rotate any exposed credentials.',confidence='medium')
        for filename in present:
            base=posixpath.basename(filename).lower()
            if base in ('.env','.env.local','.env.production','id_rsa','credentials.json','secrets.json','service-account.json'):
                add(report,'SENSITIVE_FILE','major','Potentially sensitive file bundled',filename,'No credentials or private keys in shared archive','Sensitive filename present','Remove this file from client builds; inspect and rotate keys if exposed.',confidence='medium')
        if browser:
            html_files=sorted(f for f in preview_files if f.lower().endswith(('.html','.htm')))
            target=next((f for f in html_files if f.lower()=='index.html'),html_files[0] if html_files else None)
            if target and on_browser:
                on_browser(report,preview_files,target)
            else: report['warnings'].append('Browser check skipped: no HTML entry page.')
    return finish(report)

def finish(report):
    counts={s:sum(1 for f in report['findings'] if f['severity']==s and f['review']!='rejected') for s in SEVERITIES}
    report['metrics']['severity']=counts
    report['metrics']['findings_total']=sum(counts.values())
    report['metrics']['checks_recorded']=len(report['checked'])
    report['quality_gate']='INCOMPLETE' if not report['checked'] else ('REVIEW_REQUIRED' if counts['critical'] or counts['major'] else ('WARNINGS' if counts['minor'] else 'NO_DETECTED_ISSUES'))
    return report

# Public website scan: pinned IP connection, no cookie/auth submission, same hostname only.
class PinnedHTTP(http.client.HTTPConnection):
    def __init__(self,hostname,pinned_ip,port=80,timeout=8):
        super().__init__(hostname,port,timeout=timeout);self.pinned_ip=pinned_ip
    def connect(self): self.sock=socket.create_connection((self.pinned_ip,self.port),self.timeout)
class PinnedHTTPS(http.client.HTTPSConnection):
    def __init__(self,hostname,pinned_ip,port=443,timeout=8):
        super().__init__(hostname,port,timeout=timeout,context=ssl.create_default_context());self.pinned_ip=pinned_ip
    def connect(self):
        sock=socket.create_connection((self.pinned_ip,self.port),self.timeout)
        self.sock=self._context.wrap_socket(sock,server_hostname=self.host)

def validate_address(url,allow_local=False):
    p=urlsplit(url)
    if p.scheme not in ('http','https') or not p.hostname or p.username or p.password or p.fragment:
        raise ScanError('Only HTTP(S) URLs without credentials/fragments are supported.')
    try: port=p.port
    except ValueError: raise ScanError('Invalid URL port.')
    if port not in (None,80,443) and not (allow_local and p.hostname in ('127.0.0.1','localhost')):
        raise ScanError('Only default HTTP/HTTPS ports are supported.')
    try: results=socket.getaddrinfo(p.hostname,port or (443 if p.scheme=='https' else 80),type=socket.SOCK_STREAM)
    except (OSError,ValueError): raise ScanError('Cannot resolve target hostname.')
    ips=[]
    for res in results:
        ip=res[4][0]; parsed=ipaddress.ip_address(ip)
        if not parsed.is_global and not (allow_local and parsed.is_loopback): raise ScanError('Private/local/reserved addresses are blocked.')
        if ip not in ips:ips.append(ip)
    if not ips: raise ScanError('No allowed IP address for this target.')
    return p, ips

def fetch_page(url,allow_local=False):
    # Re-validate each redirect, connect exclusively to the validated IP (DNS rebinding resistant).
    for redirect in range(4):
        p,ips=validate_address(url,allow_local)
        port=p.port or (443 if p.scheme=='https' else 80)
        conn=(PinnedHTTPS if p.scheme=='https' else PinnedHTTP)(p.hostname,ips[0],port)
        path=(p.path or '/')+('?' + p.query if p.query else '')
        try:
            conn.request('GET',path,headers={'Host':p.netloc,'User-Agent':'ALEX-QA-Factory/1.0 (+authorized-check)','Accept':'text/html','Connection':'close'})
            resp=conn.getresponse(); status=resp.status
            if status in (301,302,303,307,308):
                loc=resp.getheader('Location')
                if not loc: raise ScanError(f'HTTP {status} without Location')
                moved=urljoin(url,loc)
                desthost=urlsplit(moved).hostname
                root=lambda host: (host or '').removeprefix('www.')
                if root(desthost)!=root(p.hostname): raise ScanError('Redirect to another hostname blocked.')
                url=moved;continue
            ct=resp.getheader('Content-Type','')
            raw=resp.read(1_500_001)
            if len(raw)>1_500_000: raise ScanError('Page too large (>1.5 MB).')
            return url,status,ct,raw.decode('utf-8',errors='replace')
        finally: conn.close()
    raise ScanError('Too many redirects.')

def scan_url(url,allow_local=False,max_pages=10):
    url=url.strip();p,_=validate_address(url,allow_local)
    host=p.hostname
    report=make_report('url',url);todo=[url];visited=set();cached={}
    while todo and len(visited)<min(max_pages,MAX_HTML_PAGES):
        current=todo.pop(0)
        if current in visited: continue
        visited.add(current)
        try:
            final,status,ctype,body=fetch_page(current,allow_local)
        except Exception as e:
            add(report,'HTTP_FETCH','major','Page could not be loaded',current,'Page opens successfully',str(e),'Check deployment, SSL, URL and server response.')
            continue
        if len(visited)==1:host=urlsplit(final).hostname or host
        cached[current]=status;report['checked'].append(final+f' [HTTP {status}]')
        if status>=400:
            add(report,'HTTP_STATUS','major','HTTP error response',current,'HTTP 2xx/3xx',f'HTTP {status}','Fix link or restore page.')
            continue
        if 'text/html' not in ctype.lower(): continue
        parser=DocParser()
        try: parser.feed(body)
        except Exception:continue
        scan_html(report,final,body,set(),is_remote=True)
        for a,line in parser.links:
            href=a.get('href','')
            if not href or href.startswith(('#','mailto:','tel:','javascript:')): continue
            link,_=urldefrag(urljoin(final,href))
            dest=urlsplit(link)
            if dest.scheme not in ('http','https') or dest.hostname!=host: continue
            if link not in visited and link not in todo and len(todo)+len(visited)<max_pages*3:
                todo.append(link)
    report['metrics']={'pages_visited':len(visited),'pages_success':sum(1 for status in cached.values() if status<400),'max_pages':max_pages}
    if todo: report['warnings'].append('Page limit reached: some pages were not scanned.')
    report['warnings'].append('URL mode is a non-invasive GET-only audit; dynamic functional workflows are not tested.')
    return finish(report)

def scan_public_github_repo(link,branch='',browser=False,on_browser=None):
    """Download and audit PUBLIC GitHub repositories via codeload.github.com (no tokens)."""
    import urllib.parse
    p=urllib.parse.urlsplit(link.strip())
    if p.scheme!='https' or p.hostname not in ('github.com','www.github.com') or p.username or p.password or p.query or p.fragment:
        raise ScanError('Enter an HTTPS public GitHub URL: https://github.com/owner/repo')
    path=p.path.strip('/').split('/')
    if len(path)<2 or not all(re.fullmatch(r'[\w.\-]+',x,flags=re.ASCII) for x in path[:2]):
        raise ScanError('GitHub URL must include owner and repository name.')
    owner,repo=path[:2]
    repo=repo.removesuffix('.git')
    if not branch:
        if len(path)>=4 and path[2]=='tree':branch=path[3]
        else:branch='main'
    if not re.fullmatch(r'[\w./-]{1,120}',branch,flags=re.ASCII) or '..' in branch or branch.startswith('/'):
        raise ScanError('Unsupported Git branch/ref name.')
    import urllib.parse
    attempts=[branch] if branch!='main' else ['main','master']
    for b in attempts:
        url=f'https://codeload.github.com/{owner}/{repo}/zip/refs/heads/'+urllib.parse.quote(b,safe='/')
        p,ips=validate_address(url)
        conn=PinnedHTTPS('codeload.github.com',ips[0],443,timeout=16)
        try:
            conn.request('GET',p.path,headers={'User-Agent':'ALEX-QA-Factory/1.0','Accept':'application/zip','Connection':'close'})
            resp=conn.getresponse()
            if resp.status==404:continue
            if resp.status!=200:raise ScanError(f'GitHub archive unavailable (HTTP {resp.status}). Private repositories are not supported.')
            blob=resp.read(MAX_ZIP_BYTES+1)
            if len(blob)>MAX_ZIP_BYTES:raise ScanError('GitHub ZIP archive exceeds 25 MB.')
        except (OSError,TimeoutError) as e:raise ScanError('Network error downloading GitHub archive: '+str(e)[:140])
        finally:conn.close()
        r=scan_zip_bytes(blob,f'{owner}/{repo} @ {b}',browser,on_browser)
        r['kind']='github'
        r['warnings'].append('Public GitHub archive only. This does not scan private branches, pull requests or the project build pipeline.')
        return finish(r)
    raise ScanError('Branch not found (tried main/master). Supply the branch explicitly.')
