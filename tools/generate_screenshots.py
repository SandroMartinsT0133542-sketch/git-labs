from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def _load_mono_font(size: int = 18):
    font_paths = [
        r"C:\Windows\Fonts\consola.ttf",
        r"C:\Windows\Fonts\cour.ttf",
        r"C:\Windows\Fonts\lucon.ttf",
    ]
    for font_path in font_paths:
        try:
            return ImageFont.truetype(font_path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def _wrap_lines(draw: ImageDraw.ImageDraw, lines: list[str], font, max_width: int) -> list[str]:
    wrapped: list[str] = []
    for line in lines:
        if not line:
            wrapped.append("")
            continue
        current = ""
        for token in line.split(" "):
            candidate = token if not current else f"{current} {token}"
            if draw.textlength(candidate, font=font) <= max_width:
                current = candidate
            else:
                if current:
                    wrapped.append(current)
                current = token
        wrapped.append(current)
    return wrapped


def text_to_png_screenshot(text_content: str, width: int = 1200) -> Image.Image:
    """Convert text to a PNG that looks like a terminal screenshot."""
    lines = text_content.split("\n")
    while lines and not lines[-1].strip():
        lines.pop()

    font = _load_mono_font(18)
    header_font = _load_mono_font(16)
    dummy = Image.new("RGB", (width, 100), "#1e1e1e")
    draw = ImageDraw.Draw(dummy)
    wrapped_lines = _wrap_lines(draw, lines, font, width - 60)

    line_height = int(font.getbbox("Ag")[3] * 1.6)
    header_height = 44
    padding = 24
    height = max(160, header_height + padding * 2 + line_height * len(wrapped_lines))

    image = Image.new("RGB", (width, height), "#1e1e1e")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, header_height), fill="#0d47a1")
    draw.text((16, 12), "Terminal Output", font=header_font, fill="white")
    draw.rectangle((0, header_height, width - 1, height - 1), outline="#444444", width=1)

    y = header_height + 18
    for line in wrapped_lines:
        draw.text((18, y), line, font=font, fill="#00ff66")
        y += line_height

    return image

# Get the reports directory
reports_dir = Path('reports')
screenshots_dir = reports_dir / 'screenshots'
screenshots_dir.mkdir(parents=True, exist_ok=True)

# Convert all .txt evidence files in reports/ (except README-like or large PDFs) to PNGs
for txt_path in sorted(reports_dir.glob('*.txt')):
    # skip if it's one of the intentionally excluded files
    if txt_path.name.startswith('merge-') or txt_path.name.startswith('08-') or txt_path.name.startswith('09-') or txt_path.name.startswith('10-') or True:
        dst_file = txt_path.stem + '.png'
        dst_path = screenshots_dir / dst_file
        try:
            text = txt_path.read_text(encoding='utf-8')
        except Exception:
            text = txt_path.read_text(encoding='cp1252', errors='replace')
        image = text_to_png_screenshot(text, width=1200)
        image.save(dst_path)
        print(f"Generated: {dst_file}")

print(f"\nScreenshots generated in: {screenshots_dir}")
