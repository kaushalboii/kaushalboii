#!/usr/bin/env python3
"""
Render Kaushal's developer system telemetry, identity, and deployment logs
as a terminal-window SVG that matches the dark cyberpunk aesthetic of stats.svg
and kaushal-ascii.svg.

Usage:
    python scripts/render_dev_system_svg.py [output.svg]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "dev-system.svg")

W, H = 860, 520
PAD = 20
TITLEBAR_H = 32

BG = "#0d1117"
BG2 = "#111722"
CARD_BG = "#161b22"
FRAME = "#30363d"
FRAME_ACCENT = "#1f6feb"
MUTED = "#7d8590"
TEXT = "#e6edf3"
GREEN = "#39d353"
CYAN = "#38bdf8"
AMBER = "#f59e0b"
PURPLE = "#a855f7"

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace">',
    '<style>',
    '  .fade-in { opacity: 0; animation: fadeIn 0.5s ease-out both; }',
    '  .pulse-fast { animation: pulse 1.8s ease-in-out infinite; }',
    '  .pulse-glow { animation: pulseGlow 2.2s ease-in-out infinite; }',
    '  .cursor { animation: blink 1s step-start infinite; }',
    '  .bar-grow { transform-box: fill-box; transform-origin: left; animation: barGrow 1.2s cubic-bezier(0.16, 1, 0.3, 1) both; }',
    '  @keyframes fadeIn { 0% { opacity: 0; transform: translateY(8px); } 100% { opacity: 1; transform: translateY(0); } }',
    '  @keyframes pulse { 0%, 100% { opacity: 0.95; transform: scale(1); } 50% { opacity: 0.45; transform: scale(0.92); } }',
    '  @keyframes pulseGlow { 0% { r: 3.5px; opacity: 0.9; } 50% { r: 8px; opacity: 0; } 100% { r: 3.5px; opacity: 0.9; } }',
    '  @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }',
    '  @keyframes barGrow { 0% { transform: scaleX(0); } 100% { transform: scaleX(1); } }',
    '  @media (prefers-reduced-motion: reduce) {',
    '    .fade-in, .bar-grow { opacity: 1 !important; transform: none !important; animation: none !important; }',
    '    .pulse-fast, .pulse-glow, .cursor { animation: none !important; }',
    '  }',
    '</style>',
    '<defs>',
    f'  <linearGradient id="win-bg" x1="0" y1="0" x2="0" y2="1">',
    f'    <stop offset="0%" stop-color="{BG2}"/>',
    f'    <stop offset="100%" stop-color="{BG}"/>',
    '  </linearGradient>',
    '  <linearGradient id="bar-grad" x1="0" y1="0" x2="1" y2="0">',
    f'    <stop offset="0%" stop-color="{CYAN}"/>',
    f'    <stop offset="100%" stop-color="{GREEN}"/>',
    '  </linearGradient>',
    '  <linearGradient id="accent-edge" x1="0" y1="0" x2="0" y2="1">',
    f'    <stop offset="0%" stop-color="{CYAN}" stop-opacity="0.8"/>',
    f'    <stop offset="100%" stop-color="{GREEN}" stop-opacity="0.2"/>',
    '  </linearGradient>',
    '</defs>',
    # Window shell
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#win-bg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]

# Traffic lights
for i, col in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{col}"/>')

# Titlebar
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
             f'text-anchor="middle">kaushal@dev-station: ~$ systemctl status kaushal.profile</text>')

# Live System Badge
parts.append(
    f'<g transform="translate({W - 145}, {TITLEBAR_H/2})">'
    f'  <circle cx="0" cy="0" r="3.5" fill="{GREEN}"/>'
    f'  <circle cx="0" cy="0" r="3.5" fill="none" stroke="{GREEN}" stroke-width="1.5" class="pulse-glow"/>'
    f'  <text x="12" y="3.5" fill="{GREEN}" font-size="11" font-weight="700" letter-spacing="1">SYSTEM ONLINE</text>'
    f'</g>'
)

# HUD Tech Crosshairs / Corner brackets
parts.append(f'<path d="M 22 44 L 34 44 M 22 44 L 22 56" stroke="{CYAN}" stroke-width="1.5" fill="none" opacity="0.6"/>')
parts.append(f'<path d="M {W-22} 44 L {W-34} 44 M {W-22} 44 L {W-22} 56" stroke="{CYAN}" stroke-width="1.5" fill="none" opacity="0.6"/>')
parts.append(f'<path d="M 22 {H-22} L 34 {H-22} M 22 {H-22} L 22 {H-34}" stroke="{CYAN}" stroke-width="1.5" fill="none" opacity="0.6"/>')
parts.append(f'<path d="M {W-22} {H-22} L {W-34} {H-22} M {W-22} {H-22} L {W-22} {H-34}" stroke="{CYAN}" stroke-width="1.5" fill="none" opacity="0.6"/>')

# ==================== LEFT COLUMN: CORE IDENTITY & STACK ====================
left_x = 22
left_y = 48
left_w = 428
left_h = H - left_y - 20

parts.append(f'<g class="fade-in" style="animation-delay: 0.1s">')
parts.append(f'  <rect x="{left_x}" y="{left_y}" width="{left_w}" height="{left_h}" rx="10" '
             f'fill="{CARD_BG}" stroke="{FRAME}"/>')
# Header
parts.append(f'  <text x="{left_x + 18}" y="{left_y + 28}" fill="{CYAN}" font-size="13" font-weight="700" letter-spacing="1.2">⚡ INITIALIZING DEV SYSTEM</text>')
parts.append(f'  <text x="{left_x + left_w - 18}" y="{left_y + 28}" fill="{GREEN}" font-size="11" text-anchor="end">BOOT: 100%</text>')

# Boot Progress Bar
bar_x = left_x + 18
bar_y = left_y + 40
bar_w = left_w - 36
bar_h = 6
parts.append(f'  <rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="3" fill="#21262d"/>')
parts.append(f'  <rect class="bar-grow" x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="3" fill="url(#bar-grad)"/>')

# Divider
parts.append(f'  <line x1="{left_x + 18}" y1="{left_y + 60}" x2="{left_x + left_w - 18}" y2="{left_y + 60}" stroke="{FRAME}" stroke-dasharray="3,3"/>')

# Identity section
parts.append(f'  <text x="{left_x + 18}" y="{left_y + 82}" fill="{MUTED}" font-size="11" font-weight="700" letter-spacing="1">🧠 CORE IDENTITY</text>')
parts.append(f'  <text x="{left_x + 18}" y="{left_y + 106}" fill="{TEXT}" font-size="19" font-weight="700">Kaushal Maran</text>')

# Role pill
pill_x = left_x + 18
pill_y = left_y + 118
parts.append(f'  <rect x="{pill_x}" y="{pill_y}" width="205" height="22" rx="11" fill="#1f6feb22" stroke="#388bfd"/>')
parts.append(f'  <text x="{pill_x + 10}" y="{pill_y + 15}" fill="#58a6ff" font-size="11" font-weight="600">Mobile Application Developer</text>')

# Mode indicator
mode_x = pill_x + 215
parts.append(f'  <rect x="{mode_x}" y="{pill_y}" width="90" height="22" rx="11" fill="#23863622" stroke="#2ea043"/>')
parts.append(f'  <circle cx="{mode_x + 12}" cy="{pill_y + 11}" r="3" fill="{GREEN}"/>')
parts.append(f'  <text x="{mode_x + 22}" y="{pill_y + 15}" fill="{GREEN}" font-size="11" font-weight="600">ACTIVE</text>')

# System Configuration / Stack
parts.append(f'  <line x1="{left_x + 18}" y1="{left_y + 156}" x2="{left_x + left_w - 18}" y2="{left_y + 156}" stroke="{FRAME}"/>')
parts.append(f'  <text x="{left_x + 18}" y="{left_y + 178}" fill="{MUTED}" font-size="11" font-weight="700" letter-spacing="1">⚙️ PRIMARY STACK</text>')

# Stack Cards
# iOS Card
c1_y = left_y + 192
parts.append(f'  <rect x="{left_x + 18}" y="{c1_y}" width="{left_w - 36}" height="56" rx="8" fill="#0d1117" stroke="{FRAME}"/>')
parts.append(f'  <text x="{left_x + 30}" y="{c1_y + 24}" fill="{TEXT}" font-size="13" font-weight="700">📱 iOS Development</text>')
parts.append(f'  <text x="{left_x + 30}" y="{c1_y + 44}" fill="{MUTED}" font-size="11">SwiftUI · Swift · Combine · Xcode · UIKit</text>')
parts.append(f'  <circle cx="{left_x + left_w - 34}" cy="{c1_y + 28}" r="4" fill="{GREEN}"/>')

# Android Card
c2_y = c1_y + 64
parts.append(f'  <rect x="{left_x + 18}" y="{c2_y}" width="{left_w - 36}" height="56" rx="8" fill="#0d1117" stroke="{FRAME}"/>')
parts.append(f'  <text x="{left_x + 30}" y="{c2_y + 24}" fill="{TEXT}" font-size="13" font-weight="700">🤖 Android Development</text>')
parts.append(f'  <text x="{left_x + 30}" y="{c2_y + 44}" fill="{MUTED}" font-size="11">Kotlin · Jetpack Compose · Coroutines · Flow · Studio</text>')
parts.append(f'  <circle cx="{left_x + left_w - 34}" cy="{c2_y + 28}" r="4" fill="{GREEN}"/>')

# Secondary Capabilities
cap_y = c2_y + 72
parts.append(f'  <text x="{left_x + 18}" y="{cap_y + 14}" fill="{MUTED}" font-size="11" font-weight="700" letter-spacing="1">🎨 SECONDARY CAPABILITIES</text>')

caps = [
    ("🎨 UI/UX Engineering", "→ Figma → Production UI"),
    ("⚡ Performance &amp; Arch", "→ MVVM / MVI · Clean Arch"),
    ("🔗 Integrations", "→ APIs · Firebase · CI/CD"),
]
for j, (title, desc) in enumerate(caps):
    cy = cap_y + 30 + j * 26
    parts.append(f'  <text x="{left_x + 22}" y="{cy}" fill="{TEXT}" font-size="11" font-weight="600">{title}</text>')
    parts.append(f'  <text x="{left_x + 180}" y="{cy}" fill="{MUTED}" font-size="11">{desc}</text>')

parts.append('</g>')

# ==================== RIGHT TOP: DEPLOYMENT TELEMETRY ====================
right_x = left_x + left_w + 14
right_w = W - right_x - 22
rt_y = left_y
rt_h = 195

parts.append(f'<g class="fade-in" style="animation-delay: 0.25s">')
parts.append(f'  <rect x="{right_x}" y="{rt_y}" width="{right_w}" height="{rt_h}" rx="10" '
             f'fill="{CARD_BG}" stroke="{FRAME}"/>')
parts.append(f'  <text x="{right_x + 18}" y="{rt_y + 28}" fill="{CYAN}" font-size="13" font-weight="700" letter-spacing="1.2">📊 DEPLOYMENT LOGS</text>')
parts.append(f'  <text x="{right_x + right_w - 18}" y="{rt_y + 28}" fill="{GREEN}" font-size="11" text-anchor="end">STATUS: STABLE</text>')

# 3 metric tiles in a row
tile_w = (right_w - 36 - 16) / 3
tile_h = 76
metrics = [
    ("10+", "Android Apps", "Deployed &amp; Live", GREEN),
    ("2", "iOS Apps", "App Store / SwiftUI", CYAN),
    ("100%", "Releases", "Zero Downtime", AMBER),
]

for i, (val, title, caption, accent) in enumerate(metrics):
    tx = right_x + 18 + i * (tile_w + 8)
    ty = rt_y + 44
    parts.append(f'  <rect x="{tx:.1f}" y="{ty}" width="{tile_w:.1f}" height="{tile_h}" rx="8" fill="#0d1117" stroke="{FRAME}"/>')
    parts.append(f'  <text x="{tx + tile_w/2:.1f}" y="{ty + 34}" fill="{accent}" font-size="24" font-weight="700" text-anchor="middle">{val}</text>')
    parts.append(f'  <text x="{tx + tile_w/2:.1f}" y="{ty + 52}" fill="{TEXT}" font-size="11" font-weight="600" text-anchor="middle">{title}</text>')
    parts.append(f'  <text x="{tx + tile_w/2:.1f}" y="{ty + 66}" fill="{MUTED}" font-size="9" text-anchor="middle">{caption}</text>')

# Verification / System Health line
parts.append(f'  <line x1="{right_x + 18}" y1="{rt_y + 134}" x2="{right_x + right_w - 18}" y2="{rt_y + 134}" stroke="{FRAME}"/>')
parts.append(f'  <text x="{right_x + 18}" y="{rt_y + 156}" fill="{GREEN}" font-size="12">✔ Production Releases: SUCCESSFUL</text>')
parts.append(f'  <text x="{right_x + right_w - 18}" y="{rt_y + 156}" fill="{MUTED}" font-size="11" text-anchor="end">Reliability: HIGH</text>')
parts.append(f'  <text x="{right_x + 18}" y="{rt_y + 178}" fill="{MUTED}" font-size="11">✔ Automated Pipelines: HEALTHY · Clean Code Standards</text>')
parts.append('</g>')

# ==================== RIGHT MIDDLE: CURRENT RUNTIME PROCESS ====================
rc_y = rt_y + rt_h + 12
rc_h = 155

parts.append(f'<g class="fade-in" style="animation-delay: 0.4s">')
parts.append(f'  <rect x="{right_x}" y="{rc_y}" width="{right_w}" height="{rc_h}" rx="10" '
             f'fill="{CARD_BG}" stroke="{FRAME}"/>')
parts.append(f'  <text x="{right_x + 18}" y="{rc_y + 26}" fill="{CYAN}" font-size="13" font-weight="700" letter-spacing="1.2">🔄 CURRENT PROCESS</text>')

# Pulse badge
parts.append(f'  <g transform="translate({right_x + right_w - 82}, {rc_y + 22})">'
             f'    <circle cx="0" cy="0" r="3.5" fill="{GREEN}"/>'
             f'    <text x="10" y="3.5" fill="{GREEN}" font-size="11" font-weight="600">RUNNING</text>'
             f'  </g>')

# Status banner
sb_y = rc_y + 38
parts.append(f'  <rect x="{right_x + 18}" y="{sb_y}" width="{right_w - 36}" height="26" rx="6" fill="#2386361a" stroke="#2ea043"/>')
parts.append(f'  <text x="{right_x + 30}" y="{sb_y + 17}" fill="{GREEN}" font-size="11" font-weight="700">🟢 STATUS: BUILDING iOS APPLICATIONS</text>')

# Terminal logs
logs = [
    "&gt; Loading iOS development environment...",
    "&gt; Compiling SwiftUI views &amp; optimizing UI performance...",
    "&gt; Running live previews &amp; testing reactive data flows...",
]
for k, l in enumerate(logs):
    parts.append(f'  <text x="{right_x + 18}" y="{sb_y + 44 + k * 18}" fill="{MUTED}" font-size="11">{l}</text>')

parts.append('</g>')

# ==================== RIGHT BOTTOM: SIGNAL OUTPUT QUOTE ====================
rq_y = rc_y + rc_h + 10
rq_h = left_h - (rt_h + 12 + rc_h + 10)

parts.append(f'<g class="fade-in" style="animation-delay: 0.55s">')
parts.append(f'  <rect x="{right_x}" y="{rq_y}" width="{right_w}" height="{rq_h}" rx="8" '
             f'fill="{CARD_BG}" stroke="{FRAME}"/>')
parts.append(f'  <text x="{right_x + 16}" y="{rq_y + 22}" fill="{CYAN}" font-size="11" font-weight="700" letter-spacing="1">⚡ SIGNAL OUTPUT</text>')
parts.append(f'  <text x="{right_x + 16}" y="{rq_y + 44}" fill="{TEXT}" font-size="12" font-style="italic">"Consistency builds systems. Systems build impact."</text>')
parts.append(f'  <rect class="cursor" x="{right_x + right_w - 24}" y="{rq_y + 33}" width="7" height="13" fill="{GREEN}"/>')
parts.append('</g>')

parts.append('</svg>')

svg = "\n".join(parts)
with open(OUT, "w") as f:
    f.write(svg)

print(f"Generated {OUT}: {W}x{H}, {len(svg)} bytes")
