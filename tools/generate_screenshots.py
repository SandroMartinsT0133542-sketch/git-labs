import html
from pathlib import Path

def text_to_svg_screenshot(text_content: str, width: int = 1000, line_height: int = 20) -> str:
    """Convert text to an SVG that looks like a terminal screenshot."""
    lines = text_content.split('\n')
    # Remove empty lines at the end
    while lines and not lines[-1].strip():
        lines.pop()
    
    height = max(150, line_height * (len(lines) + 3))
    
    # Escape HTML
    escaped_lines = [html.escape(line) for line in lines]
    escaped_text = '\n'.join(escaped_lines)
    
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">
  <!-- Background -->
  <rect width="100%" height="100%" fill="#1e1e1e"/>
  
  <!-- Header -->
  <rect width="100%" height="30" fill="#0d47a1"/>
  <text x="10" y="20" font-family="Segoe UI, Arial" font-size="12" fill="white" font-weight="bold">Terminal Output</text>
  
  <!-- Content area -->
  <rect x="0" y="30" width="100%" height="{height - 30}" fill="#1e1e1e" stroke="#444" stroke-width="1"/>
  
  <!-- Text content -->
  <foreignObject x="15" y="40" width="{width - 30}" height="{height - 50}">
    <body xmlns="http://www.w3.org/1999/xhtml" style="margin:0; padding:0;">
      <pre style="font-family: 'Courier New', monospace; font-size: 12px; color: #00ff00; line-height: 1.5; margin: 0; padding: 0; word-wrap: break-word; white-space: pre-wrap;">{escaped_text}</pre>
    </body>
  </foreignObject>
</svg>
"""
    return svg

# Get the reports directory
reports_dir = Path('reports')
screenshots_dir = reports_dir / 'screenshots'
screenshots_dir.mkdir(parents=True, exist_ok=True)

# Files to convert
files_to_convert = [
    ('01-git-status-clean.txt', 'git-status-initial.svg'),
    ('04-git-status-conflict.txt', 'git-status-conflict.svg'),
    ('05-git-diff-conflict.txt', 'git-diff-conflict.svg'),
    ('06-git-log-postmerge.txt', 'git-log-graph.svg'),
    ('07-tags-list.txt', 'git-tags-list.svg'),
]

for src_file, dst_file in files_to_convert:
    src_path = reports_dir / src_file
    dst_path = screenshots_dir / dst_file
    
    if src_path.exists():
        text = src_path.read_text(encoding='utf-8')
        svg = text_to_svg_screenshot(text, width=1100)
        dst_path.write_text(svg, encoding='utf-8')
        print(f"Generated: {dst_file}")
    else:
        print(f"Skipped (not found): {src_file}")

print(f"\nScreenshots generated in: {screenshots_dir}")
