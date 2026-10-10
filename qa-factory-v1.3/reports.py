"""Standalone report exports. Base: JSON, HTML, Markdown, CSV; optional PDF and DOCX."""
from __future__ import annotations
import csv,html,io,json,zipfile
from pathlib import Path


def make_markdown(r):
    v=[]
    v += [f'# ALEX AI QA FACTORY — {r["name"]}', '', f'Run: `{r["id"]}` • {r["started_at"]}',
          f'Mode: {r["kind"]} • Quality gate: **{r["quality_gate"]}**','',
          f'Findings: {len(r["findings"])} • Checked: {len(r["checked"])}','',
          '> Automated checks are partial. Findings require human validation.','']
    for f in r['findings']:
        v += [f'## {f["id"]}: {f["title"]}', '',f'- Rule: `{f["code"]}`',f'- Severity: **{f["severity"]}**', f'- Review: {f["review"]}',f'- Confidence: {f["confidence"]}',f'- Location: `{f["location"]}`',
              f'- Expected: {f["expected"]}',f'- Actual: {f["actual"]}',f'- Fix: {f["recommendation"]}',f'- Evidence: {", ".join(f["evidence"]) or "not captured"}', '']
    v += ['## Checks performed','']+['- '+x for x in r['checked']]
    v += ['','## Warnings / limitations','']+['- '+x for x in r['warnings']]
    return '\n'.join(v)+'\n'

def make_html(r):
    esc=lambda v:html.escape(str(v),quote=True)
    severity={'critical':'#fb7185','major':'#fb923c','minor':'#facc15','info':'#38bdf8'}
    cards=''.join(f'''<article class="issue"><h3><span style="color:{severity.get(f['severity'],'#fff')}">{esc(f['id'])} · {esc(f['severity'].upper())}</span> — {esc(f['title'])}</h3>
      <p class="muted">{esc(f['location'])} · confidence {esc(f['confidence'])} · review: {esc(f['review'])}</p>
      <p><b>Expected / Ожидалось:</b> {esc(f['expected'])}</p><p><b>Actual / Получено:</b> {esc(f['actual'])}</p>
      <p><b>Recommendation / Исправление:</b> {esc(f['recommendation'])}</p>
      {''.join('<p><a href="evidence/'+esc(e)+'">Screenshot '+esc(e)+'</a></p>' for e in f['evidence'])}</article>''' for f in r['findings'])
    counts=''.join(f'<div class="metric"><b>{r["metrics"].get("severity",{}).get(s,0)}</b><small>{s.upper()}</small></div>' for s in severity)
    return f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ALEX QA · {esc(r['name'])}</title>
