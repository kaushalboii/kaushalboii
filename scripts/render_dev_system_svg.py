#!/usr/bin/env python3
"""
Render Kaushal's developer system telemetry, identity, and deployment logs
as a terminal-window SVG.

Supports both dark mode (dev-system.svg with adaptive CSS) and light mode
(dev-system-light.svg with GitHub Primer light palette).

Usage:
    python scripts/render_dev_system_svg.py [output.svg]
    If no args provided, automatically renders both dev-system.svg and dev-system-light.svg.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DARK_OUT = os.path.join(HERE, "..", "dev-system.svg")
DEFAULT_LIGHT_OUT = os.path.join(HERE, "..", "dev-system-light.svg")

W, H = 860, 520
PAD = 20
TITLEBAR_H = 32


def build_dev_system_svg(theme="dark"):
    is_light = (theme == "light")
    scheme = "light" if is_light else "light dark"

    if is_light:
        bg1, bg2 = "#ffffff", "#f6f8fa"
        card_bg = "#ffffff"
        inner_card_bg = "#f6f8fa"
        frame_col = "#d0d7de"
        frame_accent = "#0969da"
        muted_col = "#57606a"
        text_col = "#1f2328"
        green_col = "#1a7f37"
        cyan_col = "#0969da"
        amber_col = "#b45309"
        purple_col = "#8250df"
        track_col = "#eaeef2"
        role_pill_bg = "#ddf4ff"
        role_pill_stroke = "#54aeff"
        role_pill_text = "#0969da"
        mode_pill_bg = "#dafbe1"
        mode_pill_stroke = "#4ac26b"
        status_banner_bg = "#dafbe1"
        status_banner_stroke = "#4ac26b"
        cursor_col = "#0969da"
    else:
        bg1, bg2 = "#111722", "#0d1117"
        card_bg = "#161b22"
        inner_card_bg = "#0d1117"
        frame_col = "#30363d"
        frame_accent = "#1f6feb"
        muted_col = "#7d8590"
        text_col = "#e6edf3"
        green_col = "#39d353"
        cyan_col = "#38bdf8"
        amber_col = "#f59e0b"
        purple_col = "#a855f7"
        track_col = "#21262d"
        role_pill_bg = "#1f6feb22"
        role_pill_stroke = "#388bfd"
        role_pill_text = "#58a6ff"
        mode_pill_bg = "#23863622"
        mode_pill_stroke = "#2ea043"
        status_banner_bg = "#2386361a"
        status_banner_stroke = "#2ea043"
        cursor_col = "#39d353"

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'style="color-scheme: {scheme};" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace">',
        '<style>',
        f'  :root {{ color-scheme: {scheme}; }}',
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
    ]

    if not is_light:
        parts.extend([
            '  @media (prefers-color-scheme: light) {',
            '    .win-shell { fill: url(#win-bg-light) !important; }',
            '    .frame-stroke { stroke: #d0d7de !important; }',
            '    .card-box { fill: #ffffff !important; stroke: #d0d7de !important; }',
            '    .inner-box { fill: #f6f8fa !important; stroke: #d0d7de !important; }',
            '    .hud-cyan { stroke: #0969da !important; fill: none !important; opacity: 0.7 !important; }',
            '    .txt-primary { fill: #1f2328 !important; }',
            '    .txt-muted { fill: #57606a !important; }',
            '    .txt-cyan { fill: #0969da !important; }',
            '    .txt-green { fill: #1a7f37 !important; }',
            '    .txt-amber { fill: #b45309 !important; }',
            '    .dot-fill { fill: #1a7f37 !important; }',
            '    .ring-stroke { stroke: #1a7f37 !important; fill: none !important; }',
            '    .track-bg { fill: #eaeef2 !important; }',
            '    .bar-grad-fill { fill: url(#bar-grad-light) !important; }',
            '    .role-pill { fill: #ddf4ff !important; stroke: #54aeff !important; }',
            '    .role-txt { fill: #0969da !important; }',
            '    .mode-pill { fill: #dafbe1 !important; stroke: #4ac26b !important; }',
            '    .status-banner { fill: #dafbe1 !important; stroke: #4ac26b !important; }',
            '    .cursor-elem { fill: #0969da !important; }',
            '  }',
        ])

    parts.append('</style>')
    parts.append('<defs>')
    parts.append(f'  <linearGradient id="win-bg" x1="0" y1="0" x2="0" y2="1">')
    parts.append(f'    <stop offset="0%" stop-color="{bg1}"/>')
    parts.append(f'    <stop offset="100%" stop-color="{bg2}"/>')
    parts.append('  </linearGradient>')
    if not is_light:
        parts.append('  <linearGradient id="win-bg-light" x1="0" y1="0" x2="0" y2="1">')
        parts.append('    <stop offset="0%" stop-color="#ffffff"/>')
        parts.append('    <stop offset="100%" stop-color="#f6f8fa"/>')
        parts.append('  </linearGradient>')

    parts.append('  <linearGradient id="bar-grad" x1="0" y1="0" x2="1" y2="0">')
    parts.append(f'    <stop offset="0%" stop-color="{cyan_col}"/>')
    parts.append(f'    <stop offset="100%" stop-color="{green_col}"/>')
    parts.append('  </linearGradient>')
    if not is_light:
        parts.append('  <linearGradient id="bar-grad-light" x1="0" y1="0" x2="1" y2="0">')
        parts.append('    <stop offset="0%" stop-color="#0969da"/>')
        parts.append('    <stop offset="100%" stop-color="#1a7f37"/>')
        parts.append('  </linearGradient>')

    parts.append('</defs>')

    # Window shell
    parts.append(f'<rect class="win-shell" width="{W}" height="{H}" rx="12" fill="url(#win-bg)"/>')
    parts.append(f'<rect class="frame-stroke" x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{frame_col}"/>')
    parts.append(f'<line class="frame-stroke" x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{frame_col}"/>')

    # Traffic lights
    for i, col in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{col}"/>')

    # Titlebar
    parts.append(f'<text class="txt-muted" x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{muted_col}" font-size="12" '
                 f'text-anchor="middle">kaushal@dev-station: ~$ systemctl status kaushal.profile</text>')

    # Live System Badge
    parts.append(
        f'<g transform="translate({W - 145}, {TITLEBAR_H/2})">'
        f'  <circle class="dot-fill" cx="0" cy="0" r="3.5" fill="{green_col}"/>'
        f'  <circle class="ring-stroke pulse-glow" cx="0" cy="0" r="3.5" fill="none" stroke="{green_col}" stroke-width="1.5"/>'
        f'  <text class="txt-green" x="12" y="3.5" fill="{green_col}" font-size="11" font-weight="700" letter-spacing="1">SYSTEM ONLINE</text>'
        f'</g>'
    )

    # HUD Tech Corner brackets
    bracket_opacity = "0.7" if is_light else "0.6"
    parts.append(f'<path class="hud-cyan" d="M 22 44 L 34 44 M 22 44 L 22 56" stroke="{cyan_col}" stroke-width="1.5" fill="none" opacity="{bracket_opacity}"/>')
    parts.append(f'<path class="hud-cyan" d="M {W-22} 44 L {W-34} 44 M {W-22} 44 L {W-22} 56" stroke="{cyan_col}" stroke-width="1.5" fill="none" opacity="{bracket_opacity}"/>')
    parts.append(f'<path class="hud-cyan" d="M 22 {H-22} L 34 {H-22} M 22 {H-22} L 22 {H-34}" stroke="{cyan_col}" stroke-width="1.5" fill="none" opacity="{bracket_opacity}"/>')
    parts.append(f'<path class="hud-cyan" d="M {W-22} {H-22} L {W-34} {H-22} M {W-22} {H-22} L {W-22} {H-34}" stroke="{cyan_col}" stroke-width="1.5" fill="none" opacity="{bracket_opacity}"/>')

    # ==================== LEFT COLUMN: CORE IDENTITY & STACK ====================
    left_x = 22
    left_y = 48
    left_w = 428
    left_h = H - left_y - 20

    parts.append(f'<g class="fade-in" style="animation-delay: 0.1s">')
    parts.append(f'  <rect class="card-box" x="{left_x}" y="{left_y}" width="{left_w}" height="{left_h}" rx="10" '
                 f'fill="{card_bg}" stroke="{frame_col}"/>')
    # Header
    parts.append(f'  <text class="txt-cyan" x="{left_x + 18}" y="{left_y + 28}" fill="{cyan_col}" font-size="13" font-weight="700" letter-spacing="1.2">⚡ INITIALIZING DEV SYSTEM</text>')
    parts.append(f'  <text class="txt-green" x="{left_x + left_w - 18}" y="{left_y + 28}" fill="{green_col}" font-size="11" text-anchor="end">BOOT: 100%</text>')

    # Boot Progress Bar
    bar_x = left_x + 18
    bar_y = left_y + 40
    bar_w = left_w - 36
    bar_h = 6
    parts.append(f'  <rect class="track-bg" x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="3" fill="{track_col}"/>')
    parts.append(f'  <rect class="bar-grow bar-grad-fill" x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="3" fill="url(#bar-grad)"/>')

    # Divider
    parts.append(f'  <line class="frame-stroke" x1="{left_x + 18}" y1="{left_y + 60}" x2="{left_x + left_w - 18}" y2="{left_y + 60}" stroke="{frame_col}" stroke-dasharray="3,3"/>')

    # Identity section
    parts.append(f'  <text class="txt-muted" x="{left_x + 18}" y="{left_y + 82}" fill="{muted_col}" font-size="11" font-weight="700" letter-spacing="1">🧠 CORE IDENTITY</text>')
    parts.append(f'  <text class="txt-primary" x="{left_x + 18}" y="{left_y + 106}" fill="{text_col}" font-size="19" font-weight="700">Kaushal Maran</text>')

    # Role pill
    pill_x = left_x + 18
    pill_y = left_y + 118
    parts.append(f'  <rect class="role-pill" x="{pill_x}" y="{pill_y}" width="205" height="22" rx="11" fill="{role_pill_bg}" stroke="{role_pill_stroke}"/>')
    parts.append(f'  <text class="role-txt" x="{pill_x + 10}" y="{pill_y + 15}" fill="{role_pill_text}" font-size="11" font-weight="600">Mobile Application Developer</text>')

    # Mode indicator
    mode_x = pill_x + 215
    parts.append(f'  <rect class="mode-pill" x="{mode_x}" y="{pill_y}" width="90" height="22" rx="11" fill="{mode_pill_bg}" stroke="{mode_pill_stroke}"/>')
    parts.append(f'  <circle class="dot-fill" cx="{mode_x + 12}" cy="{pill_y + 11}" r="3" fill="{green_col}"/>')
    parts.append(f'  <text class="txt-green" x="{mode_x + 22}" y="{pill_y + 15}" fill="{green_col}" font-size="11" font-weight="600">ACTIVE</text>')

    # System Configuration / Stack
    parts.append(f'  <line class="frame-stroke" x1="{left_x + 18}" y1="{left_y + 156}" x2="{left_x + left_w - 18}" y2="{left_y + 156}" stroke="{frame_col}"/>')
    parts.append(f'  <text class="txt-muted" x="{left_x + 18}" y="{left_y + 178}" fill="{muted_col}" font-size="11" font-weight="700" letter-spacing="1">⚙️ PRIMARY STACK</text>')

    # Stack Cards
    # iOS Card
    c1_y = left_y + 192
    parts.append(f'  <rect class="inner-box" x="{left_x + 18}" y="{c1_y}" width="{left_w - 36}" height="56" rx="8" fill="{inner_card_bg}" stroke="{frame_col}"/>')
    parts.append(f'  <text class="txt-primary" x="{left_x + 30}" y="{c1_y + 24}" fill="{text_col}" font-size="13" font-weight="700">📱 iOS Development</text>')
    parts.append(f'  <text class="txt-muted" x="{left_x + 30}" y="{c1_y + 44}" fill="{muted_col}" font-size="11">SwiftUI · Swift · Combine · Xcode · UIKit</text>')
    parts.append(f'  <circle class="dot-fill" cx="{left_x + left_w - 34}" cy="{c1_y + 28}" r="4" fill="{green_col}"/>')

    # Android Card
    c2_y = c1_y + 64
    parts.append(f'  <rect class="inner-box" x="{left_x + 18}" y="{c2_y}" width="{left_w - 36}" height="56" rx="8" fill="{inner_card_bg}" stroke="{frame_col}"/>')
    parts.append(f'  <text class="txt-primary" x="{left_x + 30}" y="{c2_y + 24}" fill="{text_col}" font-size="13" font-weight="700">🤖 Android Development</text>')
    parts.append(f'  <text class="txt-muted" x="{left_x + 30}" y="{c2_y + 44}" fill="{muted_col}" font-size="11">Kotlin · Jetpack Compose · Coroutines · Flow · Studio</text>')
    parts.append(f'  <circle class="dot-fill" cx="{left_x + left_w - 34}" cy="{c2_y + 28}" r="4" fill="{green_col}"/>')

    # Secondary Capabilities
    cap_y = c2_y + 72
    parts.append(f'  <text class="txt-muted" x="{left_x + 18}" y="{cap_y + 14}" fill="{muted_col}" font-size="11" font-weight="700" letter-spacing="1">🎨 SECONDARY CAPABILITIES</text>')

    caps = [
        ("🎨 UI/UX Engineering", "→ Figma → Production UI"),
        ("⚡ Performance &amp; Arch", "→ MVVM / MVI · Clean Arch"),
        ("🔗 Integrations", "→ APIs · Firebase · CI/CD"),
    ]
    for j, (title, desc) in enumerate(caps):
        cy = cap_y + 30 + j * 26
        parts.append(f'  <text class="txt-primary" x="{left_x + 22}" y="{cy}" fill="{text_col}" font-size="11" font-weight="600">{title}</text>')
        parts.append(f'  <text class="txt-muted" x="{left_x + 180}" y="{cy}" fill="{muted_col}" font-size="11">{desc}</text>')

    parts.append('</g>')

    # ==================== RIGHT TOP: DEPLOYMENT TELEMETRY ====================
    right_x = left_x + left_w + 14
    right_w = W - right_x - 22
    rt_y = left_y
    rt_h = 195

    parts.append(f'<g class="fade-in" style="animation-delay: 0.25s">')
    parts.append(f'  <rect class="card-box" x="{right_x}" y="{rt_y}" width="{right_w}" height="{rt_h}" rx="10" '
                 f'fill="{card_bg}" stroke="{frame_col}"/>')
    parts.append(f'  <text class="txt-cyan" x="{right_x + 18}" y="{rt_y + 28}" fill="{cyan_col}" font-size="13" font-weight="700" letter-spacing="1.2">📊 DEPLOYMENT LOGS</text>')
    parts.append(f'  <text class="txt-green" x="{right_x + right_w - 18}" y="{rt_y + 28}" fill="{green_col}" font-size="11" text-anchor="end">STATUS: STABLE</text>')

    # 3 metric tiles in a row
    tile_w = (right_w - 36 - 16) / 3
    tile_h = 76
    metrics = [
        ("10+", "Android Apps", "Deployed &amp; Live", green_col, "txt-green"),
        ("2", "iOS Apps", "App Store / SwiftUI", cyan_col, "txt-cyan"),
        ("100%", "Releases", "Zero Downtime", amber_col, "txt-amber"),
    ]

    for i, (val, title, caption, accent, cls_acc) in enumerate(metrics):
        tx = right_x + 18 + i * (tile_w + 8)
        ty = rt_y + 44
        parts.append(f'  <rect class="inner-box" x="{tx:.1f}" y="{ty}" width="{tile_w:.1f}" height="{tile_h}" rx="8" fill="{inner_card_bg}" stroke="{frame_col}"/>')
        parts.append(f'  <text class="{cls_acc}" x="{tx + tile_w/2:.1f}" y="{ty + 34}" fill="{accent}" font-size="24" font-weight="700" text-anchor="middle">{val}</text>')
        parts.append(f'  <text class="txt-primary" x="{tx + tile_w/2:.1f}" y="{ty + 52}" fill="{text_col}" font-size="11" font-weight="600" text-anchor="middle">{title}</text>')
        parts.append(f'  <text class="txt-muted" x="{tx + tile_w/2:.1f}" y="{ty + 66}" fill="{muted_col}" font-size="9" text-anchor="middle">{caption}</text>')

    # Verification / System Health line
    parts.append(f'  <line class="frame-stroke" x1="{right_x + 18}" y1="{rt_y + 134}" x2="{right_x + right_w - 18}" y2="{rt_y + 134}" stroke="{frame_col}"/>')
    parts.append(f'  <text class="txt-green" x="{right_x + 18}" y="{rt_y + 156}" fill="{green_col}" font-size="12">✔ Production Releases: SUCCESSFUL</text>')
    parts.append(f'  <text class="txt-muted" x="{right_x + right_w - 18}" y="{rt_y + 156}" fill="{muted_col}" font-size="11" text-anchor="end">Reliability: HIGH</text>')
    parts.append(f'  <text class="txt-muted" x="{right_x + 18}" y="{rt_y + 178}" fill="{muted_col}" font-size="11">✔ Automated Pipelines: HEALTHY · Clean Code Standards</text>')
    parts.append('</g>')

    # ==================== RIGHT MIDDLE: CURRENT RUNTIME PROCESS ====================
    rc_y = rt_y + rt_h + 12
    rc_h = 155

    parts.append(f'<g class="fade-in" style="animation-delay: 0.4s">')
    parts.append(f'  <rect class="card-box" x="{right_x}" y="{rc_y}" width="{right_w}" height="{rc_h}" rx="10" '
                 f'fill="{card_bg}" stroke="{frame_col}"/>')
    parts.append(f'  <text class="txt-cyan" x="{right_x + 18}" y="{rc_y + 26}" fill="{cyan_col}" font-size="13" font-weight="700" letter-spacing="1.2">🔄 CURRENT PROCESS</text>')

    # Pulse badge
    parts.append(f'  <g transform="translate({right_x + right_w - 82}, {rc_y + 22})">'
                 f'    <circle class="dot-fill" cx="0" cy="0" r="3.5" fill="{green_col}"/>'
                 f'    <text class="txt-green" x="10" y="3.5" fill="{green_col}" font-size="11" font-weight="600">RUNNING</text>'
                 f'  </g>')

    # Status banner
    sb_y = rc_y + 38
    parts.append(f'  <rect class="status-banner" x="{right_x + 18}" y="{sb_y}" width="{right_w - 36}" height="26" rx="6" fill="{status_banner_bg}" stroke="{status_banner_stroke}"/>')
    parts.append(f'  <text class="txt-green" x="{right_x + 30}" y="{sb_y + 17}" fill="{green_col}" font-size="11" font-weight="700">🟢 STATUS: BUILDING iOS APPLICATIONS</text>')

    # Terminal logs
    logs = [
        "&gt; Loading iOS development environment...",
        "&gt; Compiling SwiftUI views &amp; optimizing UI performance...",
        "&gt; Running live previews &amp; testing reactive data flows...",
    ]
    for k, l in enumerate(logs):
        parts.append(f'  <text class="txt-muted" x="{right_x + 18}" y="{sb_y + 44 + k * 18}" fill="{muted_col}" font-size="11">{l}</text>')

    parts.append('</g>')

    # ==================== RIGHT BOTTOM: SIGNAL OUTPUT QUOTE ====================
    rq_y = rc_y + rc_h + 10
    rq_h = left_h - (rt_h + 12 + rc_h + 10)

    parts.append(f'<g class="fade-in" style="animation-delay: 0.55s">')
    parts.append(f'  <rect class="card-box" x="{right_x}" y="{rq_y}" width="{right_w}" height="{rq_h}" rx="8" '
                 f'fill="{card_bg}" stroke="{frame_col}"/>')
    parts.append(f'  <text class="txt-cyan" x="{right_x + 16}" y="{rq_y + 22}" fill="{cyan_col}" font-size="11" font-weight="700" letter-spacing="1">⚡ SIGNAL OUTPUT</text>')
    parts.append(f'  <text class="txt-primary" x="{right_x + 16}" y="{rq_y + 44}" fill="{text_col}" font-size="12" font-style="italic">"Consistency builds systems. Systems build impact."</text>')
    parts.append(f'  <rect class="cursor cursor-elem" x="{right_x + right_w - 24}" y="{rq_y + 33}" width="7" height="13" fill="{cursor_col}"/>')
    parts.append('</g>')

    parts.append('</svg>')
    return "\n".join(parts)


def main():
    custom_out = sys.argv[1] if len(sys.argv) > 1 else None

    if custom_out:
        theme = "light" if "light" in custom_out.lower() else "dark"
        svg = build_dev_system_svg(theme=theme)
        with open(custom_out, "w") as f:
            f.write(svg)
        print(f"Generated {custom_out}: {W}x{H}, {len(svg)} bytes ({theme} mode)")
    else:
        # Generate both dark and light
        dark_svg = build_dev_system_svg(theme="dark")
        with open(DEFAULT_DARK_OUT, "w") as f:
            f.write(dark_svg)
        print(f"Generated {DEFAULT_DARK_OUT}: {W}x{H}, {len(dark_svg)} bytes (dark mode + adaptive CSS)")

        light_svg = build_dev_system_svg(theme="light")
        with open(DEFAULT_LIGHT_OUT, "w") as f:
            f.write(light_svg)
        print(f"Generated {DEFAULT_LIGHT_OUT}: {W}x{H}, {len(light_svg)} bytes (light mode)")


if __name__ == "__main__":
    main()
