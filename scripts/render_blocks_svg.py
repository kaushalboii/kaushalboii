#!/usr/bin/env python3
"""
Render Kaushal's Creative Community & System Building Blocks as a terminal-window SVG.
Matches the design specs of stats.svg, contrib-heatmap.svg, and kaushal-ascii.svg.

Canvas: 860 x 530
Palette: #0d1117 (bg), #111722 (bg2), #161b22 (tile), #30363d (frame),
         #7d8590 (muted), #e6edf3 (ink), #39d353 (terminal green), #22d3ee (cyan)

Usage:
    python scripts/render_blocks_svg.py [output.svg]
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "building-blocks.svg")

W, H = 860, 530

CARDS = [
    {
        "id": "01",
        "title": "MOBILE ARCHITECTURE",
        "badge": "SWIFTUI · FLUTTER · KOTLIN",
        "badge_color": "#22d3ee",
        "badge_bg": "rgba(34, 211, 238, 0.12)",
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
        "badge_bg": "rgba(57, 211, 83, 0.12)",
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
        "badge_bg": "rgba(34, 211, 238, 0.12)",
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
        "badge_bg": "rgba(242, 204, 96, 0.12)",
        "lines": [
            ("├──", "Modular UI Kits & Interactive Specs"),
            ("├──", "Storytelling through Code & Motion"),
            ("└──", "Building in Public & Developer Culture")
        ],
        "metric_label": "COMMUNITY",
        "metric_val": "Open Collaboration"
    }
]

def generate_svg():
    svg_parts = []
    
    # Header & Styles
    svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#111722"/>
    <stop offset="100%" stop-color="#0d1117"/>
  </linearGradient>
  <linearGradient id="card-grad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#19202c"/>
    <stop offset="100%" stop-color="#131922"/>
  </linearGradient>
</defs>
<style>
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
  }}
</style>

<!-- Terminal Window Background -->
<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="#30363d" stroke-width="1"/>

<!-- Titlebar -->
<line x1="0" y1="32" x2="{W}" y2="32" stroke="#30363d"/>
<circle cx="20" cy="16" r="5" fill="#ff5f56"/>
<circle cx="36" cy="16" r="5" fill="#ffbd2e"/>
<circle cx="52" cy="16" r="5" fill="#27c93f"/>
<text x="{W/2}" y="20" fill="#7d8590" font-size="12" text-anchor="middle">kaushal@github: ~$ ./building-blocks.sh --status=active</text>

<!-- Sub-header status ribbon -->
<g class="card" style="animation-delay: 0.05s;">
  <circle cx="26" cy="53" r="4" fill="#39d353" class="pulse"/>
  <text x="36" y="57" fill="#39d353" font-size="11" font-weight="700">SYSTEM: ACTIVE</text>
  <text x="160" y="57" fill="#7d8590" font-size="11">● NODES: 4/4 INITIALIZED</text>
  <text x="340" y="57" fill="#7d8590" font-size="11">● ECOSYSTEM: CREATIVE COMMUNITY LABS</text>
  <text x="{W-24}" y="57" fill="#22d3ee" font-size="11" text-anchor="end">BUILD VERSION: 2026.11</text>
  <line x1="20" y1="68" x2="{W-20}" y2="68" stroke="#21262d" stroke-dasharray="3,3"/>
</g>
''')

    # Render Cards (2 x 2 grid)
    card_w = 398
    card_h = 178
    start_x = 22
    start_y = 80
    gap_x = 20
    gap_y = 16

    delays = [0.15, 0.25, 0.35, 0.45]

    for i, c in enumerate(CARDS):
        col = i % 2
        row = i // 2
        cx = start_x + col * (card_w + gap_x)
        cy = start_y + row * (card_h + gap_y)
        delay = delays[i]

        title_esc = html.escape(c["title"])
        badge_esc = html.escape(c["badge"])
        badge_w = len(c["badge"]) * 6.5 + 14

        svg_parts.append(f'''
<!-- Card {c["id"]} -->
<g class="card" style="animation-delay: {delay}s;">
  <rect x="{cx}" y="{cy}" width="{card_w}" height="{card_h}" rx="10" fill="url(#card-grad)" stroke="#30363d" stroke-width="1"/>
  
  <!-- Card Header -->
  <text x="{cx + 18}" y="{cy + 28}" fill="#7d8590" font-size="12" font-weight="700">[{c["id"]}]</text>
  <text x="{cx + 46}" y="{cy + 28}" fill="#e6edf3" font-size="13" font-weight="700">{title_esc}</text>
  
  <!-- Badge Pill -->
  <rect x="{cx + card_w - 18 - badge_w}" y="{cy + 14}" width="{badge_w}" height="20" rx="10" fill="{c['badge_bg']}" stroke="{c['badge_color']}" stroke-width="0.8"/>
  <text x="{cx + card_w - 18 - (badge_w / 2)}" y="{cy + 28}" fill="{c['badge_color']}" font-size="9.5" font-weight="700" text-anchor="middle">{badge_esc}</text>

  <line x1="{cx + 16}" y1="{cy + 42}" x2="{cx + card_w - 16}" y2="{cy + 42}" stroke="#21262d"/>
  
  <!-- Tree Lines -->
''')
        line_y = cy + 66
        for prefix, txt in c["lines"]:
            prefix_esc = html.escape(prefix)
            txt_esc = html.escape(txt)
            svg_parts.append(f'''  <text x="{cx + 18}" y="{line_y}" fill="#39d353" font-size="12">{prefix_esc}</text>
  <text x="{cx + 48}" y="{line_y}" fill="#c9d1d9" font-size="12">{txt_esc}</text>
''')
            line_y += 24

        metric_label_esc = html.escape(c["metric_label"])
        metric_val_esc = html.escape(c["metric_val"])

        # Metric Footer inside card
        svg_parts.append(f'''
  <!-- Card Footer -->
  <rect x="{cx + 16}" y="{cy + card_h - 32}" width="{card_w - 32}" height="22" rx="5" fill="#0d1117" stroke="#21262d"/>
  <text x="{cx + 26}" y="{cy + card_h - 18}" fill="#7d8590" font-size="10">{metric_label_esc}:</text>
  <text x="{cx + 115}" y="{cy + card_h - 18}" fill="#39d353" font-size="10" font-weight="700">{metric_val_esc}</text>
  <text x="{cx + card_w - 26}" y="{cy + card_h - 18}" fill="#22d3ee" font-size="10" text-anchor="end">READY</text>
</g>
''')

    # Bottom Terminal Prompt
    mission = html.escape('"Blending design, AI, and code to empower human experiences."')
    svg_parts.append(f'''
<!-- Bottom Mission Banner -->
<g class="card" style="animation-delay: 0.55s;">
  <rect x="22" y="474" width="{W - 44}" height="36" rx="8" fill="#0b0e14" stroke="#30363d"/>
  <text x="36" y="496" fill="#39d353" font-size="11.5" font-weight="700">kaushal@github:~$</text>
  <text x="175" y="496" fill="#7d8590" font-size="11.5">echo $COMMUNITY_MISSION</text>
  <text x="360" y="496" fill="#e6edf3" font-size="11.5">{mission}</text>
  <circle cx="{W - 38}" cy="492" r="3" fill="#22d3ee" class="pulse"/>
</g>

</svg>
''')

    return "".join(svg_parts)

if __name__ == "__main__":
    content = generate_svg()
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {OUT} ({len(content)} bytes)")
