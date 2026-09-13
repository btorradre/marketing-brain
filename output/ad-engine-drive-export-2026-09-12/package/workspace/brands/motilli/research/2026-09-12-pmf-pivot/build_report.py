from pathlib import Path
import re, json, math, html
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
TARGET = ROOT / 'output/pdf/motilli-product-market-fit-and-pivot.pdf'
raw = (HERE / 'REPORT.md').read_text()
pages = raw.split('<!--page-->')
refs = dict(re.findall(r'^\[\^(\d+)\]: (.+)$', raw, re.M))

body = ParagraphStyle('body', fontName='Helvetica', fontSize=9.7, leading=13.0, spaceAfter=8, textColor=colors.HexColor('#171717'))
title = ParagraphStyle('title', parent=body, fontName='Helvetica-Bold', fontSize=23, leading=28, spaceAfter=18)
cell = ParagraphStyle('cell', parent=body, fontSize=8.8, leading=11.5, spaceAfter=0)
source = ParagraphStyle('source', parent=body, fontSize=8.5, leading=11.5, spaceAfter=9)
foot = ParagraphStyle('foot', parent=body, fontSize=7.0, leading=8.5, spaceAfter=2)

def inline(s):
    s = html.escape(s)
    s = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', lambda m: '<link href="' + html.escape(html.unescape(m[2]), quote=True) + '" color="#222222"><u>' + m[1] + '</u></link>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', s)
    s = re.sub(r'`([^`]+)`', r'\1', s)
    s = re.sub(r'(?:\[\^\d+\])+', lambda m: '<super>' + ','.join(re.findall(r'\d+', m[0])) + '</super>', s)
    return s

page_ref_ids = [sorted(set(re.findall(r'\[\^(\d+)\](?!:)', p)), key=int) for p in pages]

def footer(canvas, doc):
    n = doc.page
    if n <= len(page_ref_ids) and n <= 9:
        ids = page_ref_ids[n-1]
        y = 104
        for ident in ids:
            full = refs[ident]
            link = re.search(r'\[([^\]]+)\]\((https?://[^)]+)\)', full)
            brief = (full.split('. ')[0] + '.').replace('*', '')
            if len(brief) > 116: brief = brief[:113] + '...'
            label = f'{ident}. {html.escape(brief)}'
            if link: label += ' <link href="' + html.escape(link[2], quote=True) + '"><u>Source</u></link>'
            else: label += ' See full local reference in source inventory.'
            p = Paragraph(label, foot)
            w,h = p.wrap(516, 100)
            p.drawOn(canvas, 48, y-h)
            y -= h+1
    canvas.setFillColor(colors.HexColor('#555555'))
    canvas.setFont('Helvetica', 8)
    canvas.drawRightString(564, 22, str(n))

story=[]
for pi, section in enumerate(pages):
    lines=section.strip().splitlines();i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line: i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                vals=[x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[-: ]+',v) for v in vals): rows.append([Paragraph(inline(v),cell) for v in vals])
                i+=1
            cols=len(rows[0]); widths=([190,326] if cols==2 else [132,170,214])
            t=Table(rows,colWidths=widths,hAlign='LEFT')
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#efefef')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),0.6,colors.HexColor('#999999')),('LINEBELOW',(0,1),(-1,-1),0.3,colors.HexColor('#dddddd')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
            story.extend([t,Spacer(1,11)]);continue
        if line.startswith('# '): story.append(Paragraph(inline(line[2:]),title));i+=1;continue
        m=re.match(r'^\[\^(\d+)\]: (.+)$',line)
        if m:
            story.append(Paragraph(f'<b>{m[1]}.</b> '+inline(m[2]),source));i+=1;continue
        para=[line];i+=1
        while i<len(lines) and lines[i].strip() and not lines[i].startswith('|'):
            para.append(lines[i].strip());i+=1
        story.append(Paragraph(inline(' '.join(para)), body if pi<9 else source))
    if pi<len(pages)-1:story.append(PageBreak())

TARGET.parent.mkdir(parents=True,exist_ok=True)
doc=SimpleDocTemplate(str(TARGET),pagesize=(612,792),rightMargin=48,leftMargin=48,topMargin=43,bottomMargin=111,title='Motilli: product-market fit and the next product decision',author='')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
reader=PdfReader(str(TARGET))
print(json.dumps({'pdf':str(TARGET),'pages':len(reader.pages),'expected_logical_pages':len(pages),'page_text_lengths':[len(p.extract_text()) for p in reader.pages]},indent=2))

spend=2193.35;rev=2751.77;purchases=59;lpv=1846
p1=.03;p2=.05;pb=(p1+p2)/2
n=((1.95996398454*math.sqrt(2*pb*(1-pb))+.84162123357*math.sqrt(p1*(1-p1)+p2*(1-p2)))**2)/(p2-p1)**2
calc={'historical_window':'2026-05-04/2026-05-10','source':'acct_0756_7d.json','spend':spend,'reported_purchase_value':rev,'reported_purchases':purchases,'CPA':spend/purchases,'reported_AOV':rev/purchases,'ROAS':rev/spend,'purchase_LPV_ratio':purchases/lpv,'reported_value_less_ad_spend_per_purchase':(rev-spend)/purchases,'sample_size_illustration':{'baseline':p1,'alternative':p2,'two_sided_alpha':.05,'power':.8,'normal_approx_n_per_cell':n,'limitations':'Illustration only; independent equal groups, no sequential stopping or multiplicity adjustment.'}}
(HERE/'calculations.json').write_text(json.dumps(calc,indent=2))
