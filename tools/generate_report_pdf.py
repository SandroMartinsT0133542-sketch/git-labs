from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.units import mm
import sys

def md_to_blocks(md_text):
    # Very small markdown -> blocks converter: split by double newlines
    blocks = []
    parts = md_text.split('\n\n')
    for p in parts:
        if p.startswith('```'):
            # code block
            code = p.strip('`')
            blocks.append(('code', code))
        else:
            blocks.append(('para', p.replace('\n', ' ')))
    return blocks

def build_pdf(md_path, out_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md = f.read()

    doc = SimpleDocTemplate(out_path, pagesize=A4,
                            rightMargin=20*mm, leftMargin=20*mm,
                            topMargin=20*mm, bottomMargin=20*mm)
    styles = getSampleStyleSheet()
    story = []

    blocks = md_to_blocks(md)
    for btype, text in blocks:
        if btype == 'para':
            story.append(Paragraph(text, styles['Normal']))
            story.append(Spacer(1, 4*mm))
        else:
            story.append(Preformatted(text, styles['Code']))
            story.append(Spacer(1, 4*mm))

    doc.build(story)

if __name__ == '__main__':
    md = 'reports/report.md'
    out = 'reports/SandroMartins0133542.pdf'
    try:
        build_pdf(md, out)
        print('Wrote', out)
    except Exception as e:
        print('Error generating PDF:', e, file=sys.stderr)
        raise
