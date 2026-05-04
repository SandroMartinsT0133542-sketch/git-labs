from __future__ import annotations

from pathlib import Path
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)
ROOT = Path(__file__).resolve().parents[1]
REPORT_MD = ROOT / "reports" / "report.md"
OUTPUT_PDF = ROOT / "reports" / "SandroMartins0133542.pdf"
SCREENSHOTS_DIR = ROOT / "reports" / "screenshots"


SCREENSHOT_ITEMS = [
    ("git-status-initial.png", "Figura 1. Estado inicial do repositório"),
    ("git-status-conflict.png", "Figura 2. Estado do repositório durante o conflito"),
    ("git-diff-conflict.png", "Figura 3. Diff do conflito com marcadores"),
    ("git-log-graph.png", "Figura 4. Histórico pós-merge em gráfico"),
    ("git-tags-list.png", "Figura 5. Lista de tags criadas"),
]


LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            parent=styles["Title"],
            fontName="Times-Bold",
            fontSize=21,
            leading=25,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#1f2d3d"),
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverSubtitle",
            parent=styles["BodyText"],
            fontName="Times-Italic",
            fontSize=10.2,
            leading=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4b5563"),
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionHeading",
            parent=styles["Heading1"],
            fontName="Times-Bold",
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#1f2937"),
            spaceBefore=10,
            spaceAfter=6,
            keepWithNext=True,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SubHeading",
            parent=styles["Heading2"],
            fontName="Times-Bold",
            fontSize=11.5,
            leading=14,
            textColor=colors.HexColor("#374151"),
            spaceBefore=7,
            spaceAfter=4,
            keepWithNext=True,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            parent=styles["BodyText"],
            fontName="Times-Roman",
            fontSize=10,
            leading=14,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#1f2937"),
            spaceAfter=5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BulletCustom",
            parent=styles["BodyText"],
            fontName="Times-Roman",
            fontSize=9.8,
            leading=13.4,
            leftIndent=14,
            firstLineIndent=-8,
            textColor=colors.HexColor("#1f2937"),
            spaceAfter=2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CodeCustom",
            parent=styles["Code"],
            fontName="Courier",
            fontSize=8.15,
            leading=10,
            textColor=colors.HexColor("#17212b"),
            backColor=colors.HexColor("#f3f6f8"),
            borderPadding=7,
            leftIndent=6,
            rightIndent=6,
            spaceBefore=2,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Meta",
            parent=styles["BodyText"],
            fontName="Times-Roman",
            fontSize=10,
            leading=12.5,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4b5563"),
            spaceAfter=0,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Evidence",
            parent=styles["BodyText"],
            fontName="Times-Bold",
            fontSize=9.6,
            leading=12,
            textColor=colors.HexColor("#1f5f8b"),
            spaceAfter=4,
        )
    )
    return styles


def sanitize_text(value: str) -> str:
    return (
        value.replace("Evidências", "Registos")
        .replace("evidências", "registos")
        .replace("Evidência", "Registo")
        .replace("evidência", "registo")
        .replace("evidencias", "registos")
        .replace("evidencia", "registo")
    )


def format_inline(text: str) -> str:
    sanitized = sanitize_text(text)
    # Strip markdown inline-code markers to avoid ReportLab parser conflicts.
    sanitized = sanitized.replace("`", "")
    return escape(sanitized)


def pretty_caption_from_filename(filename: str) -> str:
    stem = Path(filename).stem
    readable = stem.replace("-", " ").replace("_", " ").strip()
    if not readable:
        return "Registo visual"
    return readable[:1].upper() + readable[1:]


def screenshot_name_from_link(link_path: str) -> str | None:
    normalized = link_path.replace("\\", "/")
    if "reports/screenshots/" not in normalized:
        return None
    file_name = Path(normalized).name
    suffix = Path(file_name).suffix.lower()
    if suffix == ".svg":
        return f"{Path(file_name).stem}.png"
    if suffix == ".png":
        return file_name
    return None


