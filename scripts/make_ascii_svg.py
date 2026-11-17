"""
Convert a portrait photo into a CLEAN, monochrome ASCII-art SVG that "types"
itself in like a terminal, then holds.

Supports both dark mode (kaushal-ascii.svg with adaptive CSS) and light mode
(kaushal-ascii-light.svg with GitHub Primer light palette).

GitHub renders SVGs embedded via <img> or <picture> and runs their SMIL animations.
Each row is revealed with a left-to-right clip wipe plus a small block cursor
riding the wipe edge, staggered top -> bottom, so the whole portrait prints once
and freezes.

Usage:
    python scripts/make_ascii_svg.py [input.png] [output.svg]
    If no custom output path is provided, automatically generates both kaushal-ascii.svg
    and kaushal-ascii-light.svg.
"""
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SRC = os.path.join(HERE, "..", "source-prepped.png")
DEFAULT_DARK_OUT = os.path.join(HERE, "..", "kaushal-ascii.svg")
DEFAULT_LIGHT_OUT = os.path.join(HERE, "..", "kaushal-ascii-light.svg")

COLS = int(os.environ.get("COLS", 180))
ART_W_TARGET = 800
CELL_W = ART_W_TARGET / COLS
CELL_H = CELL_W * 15 / 8
ROWS = round(COLS * 8 / 15)
RAMP = " .`:-=+*cs#%@"  # bright(sparse) -> dark(dense); leading space clears bg

CONTRAST = 1.05
BRIGHTNESS = 1.0
GAMMA = 1.18          # >1 brightens mids -> face lands in sparser chars
SHARPEN = False
WHITE_FLOOR = 0.80    # luminance above this is forced to blank (space)

PAD = 20
TITLEBAR_H = 30
STATUS_H = 30
ART_W = COLS * CELL_W
ART_H = ROWS * CELL_H
CANVAS_W = ART_W + PAD * 2
CANVAS_H = TITLEBAR_H + ART_H + STATUS_H + PAD

ROW_DUR = 5.8 / ROWS  # whole portrait prints in ~6s at any resolution
STAGGER = ROW_DUR     # single cursor sweeping down
STATIC = bool(os.environ.get("STATIC"))


def sample_image_to_ascii(src_path):
    im = Image.open(src_path).convert("L")
    if SHARPEN:
        im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=140, threshold=2))
    im = ImageEnhance.Brightness(im).enhance(BRIGHTNESS)
    im = ImageEnhance.Contrast(im).enhance(CONTRAST)
    im = im.resize((COLS, ROWS), Image.LANCZOS)
    px = im.load()

    rows_txt = []
    for y in range(ROWS):
        chars = []
        for x in range(COLS):
            lum = px[x, y] / 255.0
            lum = pow(lum, GAMMA)
            if lum >= WHITE_FLOOR:
                chars.append(" ")
                continue
            idx = int((1.0 - lum) * (len(RAMP) - 1) + 0.5)
            idx = max(0, min(len(RAMP) - 1, idx))
            chars.append(RAMP[idx])
        rows_txt.append("".join(chars))
    return rows_txt


