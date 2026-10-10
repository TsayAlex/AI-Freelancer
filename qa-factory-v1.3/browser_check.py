"""Optional, in-memory Chromium smoke tests. No uploaded server-side code is executed.
All browser network requests are blocked. This is a partial static-page preview.
"""
from __future__ import annotations
import base64
import mimetypes
import re
import shutil
from pathlib import Path
from qa_engine import add, normalize_local


def hydrate_local_assets(html_text, entry, preview_files):
    """Embed common local CSS/JS/images to support browser previews with zero network I/O."""
    def asset(ref):
        key=normalize_local(entry,ref)
        return preview_files.get(key or '') if key else None
    def style_replace(m):
        tag=m.group(0);href=re.search(r'\bhref\s*=\s*["\']([^"\']+)["\']',tag,re.I)
        if href and 'stylesheet' in tag.lower():
            body=asset(href.group(1))
            if body is not None and len(body)<400_000:
                return '<style>'+body.decode('utf-8','replace').replace('</style','<\\/style')+'</style>'
        return tag
    html_text=re.sub(r'<link\b[^>]*>',style_replace,html_text,flags=re.I)
    def script_replace(m):
        tag=m.group(0);ref=re.search(r'\bsrc\s*=\s*["\']([^"\']+)["\']',tag,re.I)
        if ref:
            body=asset(ref.group(1))
            if body is not None and len(body)<400_000:
                code=body.decode('utf-8','replace').replace('</script','<\\/script')
                return '<script>'+code+'</script>'
        return tag
    html_text=re.sub(r'<script\b[^>]*\bsrc\s*=\s*["\'][^"\']+["\'][^>]*>\s*</script\s*>',script_replace,html_text,flags=re.I)
    def img_replace(m):
        tag=m.group(0);src=re.search(r'\bsrc\s*=\s*["\']([^"\']+)["\']',tag,re.I)
        if src:
            body=asset(src.group(1))
            if body is not None and len(body)<800_000:
                ext=Path(src.group(1)).suffix.lower();mime=mimetypes.types_map.get(ext,'application/octet-stream')
                url=f'data:{mime};base64,'+base64.b64encode(body).decode('ascii')
                return tag[:src.start(1)]+url+tag[src.end(1):]
        return tag
    html_text=re.sub(r'<img\b[^>]*>',img_replace,html_text,flags=re.I)
    return html_text


def run_preview(report,preview_files,entry):
    try:from playwright.sync_api import sync_playwright
    except ImportError:
        report['warnings'].append('Browser preview unavailable: install Playwright (see INSTALL_BROWSER_WINDOWS.bat).');return
    markup=preview_files[entry].decode('utf-8',errors='replace')
    markup=hydrate_local_assets(markup,entry,preview_files)
    try:
        with sync_playwright() as pw:
            chromium=shutil.which('chromium') or shutil.which('google-chrome')
            options={'headless':True,'args':['--no-sandbox','--disable-dev-shm-usage']}
            if chromium:options['executable_path']=chromium
            browser=pw.chromium.launch(**options)
            try:
                for viewport,label in [({'width':1365,'height':768},'desktop'),({'width':390,'height':844},'mobile')]:
                    context=browser.new_context(viewport=viewport,accept_downloads=False,service_workers='block')
                    try:
                        page=context.new_page();page_errors=[];console_errors=[]
                        # Block every network request: only inline/data resources render.
                        page.route('**/*',lambda route:route.abort())
                        page.on('pageerror',lambda e:page_errors.append(str(e)[:350]))
                        page.on('console',lambda m:console_errors.append(m.text[:220]) if m.type=='error' else None)
                        # In-memory preview uses an opaque about:blank origin. Real applications can
                        # access localStorage on a deployed origin, but Chromium forbids it here.
                        # A tiny ephemeral mock prevents QA-tool-induced false JavaScript bugs.
                        # This does NOT test real persistence or storage quota/permissions.
                        page.evaluate("""() => { for(const key of ['localStorage','sessionStorage']) {
                          const values = new Map();
                          Object.defineProperty(window, key, {configurable:true, value:{
                            get length(){return values.size},
                            key:(i)=>[...values.keys()][i] ?? null,
                            getItem:(k)=>values.has(String(k))?values.get(String(k)):null,
                            setItem:(k,v)=>values.set(String(k),String(v)),
                            removeItem:(k)=>values.delete(String(k)),
                            clear:()=>values.clear()
                          }});
                        } }""")
                        page.set_content(markup,wait_until='domcontentloaded',timeout=12000)
                        page.wait_for_timeout(300)
                        metrics=page.evaluate('''() => ({ imagesBroken:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).length, overflow:document.documentElement.scrollWidth > innerWidth + 6 })''')
                        artifact=f'{label}.png';report.setdefault('_evidence_bytes',{})[artifact]=page.screenshot(full_page=False,timeout=5000)
                        report['evidence'].append(artifact)
                        report['checked'].append(f'{entry} [Chromium {label} {viewport["width"]}x{viewport["height"]}]')
                        if metrics['overflow']:
                            add(report,'HORIZONTAL_OVERFLOW','minor','Layout overflows viewport',f'{entry} ({label})','No horizontal overflow','Document width exceeds viewport','Fix responsive layout.',evidence=[artifact])
                        if metrics['imagesBroken']:
                            # External image requests are intentionally blocked. Do not misclassify
                            # blocked network resources as verified application bugs.
                            report['warnings'].append(f'{label}: {metrics["imagesBroken"]} image(s) unavailable in offline preview. Remote/network resources are intentionally blocked; verify on a trusted full deployment.')
                        # Non-submitting email validation probe: does the browser accept an obviously invalid email?
                        try:
                            probe=page.evaluate('''() => { const f=[...document.querySelectorAll('input')].find(e => /email/i.test((e.name||'')+' '+(e.id||''))); if(!f) return null; let before=f.value;f.value='not-an-email';let valid=f.checkValidity();f.value=before;return {valid,type:f.type} }''')
                            if probe and probe['valid']:
                                add(report,'EMAIL_BROWSER_VALIDATION','minor','Invalid email passes native field validation',f'{entry} ({label})','Malformed email rejected by native validation','not-an-email considered valid by browser field validation','Use type=email and validate again on the server; custom submit handlers were not exercised.',evidence=[artifact],confidence='medium')
                        except Exception: pass
                        if page_errors:
                            add(report,'BROWSER_JS_ERROR','major','Uncaught browser JavaScript exception',f'{entry} ({label})','No JS runtime exceptions','; '.join(page_errors[:3]),'Inspect JavaScript error and source.',evidence=[artifact])
                        if console_errors and not page_errors:
                            report['warnings'].append(f'{label} browser console (may include blocked resources): '+'; '.join(console_errors[:2]))
                    finally:context.close()
            finally:browser.close()
    except Exception as e:report['warnings'].append('Optional browser preview failed: '+str(e)[:220])
    report['warnings'].append('Browser preview is in-memory and offline (desktop/mobile). Storage APIs are simulated; real persistence, external assets and API calls are NOT tested. This is not a full deployed-app functional test.')