def image_block(image_name: str, caption: str, max_width: float = 16.0 * cm):
    image_path = SCREENSHOTS_DIR / image_name
    if not image_path.exists():
        return Paragraph(f"{caption} (ficheiro PNG indisponível)", getSampleStyleSheet()["BodyText"])

    image = Image(str(image_path))
    if image.drawWidth > max_width:
        scale = max_width / image.drawWidth
        image.drawWidth *= scale
        image.drawHeight *= scale

    return KeepTogether(
        [
            Paragraph(caption, getSampleStyleSheet()["Italic"]),
            Spacer(1, 0.12 * cm),
            image,
            Spacer(1, 0.18 * cm),
        ]
    )


def build_cover_table(styles):
    data = [
        ["Aluno", "Sandro Ferreira Martins"],
        ["Número", "0133542"],
        ["Email", "Sandro.Martins.T0133542@edu.atec.pt"],
        ["Tema", "Git, GitHub, branches, merge, tags e registos visuais"],
    ]
    table = Table(data, colWidths=[3.0 * cm, 12.8 * cm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d6eaf8")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fbfd")]),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#23313f")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9.2),
                ("LEADING", (0, 0), (-1, -1), 11),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b3c6d6")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def parse_markdown(text: str, styles):
    story = []
    in_code = False
    code_buffer: list[str] = []

    bullet_re = re.compile(r"^-\s+(.*)$")
    ordered_re = re.compile(r"^\d+\.\s+(.*)$")

    def flush_code() -> None:
        nonlocal code_buffer
        if code_buffer:
            story.append(Preformatted("\n".join(code_buffer), styles["CodeCustom"]))
            code_buffer = []

    def add_screenshot(image_name: str, caption: str) -> None:
        story.append(image_block(image_name, caption))

    for line in text.splitlines()[4:]:
        stripped = line.rstrip()
        compact = stripped.strip()

        compact = sanitize_text(compact)

        if compact.startswith("```"):
            if in_code:
                flush_code()
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_buffer.append(stripped)
            continue

        if not compact:
            story.append(Spacer(1, 0.12 * cm))
            continue

        if compact.startswith("## "):
            story.append(Paragraph(format_inline(compact[3:]), styles["SectionHeading"]))
            continue

        if compact.startswith("### "):
            story.append(Paragraph(format_inline(compact[4:]), styles["SubHeading"]))
            continue

        if compact.startswith("#### "):
            story.append(Paragraph(format_inline(compact[5:]), styles["SubHeading"]))
            continue

        if compact.startswith("**") and compact.endswith("**"):
            bold_text = compact[2:-2]
            story.append(Paragraph(f"<b>{format_inline(bold_text)}</b>", styles["Body"]))
            continue

        link_match = LINK_RE.search(compact)
        if link_match:
            link_text = link_match.group(1).strip()
            link_path = link_match.group(2).strip()

            screenshot_name = screenshot_name_from_link(link_path)
            if screenshot_name:
                caption_text = link_text if "screenshots/" not in link_text else pretty_caption_from_filename(screenshot_name)
                add_screenshot(screenshot_name, f"Figura. {format_inline(caption_text)}")
                continue

            link_label = format_inline(link_text)
            link_target = format_inline(link_path)
            story.append(Paragraph(f"{link_label}: <font color='#1f5f8b'>{link_target}</font>", styles["Body"]))
            continue

        if compact.startswith("**Registo"):
            story.append(Paragraph(format_inline(compact.replace("**", "", 2)), styles["Evidence"]))
            continue

        bullet_match = bullet_re.match(compact)
        if bullet_match:
            story.append(Paragraph(f"• {format_inline(bullet_match.group(1))}", styles["BulletCustom"]))
            continue

        ordered_match = ordered_re.match(compact)
        if ordered_match:
            story.append(Paragraph(format_inline(compact), styles["BulletCustom"]))
            continue

        story.append(Paragraph(format_inline(compact), styles["Body"]))

    if in_code:
        flush_code()

    return story