def build_ascii_svg(rows_txt, theme="dark"):
    is_light = (theme == "light")

    if is_light:
        bg1, bg2 = "#ffffff", "#f6f8fa"
        frame_col = "#d0d7de"
        title_text = "#57606a"
        ink_col = "#1f2328"
        cursor_col = "#0969da"
        name_col = "#0969da"
    else:
        bg1, bg2 = "#111722", "#0d1117"
        frame_col = "#30363d"
        title_text = "#7d8590"
        ink_col = "#c9d1d9"
        cursor_col = "#c9d1d9"
        name_col = "#c9d1d9"

    art_top = TITLEBAR_H + PAD * 0.35
    scheme = "light" if is_light else "light dark"

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
        f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" style="color-scheme: {scheme};" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace">',
        '<style>',
        f':root {{ color-scheme: {scheme}; }}',
    ]

    if not is_light:
        parts.extend([
            '@media (prefers-color-scheme: light) {',
            '  .win-bg { fill: url(#bg-light) !important; }',
            '  .win-frame { stroke: #d0d7de !important; }',
            '  .win-title { fill: #57606a !important; }',
            '  .ascii-ink { fill: #1f2328 !important; }',
            '  .ascii-cursor { fill: #0969da !important; }',
            '  .status-txt { fill: #57606a !important; }',
            '  .status-name, .status-txt .status-name { fill: #0969da !important; }',
            '  .status-cursor { fill: #0969da !important; }',
            '}',
        ])

    parts.append('</style>')
    parts.append('<defs>')
    parts.append(f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
                 f'<stop offset="0" stop-color="{bg1}"/><stop offset="1" stop-color="{bg2}"/>'
                 f'</linearGradient>')
    if not is_light:
        parts.append('<linearGradient id="bg-light" x1="0" y1="0" x2="0" y2="1">'
                     '<stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#f6f8fa"/>'
                     '</linearGradient>')
    parts.append('</defs>')

    # Window shell
    parts.append(f'<rect class="win-bg" width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#bg)"/>')
    parts.append(f'<rect class="win-frame" x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" '
                 f'fill="none" stroke="{frame_col}" stroke-width="1"/>')
    parts.append(f'<line class="win-frame" x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{frame_col}"/>')

    # Traffic lights
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

    parts.append(f'<text class="win-title" x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{title_text}" font-size="12" '
                 f'text-anchor="middle">kaushal@github: ~$ ./portrait.sh</text>')

    font_size = CELL_H * 0.86
    for ry, line in enumerate(rows_txt):
        y = art_top + ry * CELL_H + CELL_H * 0.74
        row_y = art_top + ry * CELL_H
        delay = ry * STAGGER
        safe = html.escape(line)
        text = (f'<text class="ascii-ink" xml:space="preserve" x="{PAD}" y="{y:.1f}" fill="{ink_col}" '
                f'font-size="{font_size:.1f}" textLength="{ART_W}" lengthAdjust="spacing">{safe}</text>')

        if STATIC:
            parts.append(text)
            continue

        parts.append(
            f'<clipPath id="r{ry}"><rect x="{PAD}" y="{row_y:.1f}" height="{CELL_H}" width="0">'
            f'<animate attributeName="width" from="0" to="{ART_W}" begin="{delay:.3f}s" '
            f'dur="{ROW_DUR:.2f}s" fill="freeze"/></rect></clipPath>'
        )
        parts.append(f'<g clip-path="url(#r{ry})">{text}</g>')
        parts.append(
            f'<rect class="ascii-cursor" y="{row_y+1:.1f}" width="{CELL_W}" height="{CELL_H-2}" fill="{cursor_col}" opacity="0">'
            f'<animate attributeName="x" from="{PAD}" to="{PAD+ART_W}" begin="{delay:.3f}s" '
            f'dur="{ROW_DUR:.2f}s" fill="freeze"/>'
            f'<set attributeName="opacity" to="0.85" begin="{delay:.3f}s"/>'
            f'<set attributeName="opacity" to="0" begin="{delay+ROW_DUR:.3f}s"/></rect>'
        )

    # Status bar with blinking cursor
    status_line_y = TITLEBAR_H + ART_H + PAD * 0.35
    status_y = status_line_y + 19
    parts.append(f'<line class="win-frame" x1="0" y1="{status_line_y:.1f}" x2="{CANVAS_W}" y2="{status_line_y:.1f}" stroke="{frame_col}"/>')
    parts.append(f'<text class="status-txt" x="{PAD}" y="{status_y:.1f}" fill="{title_text}" font-size="13">'
                 f'kaushal@github:~$ whoami <tspan class="status-name" fill="{name_col}">Kaushal Maran</tspan></text>')
    status_chars = len("kaushal@github:~$ whoami Kaushal Maran ")
    parts.append(f'<rect class="status-cursor" x="{PAD + status_chars * 13 * 0.6:.1f}" y="{status_y-12:.1f}" width="8" height="14" fill="{cursor_col}">'
                 f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" '
                 f'dur="1s" repeatCount="indefinite"/></rect>')

    parts.append("</svg>")
    return "".join(parts)


def main():
    src = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else DEFAULT_SRC
    custom_out = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(src):
        print(f"Error: {src} not found")
        sys.exit(1)

    rows = sample_image_to_ascii(src)

    if custom_out:
        theme = "light" if "light" in custom_out.lower() else "dark"
        svg = build_ascii_svg(rows, theme=theme)
        with open(custom_out, "w") as f:
            f.write(svg)
        print(f"wrote {custom_out}: {len(svg)} bytes; {CANVAS_W} x {CANVAS_H} ({theme} mode)")
    else:
        dark_svg = build_ascii_svg(rows, theme="dark")
        with open(DEFAULT_DARK_OUT, "w") as f:
            f.write(dark_svg)
        print(f"wrote {DEFAULT_DARK_OUT}: {len(dark_svg)} bytes; {CANVAS_W} x {CANVAS_H} (dark mode + adaptive CSS)")

        light_svg = build_ascii_svg(rows, theme="light")
        with open(DEFAULT_LIGHT_OUT, "w") as f:
            f.write(light_svg)
        print(f"wrote {DEFAULT_LIGHT_OUT}: {len(light_svg)} bytes; {CANVAS_W} x {CANVAS_H} (light mode)")


if __name__ == "__main__":
    main()