<style>:root{{color-scheme:dark}}*{{box-sizing:border-box}}body{{margin:0;background:#090f21;color:#e5ecff;font:15px system-ui,Arial}}main{{max-width:1050px;margin:40px auto;padding:25px}}header{{background:linear-gradient(115deg,#15244c,#162f3b);border:1px solid #324d7c;padding:28px;border-radius:18px}}h1{{margin:0}}.muted{{color:#a3b2cb}}.metrics{{display:flex;gap:10px;flex-wrap:wrap;margin:20px 0}}.metric{{padding:15px 22px;border-radius:12px;background:#162440;min-width:105px;display:grid}}.metric b{{font-size:30px}}.metric small{{color:#a9bdd3}}.issue{{border:1px solid #33435a;background:#111d31;border-radius:14px;padding:20px;margin:14px 0}}.issue h3{{margin-top:0}}a{{color:#67e8f9}}li{{margin:6px 0}}@media print{{body{{background:white;color:black}}.issue,header{{break-inside:avoid;background:white;color:black}}.muted{{color:#444}}}}</style>
<main><header><div>🧪 ALEX AI QA FACTORY · AUTOMATED QUALITY AUDIT</div><h1>{esc(r['name'])}</h1><p>{esc(r['started_at'])} · Run {esc(r['id'])}</p><p><b>Quality gate:</b> {esc(r['quality_gate'])}</p></header>
<div class="metrics">{counts}</div><p class="muted">These are detected candidates, NOT verified defects. Human review required. Coverage is partial.</p>
<h2>Findings / Найденные проблемы</h2>{cards or '<p>No issues detected by these checks. This does not prove the product is error-free.</p>'}
<h2>Checks performed / Проверки</h2><ul>{''.join('<li>'+esc(x)+'</li>' for x in r['checked'])}</ul>
<h2>Warnings / Ограничения</h2><ul>{''.join('<li>'+esc(x)+'</li>' for x in r['warnings'])}</ul>
<footer><hr><small>ALEX AI QA FACTORY · Offline-exportable report · Not a security certification.</small></footer></main></html>'''

def make_csv(r):
    f=io.StringIO(); w=csv.writer(f); cols=['id','code','severity','title','location','expected','actual','recommendation','confidence','review','evidence'];w.writerow(cols)
    for x in r['findings']:w.writerow([';'.join(x[k]) if isinstance(x[k],list) else x[k] for k in cols])
    return '\ufeff'+f.getvalue()

def make_pdf(r):
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,KeepTogether
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
    except ImportError:return None
    # Embed a Unicode font when installed (reports can include Cyrillic sites).
    fonts=['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','C:/Windows/Fonts/arial.ttf']
    font='Helvetica'
    for candidate in fonts:
        try:
            if Path(candidate).exists(): pdfmetrics.registerFont(TTFont('AlexUnicode',candidate));font='AlexUnicode';break
        except Exception: pass
    buff=io.BytesIO();doc=SimpleDocTemplate(buff,pagesize=A4,rightMargin=39,leftMargin=39,topMargin=35,bottomMargin=35)
    styles=getSampleStyleSheet(); styles.add(ParagraphStyle(name='AlexHead',fontName=font,fontSize=15,leading=20,spaceAfter=15,textColor=colors.HexColor('#17375d')))
    styles.add(ParagraphStyle(name='AlexText',fontName=font,fontSize=9,leading=14,spaceAfter=7))
    styles.add(ParagraphStyle(name='AlexSub',fontName=font,fontSize=11,leading=16,spaceAfter=10,textColor=colors.HexColor('#2563eb')))
    esc=lambda s:html.escape(str(s)).replace('\n','<br/>')
    story=[Paragraph('ALEX AI QA FACTORY',styles['AlexHead']),Paragraph(esc(r['name']),styles['AlexSub']),Paragraph(f'Run: {esc(r["id"])} | {esc(r["started_at"])} | Gate: {esc(r["quality_gate"])}',styles['AlexText']),Spacer(1,12)]
    for x in r['findings']:
        fields=[f'{x["id"]} — {x["title"]} ({x["severity"]})',f'Location: {x["location"]}',f'Expected: {x["expected"]}',f'Actual: {x["actual"]}',f'Recommendation: {x["recommendation"]}',f'Review: {x["review"]}']
        story += [KeepTogether([Paragraph(esc(fields[0]),styles['AlexSub'])]+[Paragraph(esc(v),styles['AlexText']) for v in fields[1:]])]
    story += [Spacer(1,8),Paragraph('Coverage / limitations',styles['AlexSub'])]
    for msg in r['warnings']: story += [Paragraph(esc(msg),styles['AlexText'])]
    story += [Paragraph('AI/automated findings must be reviewed before delivery. No complete-coverage guarantee.',styles['AlexText'])]
    doc.build(story);return buff.getvalue()

def make_docx(r):
    try:from docx import Document
    except ImportError:return None
    doc=Document();doc.add_heading('ALEX AI QA FACTORY',0);doc.add_heading(str(r['name']),1)
    doc.add_paragraph(f'Run: {r["id"]} | {r["started_at"]} | {r["quality_gate"]}')
    doc.add_paragraph('Automated findings need human validation. Coverage is partial.')
    for x in r['findings']:
        doc.add_heading(f'{x["id"]} — {x["title"]}',2)
        for label,k in [('Severity','severity'),('Location','location'),('Expected','expected'),('Actual','actual'),('Recommendation','recommendation'),('Review status','review')]:
            doc.add_paragraph(f'{label}: {x[k]}')
    doc.add_heading('Checks performed',2)
    for c in r['checked']:doc.add_paragraph(c,style='List Bullet')
    doc.add_heading('Warnings / Limitations',2)
    for c in r['warnings']:doc.add_paragraph(c,style='List Bullet')
    b=io.BytesIO();doc.save(b);return b.getvalue()

def archive_report(r,evidence_dir=None):
    out=io.BytesIO()
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr('QA_REPORT.json',json.dumps(r,ensure_ascii=False,indent=2))
        z.writestr('QA_REPORT.md',make_markdown(r))
        z.writestr('QA_REPORT.html',make_html(r))
        z.writestr('BUGS.csv',make_csv(r))
        pdf=make_pdf(r)
        if pdf:z.writestr('QA_REPORT.pdf',pdf)
        doc=make_docx(r)
        if doc:z.writestr('QA_REPORT.docx',doc)
        if evidence_dir:
            for item in r.get('evidence',[]):
                path=Path(evidence_dir)/item
                if path.is_file() and path.name==item:z.write(path,arcname='evidence/'+item)
        z.writestr('READ_ME_FIRST.txt','ALEX AI QA FACTORY — QA DELIVERY PACKAGE\n\nReport files: HTML, Markdown, JSON, CSV, plus PDF/DOCX when optional dependencies are installed.\nOpen QA_REPORT.html in a browser.\nEvery finding begins as a candidate and should be human-reviewed before sending to a client.\n\nEN: Automated scanning is partial; a clean report is not a certification.\nRU: Автоматические проверки неполные; отсутствие обнаруженных ошибок не гарантирует качество.\nUA: Автоматичні перевірки неповні; відсутність виявлених помилок не гарантує якість.\n')
    return out.getvalue()

def make_test_plan(r):
    kind=r['kind'];done=r.get('checked',[])
    cases=[
        ('TC-001','Site structure / Структура','Verify HTML pages and metadata','Static scan','Executed' if any('.html' in x or '.htm' in x for x in done) else 'Not executed'),
        ('TC-002','Links / Ссылки','Check same-site/local references','Static scan','Executed' if done else 'Not executed'),
        ('TC-003','Syntax / Синтаксис','Validate JSON and JS when available','Static scan','Executed' if kind=='zip' else 'Not applicable'),
        ('TC-004','Desktop UI / Интерфейс ПК','Check page load, JS exceptions and overflow','Chromium preview','Executed' if 'desktop.png' in r.get('evidence',[]) else 'Not executed'),
        ('TC-005','Mobile UI / Интерфейс телефона','Check 390px viewport for layout overflow and broken images','Chromium preview','Executed' if 'mobile.png' in r.get('evidence',[]) else 'Not executed'),
        ('TC-006','Form validation / Формы','Review email and required-field behaviour','Partial static + no-submit browser probe','Partially executed' if done else 'Not executed'),
        ('TC-007','Keyboard accessibility / Клавиатура','Tab through forms and keyboard navigation','Manual test','Suggested / not executed'),
        ('TC-008','Business workflows / Бизнес-логика','Complete checkout/signup/save workflow in test account','Manual + scripted E2E','Suggested / not executed'),
        ('TC-009','Security / Безопасность','Review sensitive actions, authorization and dependency vulnerabilities','Authorized security review','Suggested / not executed'),
        ('TC-010','Performance / Производительность','Measure Lighthouse metrics in deployed/staging environment','Lighthouse','Suggested / not executed'),
        ('TC-011','Cross-browser / Другие браузеры','Verify Firefox and Safari/WebKit behaviours','Additional browser tests','Suggested / not executed'),
    ]
    return cases

def test_plan_markdown(r):
    lines=[f'# TEST PLAN — {r["name"]}','',f'Run / Запуск: {r["id"]}','',
      '## Scope / Объём','Only supported automated checks were executed. Other cases are recommendations, not PASS results.',
      'Выполнены только поддерживаемые автоматические проверки. Остальные тест-кейсы — рекомендации, не результат PASS.','','## Cases / Тест-кейсы','',
      '| ID | Area / Область | How / Способ | State / Статус |','|---|---|---|---|']
    for id,area,description,method,state in make_test_plan(r):lines.append(f'| {id} | {area} | {method} | {state} |')
    lines += ['','## Acceptance / Приёмка','','- Review every candidate bug before client delivery. / Проверь каждую предполагаемую ошибку.','- Re-test after fixes. / Повтори проверку после исправлений.','- Do not claim full coverage. / Не заявляй о полном покрытии.','']
    return '\n'.join(lines)

def cases_csv(r):
    buf=io.StringIO();wr=csv.writer(buf);wr.writerow(['id','area_en_ru','description','method','execution_status'])
    for row in make_test_plan(r):wr.writerow(row)
    return '\ufeff'+buf.getvalue()

def release_checklist(r):
    major=sum(f['review']!='rejected' and f['severity'] in ('critical','major') for f in r['findings'])
    return '\n'.join(['# PRE-RELEASE CHECKLIST / ЧЕК-ЛИСТ ПЕРЕД ПУБЛИКАЦИЕЙ','',
      f'- [{"x" if major==0 else " "}] No open Critical/Major candidates / Нет открытых серьёзных проблем ({major} remaining)',
      '- [ ] All High/Major findings reviewed / Все серьёзные находки подтверждены или отклонены',
      '- [ ] Forms tested with safe test data / Формы проверены тестовыми данными',
      '- [ ] Mobile layout approved / Мобильный вид проверен',
      '- [ ] Keyboard navigation tested / Навигация клавиатурой проверена',
      '- [ ] Privacy/GDPR review completed / Проверена конфиденциальность и GDPR',
      '- [ ] Deployment/staging end-to-end tests passed / E2E-тесты на тестовом сервере пройдены',
      '- [ ] Owner approved release / Владелец разрешил выпуск',
      '',f'Automated gate: {r["quality_gate"]}',
      'This checklist does not automatically grant a release certificate. / Этот документ не является автоматическим сертификатом качества.',''])

# Add structured planning artifacts without modifying the original archival function.
_base_archive_report=archive_report
def archive_report(r,evidence_dir=None):
    packed=_base_archive_report(r,evidence_dir)
    output=io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(packed),'r') as source,zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as z:
        for name in source.namelist():z.writestr(name,source.read(name))
        z.writestr('TEST_PLAN_EN_RU.md',test_plan_markdown(r))
        z.writestr('TEST_CASES.csv',cases_csv(r))
        z.writestr('RELEASE_CHECKLIST_EN_RU.md',release_checklist(r))
    return output.getvalue()

# Fixed-rule bilingual client notes; raw observed values remain verbatim evidence.
RULE_TRANSLATIONS={
'SEO_TITLE':('Нет заголовка страницы','Додайте заголовок сторінки'),
'MOBILE_VIEWPORT':('Не задан масштаб для мобильных устройств','Не задано масштаб для мобільних пристроїв'),
'LANG':('Не указан язык HTML-страницы','Не вказано мову HTML-сторінки'),
'SEO_DESCRIPTION':('Нет метаописания страницы','Немає метаопису сторінки'),
'H1_MISSING':('Нет основного заголовка H1','Немає головного заголовка H1'),
'IMAGE_ALT':('У изображения отсутствует атрибут alt','Зображення не має атрибута alt'),
'INPUT_LABEL':('У поля может отсутствовать доступная подпись','Поле може не мати доступного підпису'),
'EMAIL_TYPE':('Поле email не использует type=email','Поле email не використовує type=email'),
'TARGET_BLANK':('Открытие новой вкладки без защиты rel','Відкриття нової вкладки без захисту rel'),
'PATH_OUTSIDE':('Путь выходит за пределы проекта','Шлях виходить за межі проєкту'),
'BROKEN_REFERENCE':('Ссылка указывает на отсутствующий файл','Посилання вказує на відсутній файл'),
'BROKEN_ANCHOR':('Не найден якорь на странице','Не знайдено якір на сторінці'),
'INVALID_JSON':('Некорректный синтаксис JSON','Некоректний синтаксис JSON'),
'JS_SYNTAX':('Ошибка синтаксиса JavaScript','Помилка синтаксису JavaScript'),
'SENSITIVE_FILE':('В архиве может быть конфиденциальный файл','В архіві може бути конфіденційний файл'),
'SECRET_FILE':('В архиве есть подозрительный конфигурационный файл','В архіві є підозрілий конфігураційний файл'),
'HTTP_FETCH':('Не удалось загрузить страницу','Не вдалося завантажити сторінку'),
'HTTP_STATUS':('Страница вернула HTTP-ошибку','Сторінка повернула HTTP-помилку'),
'HORIZONTAL_OVERFLOW':('Страница шире экрана','Сторінка ширша за екран'),
'BROKEN_IMAGES':('Изображение не отображается в тестовом браузере','Зображення не відображається у тестовому браузері'),
'BROWSER_JS_ERROR':('В браузере произошла ошибка JavaScript','У браузері сталася помилка JavaScript'),
'EMAIL_BROWSER_VALIDATION':('Браузер допускает некорректный email','Браузер допускає некоректний email'),
'BROWSER_HTTP_ERRORS':('Ресурс вернул ошибку HTTP','Ресурс повернув помилку HTTP'),
'HTML_PARSE':('Не удалось прочитать HTML','Не вдалося прочитати HTML'),
'INLINE_JS_SYNTAX':('Ошибка во встроенном JavaScript','Помилка у вбудованому JavaScript')
}
def bilingual_report(r,lang='ru'):
    ru=lang=='ru'
    L=(lambda x,y:x if ru else y)
    lines=[f'# {r["name"]} — ALEX QA REPORT',
        L('# Отчёт с построчным переводом', '# Звіт із порядковим перекладом'),'',
        'Quality gate: '+r['quality_gate'],L('Статус проверки: '+r['quality_gate'],'Стан перевірки: '+r['quality_gate']),'',
        'All issues are candidate findings until manually reviewed.',
        L('Все найденные проблемы предварительны до проверки человеком.','Усі виявлені проблеми попередні до перевірки людиною.'),'']
    for f in r['findings']:
        title=RULE_TRANSLATIONS.get(f['code'],(f['title'],f['title']))[0 if ru else 1]
        lines += [f'## {f["id"]} / {f["code"]}',f'EN: {f["title"]}',L('RU: ','UA: ')+title,'',
          f'EN — Severity: {f["severity"]}',L('RU — Серьёзность: ','UA — Серйозність: ')+f['severity'],
          f'EN — Location: `{f["location"]}`',L('RU — Расположение: ','UA — Розташування: ')+f'`{f["location"]}`',
          f'EN — Expected: {f["expected"]}',L('RU — Ожидалось: требуется корректное поведение по правилу '+f['code'],'UA — Очікувалося: коректна поведінка за правилом '+f['code']),
          f'EN — Actual (raw evidence): {f["actual"]}',L('RU — Фактические данные (оригинальный журнал): ','UA — Фактичні дані (оригінальний журнал): ')+str(f['actual']),
          f'EN — Suggested fix: {f["recommendation"]}',L('RU — Исправление: см. правило ','UA — Виправлення: див. правило ')+f['code']+' — '+title,
          f'EN — Review status: {f["review"]}',L('RU — Подтверждение: ','UA — Підтвердження: ')+f['review'],'']
    lines += ['## Coverage / Ограничения','',
       'EN: Tested files/pages: '+str(len(r.get('checked',[]))),
       L('RU: Проверено файлов/страниц: ','UA: Перевірено файлів/сторінок: ')+str(len(r.get('checked',[]))),
       'EN: This is not a certification of complete software quality.',
       L('RU: Это не сертификат полного качества программного обеспечения.','UA: Це не сертифікат повної якості програмного забезпечення.'),'']
    return '\n'.join(lines)

def review_prompt(r):
    return '\n'.join(['# AI REVIEW WORKSHEET / ЛИСТ ПРОВЕРКИ С ПОМОЩЬЮ ИИ','',
       'EN: Optional manual workflow. This file is NOT sent to any AI service automatically.',
       'RU: Дополнительный ручной процесс. Этот файл НЕ отправляется в сервис ИИ автоматически.','',
       'EN: Review these candidates for false positives; propose a safe manual test plan and request missing business requirements. Never invent evidence.',
       'RU: Проверь находки на ложные срабатывания, предложи безопасный ручной план тестов и уточни недостающие требования. Не выдумывай доказательства.','',
       'Issues / Найденные проблемы:',
       *[f'- {f["id"]} | {f["code"]} | {f["severity"]} | {f["location"]} | {f["actual"]}' for f in r['findings']],
       '', 'EN: Remove any client-sensitive information before pasting into an AI chat.',
       'RU: Удали конфиденциальные данные клиента, прежде чем вставлять этот текст в чат ИИ.',''])

_prev_archive_report=archive_report
def archive_report(r,evidence_dir=None):
    existing=_prev_archive_report(r,evidence_dir)
    output=io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(existing),'r') as src,zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as z:
        for name in src.namelist():z.writestr(name,src.read(name))
        z.writestr('QA_REPORT_EN_RU.md',bilingual_report(r,'ru'))
        z.writestr('QA_REPORT_EN_UA.md',bilingual_report(r,'uk'))
        z.writestr('AI_REVIEW_WORKSHEET_EN_RU.md',review_prompt(r))
    return output.getvalue()