def cover_page(story, styles):
    story.extend(
        [
            Spacer(1, 0.5 * cm),
            Paragraph("Relatório de Projeto Web", styles["CoverTitle"]),
            Paragraph("Relatório técnico-académico", styles["CoverSubtitle"]),
            Spacer(1, 0.28 * cm),
            Paragraph(
                sanitize_text("Documento académico com registos textuais e visuais de commits, branches, merge com conflito, tags e preparação de colaboração GitHub."),
                styles["Body"],
            ),
            Spacer(1, 0.45 * cm),
            build_cover_table(styles),
            Spacer(1, 0.35 * cm),
            Paragraph("Resumo", styles["SubHeading"]),
            Paragraph(
                sanitize_text("O trabalho demonstra a criação, evolução e análise de um repositório Git com foco em rigor operacional, documentação de registos e preparação para colaboração no GitHub. A estrutura inclui comandos essenciais, análise do histórico, resolução de conflito de merge, tagging semântica e material visual de suporte."),
                styles["Body"],
            ),
            Paragraph("Palavras-chave", styles["SubHeading"]),
            Paragraph("Git, GitHub, branches, merge, conflito, tags, documentação, registo visual", styles["Body"]),
            Spacer(1, 0.15 * cm),
            Table(
                [["Registos principais", "Screenshots SVG, report.md e logs de Git"], ["Colaborador", "vicsolucoes"], ["Estado", "Relatório revisto e pronto para submissão"]],
                colWidths=[4.2 * cm, 11.6 * cm],
                style=TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ebf5fb")),
                        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f8fbfd")]),
                        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b3c6d6")),
                        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#23313f")),
                        ("FONTSIZE", (0, 0), (-1, -1), 9.0),
                        ("LEADING", (0, 0), (-1, -1), 11),
                        ("LEFTPADDING", (0, 0), (-1, -1), 6),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                        ("TOPPADDING", (0, 0), (-1, -1), 5),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ]
                ),
            ),
            PageBreak(),
        ]
    )


def screenshots_page(story, styles):
    story.append(Paragraph("Registos Visuais", styles["SectionHeading"]))
    story.append(Paragraph("As figuras seguintes sintetizam os momentos-chave do trabalho e substituem os blocos textuais de registo.", styles["Body"]))
    story.append(Spacer(1, 0.2 * cm))
    for svg_name, caption in SCREENSHOT_ITEMS:
        story.append(image_block(svg_name, caption))



def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#c7d5e0"))
    canvas.setLineWidth(0.35)
    canvas.line(doc.leftMargin, 1.45 * cm, A4[0] - doc.rightMargin, 1.45 * cm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#5d6d7e"))
    canvas.drawString(doc.leftMargin, 1.0 * cm, "Projeto Git & GitHub")
    canvas.drawRightString(A4[0] - doc.rightMargin, 1.0 * cm, f"Página {doc.page}")
    canvas.restoreState()


def build_pdf() -> None:
    styles = build_styles()
    markdown_text = REPORT_MD.read_text(encoding="utf-8")
    story = []

    cover_page(story, styles)
    screenshots_page(story, styles)
    story.extend(parse_markdown(markdown_text, styles))

    frame = Frame(
        2.0 * cm,
        1.9 * cm,
        A4[0] - 4.0 * cm,
        A4[1] - 3.7 * cm,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
        id="normal",
    )

    doc = BaseDocTemplate(
        str(OUTPUT_PDF),
        pagesize=A4,
        leftMargin=2.0 * cm,
        rightMargin=2.0 * cm,
        topMargin=1.7 * cm,
        bottomMargin=1.8 * cm,
        title="Relatório de Projeto Web - Git & GitHub",
        author="Sandro Ferreira Martins",
        subject="Git, GitHub e registos do projeto web",
        creator="GitHub Copilot",
    )
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=footer)])
    doc.build(story)
    print(f"Wrote {OUTPUT_PDF} ({OUTPUT_PDF.stat().st_size} bytes)")


if __name__ == "__main__":
    build_pdf()