#!/usr/bin/env python3
"""
Render Kaushal's Creative Community & System Building Blocks as a terminal-window SVG.
Supports both dark mode (building-blocks.svg with adaptive CSS) and light mode
(building-blocks-light.svg).

Usage:
    python scripts/render_blocks_svg.py [output.svg]
    If no args provided, automatically renders both building-blocks.svg and building-blocks-light.svg.
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DARK_OUT = os.path.join(HERE, "..", "building-blocks.svg")
DEFAULT_LIGHT_OUT = os.path.join(HERE, "..", "building-blocks-light.svg")

W, H = 860, 530

CARDS = [
    {
        "id": "01",
        "title": "MOBILE ARCHITECTURE",
        "badge": "SWIFTUI · FLUTTER · KOTLIN",
        "badge_color": "#22d3ee",
        "badge_color_light": "#0969da",
        "lines": [
            ("├──", "SwiftUI Native & Jetpack Compose"),
            ("├──", "Kinetic Motion & Micro-Interactions"),
            ("└──", "Offline-First State & Sync Engines")
        ],
        "metric_label": "DEPLOYMENTS",
        "metric_val": "12+ Apps Shipped"
    },
    {
        "id": "02",
        "title": "INTELLIGENT AGENTS",
        "badge": "PYTHON · AGENTS · FASTAPI",
        "badge_color": "#39d353",
        "badge_color_light": "#1a7f37",
        "lines": [
            ("├──", "Autonomous LLM Workflow Loops"),
            ("├──", "Dynamic SVG & Canvas Generators"),
            ("└──", "Multimodal Context & Vision Tools")
        ],
        "metric_label": "CAPABILITY",
        "metric_val": "System Automations"
    },
    {
        "id": "03",
        "title": "FULL-STACK & SYSTEMS",
        "badge": "NODE · DOCKER · POSTGRES",
        "badge_color": "#22d3ee",
        "badge_color_light": "#0969da",
        "lines": [
            ("├──", "High-Throughput Microservices"),
            ("├──", "PostgreSQL & Redis Event Streams"),
            ("└──", "Dockerized Container Deployments")
        ],
        "metric_label": "ARCHITECTURE",
        "metric_val": "Distributed & Scalable"
    },
    {
        "id": "04",
        "title": "CREATIVE COMMUNITY LAB",
        "badge": "OPEN SOURCE · COLLAB",
        "badge_color": "#f2cc60",
        "badge_color_light": "#b45309",
        "lines": [
            ("├──", "Modular UI Kits & Interactive Specs"),
            ("├──", "Storytelling through Code & Motion"),
            ("└──", "Building in Public & Developer Culture")
        ],
        "metric_label": "COMMUNITY",
        "metric_val": "Open Collaboration"
    }
]


def generate_svg(theme="dark"):
    is_light = (theme == "light")
    scheme = "light" if is_light else "light dark"

    if is_light:
        bg1, bg2 = "#ffffff", "#f6f8fa"
        card1, card2 = "#ffffff", "#f6f8fa"
        frame_col = "#d0d7de"
        muted_col = "#57606a"
        ink_col = "#1f2328"
        cyan_col = "#0969da"
        green_col = "#1a7f37"
    else:
        bg1, bg2 = "#111722", "#0d1117"
        card1, card2 = "#19202c", "#131922"
        frame_col = "#30363d"
        muted_col = "#7d8590"
        ink_col = "#e6edf3"
        cyan_col = "#22d3ee"
        green_col = "#39d353"

    svg_parts = []
    svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="color-scheme: {scheme};" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{bg1}"/>
    <stop offset="100%" stop-color="{bg2}"/>
  </linearGradient>
  <linearGradient id="card-grad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{card1}"/>
    <stop offset="100%" stop-color="{card2}"/>
  </linearGradient>''')

    if not is_light:
        svg_parts.append('''  <linearGradient id="bg-light" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#ffffff"/>
    <stop offset="100%" stop-color="#f6f8fa"/>
  </linearGradient>
  <linearGradient id="card-grad-light" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#ffffff"/>
    <stop offset="100%" stop-color="#f6f8fa"/>
  </linearGradient>''')

    svg_parts.append(f'''</defs>
<style>
  :root {{ color-scheme: {scheme}; }}
  .card {{ opacity: 0; animation: in 0.45s ease-out both; }}
  .pulse {{ animation: blink 2s infinite ease-in-out; }}
  @keyframes in {{
    0% {{ opacity: 0; transform: translateY(14px); }}
    100% {{ opacity: 1; transform: translateY(0); }}
  }}
  @keyframes blink {{
    0%, 100% {{ opacity: 0.35; }}
    50% {{ opacity: 1; }}
  }}
  @media (prefers-reduced-motion: reduce) {{
    .card, .pulse {{ animation: none !important; opacity: 1 !important; transform: none !important; }}
  }}''')

    if not is_light:
        svg_parts.append('''  @media (prefers-color-scheme: light) {
    .win-bg { fill: url(#bg-light) !important; }
    .frame-col { stroke: #d0d7de !important; }
    .card-grad-fill { fill: url(#card-grad-light) !important; stroke: #d0d7de !important; }
    .txt-muted { fill: #57606a !important; }
    .txt-ink, .txt-muted .txt-ink { fill: #1f2328 !important; }
    .hud-cyan { stroke: #0969da !important; }
    .bracket-cyan { fill: #0969da !important; }
    .dot-fill { fill: #1a7f37 !important; }
    .txt-green { fill: #1a7f37 !important; }
    .badge-box-0 { fill: #0969da1a !important; }
    .badge-txt-0 { fill: #0969da !important; }
    .badge-box-1 { fill: #1a7f371a !important; }
    .badge-txt-1 { fill: #1a7f37 !important; }
    .badge-box-2 { fill: #8250df1a !important; }
    .badge-txt-2 { fill: #8250df !important; }
    .badge-box-3 { fill: #b453091a !important; }
    .badge-txt-3 { fill: #b45309 !important; }
    .metric-val-0 { fill: #0969da !important; }
    .metric-val-1 { fill: #1a7f37 !important; }
    .metric-val-2 { fill: #8250df !important; }
    .metric-val-3 { fill: #b45309 !important; }
  }''')

    svg_parts.append(f'''</style>

<!-- Terminal Window Background -->
<rect class="win-bg" width="{W}" height="{H}" rx="12" fill="url(#bg)"/>
<rect class="frame-col" x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{frame_col}" stroke-width="1"/>

<!-- Titlebar -->
<line class="frame-col" x1="0" y1="32" x2="{W}" y2="32" stroke="{frame_col}"/>
<circle cx="20" cy="16" r="5" fill="#ff5f56"/>
<circle cx="36" cy="16" r="5" fill="#ffbd2e"/>
<circle cx="52" cy="16" r="5" fill="#27c93f"/>

<!-- Terminal Command Title -->
<text class="txt-muted" x="{W/2}" y="21" fill="{muted_col}" font-size="12" text-anchor="middle">kaushal@dev-station: ~$ ./building-blocks.sh --status=active</text>

<!-- Top Right System Status Pulse -->
<g transform="translate({W - 135}, 16)">
  <circle cx="0" cy="0" r="4" fill="{green_col}" class="dot-fill pulse"/>
  <circle cx="0" cy="0" r="2" fill="{green_col}" class="dot-fill"/>
  <text class="txt-green" x="10" y="3.5" fill="{green_col}" font-size="10" font-weight="700" letter-spacing="1">SYSTEM OK</text>
</g>

<!-- Tech Crosshairs / HUD brackets -->
<path class="hud-cyan" d="M 22 46 L 34 46 M 22 46 L 22 58" stroke="{cyan_col}" stroke-width="1.5" fill="none" opacity="0.6"/>
<path class="hud-cyan" d="M {W-22} 46 L {W-34} 46 M {W-22} 46 L {W-22} 58" stroke="{cyan_col}" stroke-width="1.5" fill="none" opacity="0.6"/>
<path class="hud-cyan" d="M 22 {H-22} L 34 {H-22} M 22 {H-22} L 22 {H-34}" stroke="{cyan_col}" stroke-width="1.5" fill="none" opacity="0.6"/>
<path class="hud-cyan" d="M {W-22} {H-22} L {W-34} {H-22} M {W-22} {H-22} L {W-22} {H-34}" stroke="{cyan_col}" stroke-width="1.5" fill="none" opacity="0.6"/>
''')

    # Card Grid layout: 2 cols x 2 rows
    COLS, ROWS_COUNT = 2, 2
    PAD_X, PAD_Y = 22, 50
    GAP_X, GAP_Y = 16, 16
    CARD_W = (W - PAD_X * 2 - GAP_X * (COLS - 1)) / COLS
    CARD_H = (H - PAD_Y - 24 - GAP_Y * (ROWS_COUNT - 1)) / ROWS_COUNT

    delays = [0.08, 0.20, 0.32, 0.44]

    for i, c in enumerate(CARDS):
        row = i // COLS
        col = i % COLS
        x = PAD_X + col * (CARD_W + GAP_X)
        y = PAD_Y + row * (CARD_H + GAP_Y)
        delay = delays[i]
        badge_c = c["badge_color_light"] if is_light else c["badge_color"]
        badge_bg = f"{badge_c}1a"

        svg_parts.append(f'''
<!-- Card {c["id"]} -->
<g class="card" style="animation-delay: {delay}s">
  <rect class="card-grad-fill" x="{x}" y="{y}" width="{CARD_W}" height="{CARD_H}" rx="8" fill="url(#card-grad)" stroke="{frame_col}" stroke-width="1"/>
  
  <!-- Index Number -->
  <text class="bracket-cyan" x="{x + 18}" y="{y + 32}" fill="{cyan_col}" font-size="12" font-weight="700">[{c["id"]}]</text>
  
  <!-- Card Title -->
  <text class="txt-ink" x="{x + 46}" y="{y + 32}" fill="{ink_col}" font-size="13" font-weight="700" letter-spacing="1">{html.escape(c["title"])}</text>
  
  <!-- Stack / Tech Badge -->
  <rect class="badge-box-{i}" x="{x + CARD_W - 170}" y="{y + 18}" width="154" height="20" rx="4" fill="{badge_bg}"/>
  <text class="badge-txt-{i}" x="{x + CARD_W - 93}" y="{y + 32}" fill="{badge_c}" font-size="9" font-weight="700" text-anchor="middle" letter-spacing="0.5">{c["badge"]}</text>

  <!-- Divider Line -->
  <line class="frame-col" x1="{x + 16}" y1="{y + 46}" x2="{x + CARD_W - 16}" y2="{y + 46}" stroke="{frame_col}" stroke-width="1" stroke-dasharray="3,3"/>
''')
        # Content lines
        for line_idx, (tree_sym, text) in enumerate(c["lines"]):
            ly = y + 74 + line_idx * 25
            svg_parts.append(f'''  <text class="txt-muted" x="{x + 18}" y="{ly}" fill="{muted_col}" font-size="11">{tree_sym} <tspan class="txt-ink" fill="{ink_col}">{html.escape(text)}</tspan></text>''')

        # Card Footer Metric
        svg_parts.append(f'''
  <!-- Card Footer -->
  <line class="frame-col" x1="{x + 16}" y1="{y + CARD_H - 34}" x2="{x + CARD_W - 16}" y2="{y + CARD_H - 34}" stroke="{frame_col}" stroke-width="1"/>
  <text class="txt-muted" x="{x + 18}" y="{y + CARD_H - 16}" fill="{muted_col}" font-size="9" font-weight="700" letter-spacing="1">METRIC // {c["metric_label"]}:</text>
  <text class="metric-val-{i}" x="{x + CARD_W - 18}" y="{y + CARD_H - 16}" fill="{badge_c}" font-size="10" font-weight="700" text-anchor="end">{html.escape(c["metric_val"])}</text>
</g>
''')

    svg_parts.append("</svg>")
    return "\n".join(svg_parts)


def main():
    custom_out = sys.argv[1] if len(sys.argv) > 1 else None

    if custom_out:
        theme = "light" if "light" in custom_out.lower() else "dark"
        svg = generate_svg(theme=theme)
        with open(custom_out, "w") as f:
            f.write(svg)
        print(f"wrote {custom_out}: {W} x {H}, {len(svg)} bytes ({theme} mode)")
    else:
        dark_svg = generate_svg(theme="dark")
        with open(DEFAULT_DARK_OUT, "w") as f:
            f.write(dark_svg)
        print(f"wrote {DEFAULT_DARK_OUT}: {W} x {H}, {len(dark_svg)} bytes (dark mode + adaptive CSS)")

        light_svg = generate_svg(theme="light")
        with open(DEFAULT_LIGHT_OUT, "w") as f:
            f.write(light_svg)
        print(f"wrote {DEFAULT_LIGHT_OUT}: {W} x {H}, {len(light_svg)} bytes (light mode)")


if __name__ == "__main__":
    main()
