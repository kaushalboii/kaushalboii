#!/usr/bin/env python3
"""
Render the streak / numbers card from data/contributions.json (written daily by
fetch_contributions.py) as a terminal-window SVG that sits beside kaushal-ascii.svg.

Supports both dark mode (default stats.svg with dynamic light-mode CSS fallback)
and light mode (stats-light.svg with GitHub Primer light palette).

The canvas is the same size as the portrait (840 x 880) so the two panels line
up when the README shows them side by side at equal widths.

Usage:
    python scripts/render_stats_svg.py [data.json] [output.svg]
    If no args provided, automatically renders both stats.svg and stats-light.svg.
"""
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SRC = os.path.join(HERE, "..", "data", "contributions.json")
DEFAULT_DARK_OUT = os.path.join(HERE, "..", "stats.svg")
DEFAULT_LIGHT_OUT = os.path.join(HERE, "..", "stats-light.svg")

W, H = 840, 880
PAD = 20
TITLEBAR_H = 30
COLS, ROWS = 2, 3
GAP = 16
TILE_W = (W - PAD * 2 - GAP * (COLS - 1)) / COLS
TILE_H = 150
TILES_TOP = TITLEBAR_H + PAD + 4
CHART_TOP = TILES_TOP + ROWS * TILE_H + (ROWS - 1) * GAP + GAP

# Timing (seconds)
TILE_STAGGER = 0.15
SLIDE_DUR = 0.45
COUNT_DUR = 1.2
FRAMES = 16
BAR_START = TILE_STAGGER * COLS * ROWS + 0.4
BAR_STAGGER = 0.06
BAR_DUR = 0.6


def short(d):
    return datetime.date.fromisoformat(d).strftime("%b %-d")


def span(s):
    return f'{short(s["start"])} – {short(s["end"])}' if s["length"] else "—"


def fmt(v, like):
    return f"{v:,.1f}" if isinstance(like, float) else f"{int(round(v)):,}"


def build_stats_svg(data, theme="dark"):
    is_light = (theme == "light")
    scheme = "light" if is_light else "light dark"

    if is_light:
        bg1, bg2 = "#ffffff", "#f6f8fa"
        frame_col = "#d0d7de"
        tile_bg = "#ffffff"
        muted_col = "#57606a"
        ink_col = "#1f2328"
        green_col = "#1a7f37"
        radar_stroke = "#0969da"
        bar_col = "#2da44e"
        bar_peak_col = "#1a7f37"
        pulse_col = "#0969da"
    else:
        bg1, bg2 = "#111722", "#0d1117"
        frame_col = "#30363d"
        tile_bg = "#161b22"
        muted_col = "#7d8590"
        ink_col = "#e6edf3"
        green_col = "#39d353"
        radar_stroke = "#38bdf8"
        bar_col = "#26a641"
        bar_peak_col = "#39d353"
        pulse_col = "#38bdf8"

    cur = data["current_streak"]
    lng = data["longest_streak"]
    best = data["best_day"]
    n_days = len(data["days"])

    # (label, value, suffix, caption, is_green_accent)
    tiles = [
        ("current streak", cur["length"], " days", span(cur), True),
        ("longest streak", lng["length"], " days", span(lng), False),
        ("contributions", data["total_contributions"], "", "in the last year", False),
        ("active days", data["active_days"], f" / {n_days}", f'{data["active_days"] / n_days:.0%} of the year', False),
        ("best day", best["count"], "", short(best["date"]), False),
        ("avg / active day", data["avg_per_active_day"], "", "contributions", False),
    ]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'style="color-scheme: {scheme};" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace">',
        '<style>',
        f':root {{ color-scheme: {scheme}; }}',
        f'.t{{opacity:0;animation:in {SLIDE_DUR}s ease-out both}}',
        '@keyframes in{0%{opacity:0;transform:translateY(14px)}100%{opacity:1;transform:translateY(0)}}',
        f'.b{{transform-box:fill-box;transform-origin:bottom;transform:scaleY(0);animation:grow {BAR_DUR}s ease-out both}}',
        '@keyframes grow{to{transform:scaleY(1)}}',
        '@keyframes eq1{0%,100%{height:4px;y:14px}50%{height:18px;y:0px}}',
        '@keyframes eq2{0%,100%{height:16px;y:2px}50%{height:6px;y:12px}}',
        '@keyframes eq3{0%,100%{height:8px;y:10px}50%{height:20px;y:-2px}}',
        '@keyframes eq4{0%,100%{height:19px;y:-1px}50%{height:7px;y:11px}}',
        '@media (prefers-reduced-motion: reduce){.t,.b{opacity:1!important;transform:none!important;animation:none!important}}',
    ]

    # If building the dark version, add CSS rules that dynamically adapt to light mode in browser
    if not is_light:
        parts.extend([
            '@media (prefers-color-scheme: light) {',
            '  .win-bg { fill: url(#bg-light) !important; }',
            '  .win-frame { stroke: #d0d7de !important; }',
            '  .title-txt { fill: #57606a !important; }',
            '  .hud-bracket { stroke: #0969da !important; fill: none !important; }',
            '  .tile-rect { fill: #ffffff !important; stroke: #d0d7de !important; }',
            '  .txt-muted, .txt-ink .txt-muted, .txt-green .txt-muted { fill: #57606a !important; }',
            '  .txt-ink { fill: #1f2328 !important; }',
            '  .txt-green { fill: #1a7f37 !important; }',
            '  .badge-dot { fill: #1a7f37 !important; }',
            '  .badge-ring { stroke: #1a7f37 !important; fill: none !important; }',
            '  .badge-txt { fill: #1a7f37 !important; }',
            '  .pulse-bar { fill: #0969da !important; }',
            '  .chart-bar-reg { fill: #2da44e !important; }',
            '  .chart-bar-peak { fill: #1a7f37 !important; }',
            '}',
        ])

    parts.append('</style>')
    parts.append('<defs>')
    parts.append(f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
                 f'<stop offset="0" stop-color="{bg1}"/><stop offset="1" stop-color="{bg2}"/></linearGradient>')
    if not is_light:
        parts.append('<linearGradient id="bg-light" x1="0" y1="0" x2="0" y2="1">'
                     '<stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#f6f8fa"/></linearGradient>')
    parts.append('</defs>')

    # Window shell
    parts.append(f'<rect class="win-bg" width="{W}" height="{H}" rx="12" fill="url(#bg)"/>')
    parts.append(f'<rect class="win-frame" x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{frame_col}"/>')
    parts.append(f'<line class="win-frame" x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{frame_col}"/>')

    # Traffic lights
    for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dot}"/>')

    parts.append(f'<text class="title-txt" x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{muted_col}" font-size="12" '
                 f'text-anchor="middle">kaushal@github: ~$ ./stats.sh --live</text>')

    # Active status badge
    parts.append(f'<g transform="translate(740, 15.0)">'
                 f'<circle class="badge-dot" cx="0" cy="0" r="3.5" fill="{green_col}"/>'
                 f'<circle class="badge-ring" cx="0" cy="0" r="3.5" fill="none" stroke="{green_col}" stroke-width="1.5">'
                 f'<animate attributeName="r" values="3.5;8;3.5" dur="2s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0.9;0;0.9" dur="2s" repeatCount="indefinite"/></circle>'
                 f'<text class="badge-txt" x="10" y="3.5" fill="{green_col}" font-size="10" font-weight="700" letter-spacing="1">ACTIVE</text></g>')

    # HUD corner brackets
    parts.append(f'<path class="hud-bracket" d="M 24 46 L 38 46 M 24 46 L 24 60" stroke="{radar_stroke}" stroke-width="2" fill="none" opacity="0.6"/>')
    parts.append(f'<path class="hud-bracket" d="M 816 46 L 802 46 M 816 46 L 816 60" stroke="{radar_stroke}" stroke-width="2" fill="none" opacity="0.6"/>')
    parts.append(f'<path class="hud-bracket" d="M 24 856 L 38 856 M 24 856 L 24 842" stroke="{radar_stroke}" stroke-width="2" fill="none" opacity="0.6"/>')
    parts.append(f'<path class="hud-bracket" d="M 816 856 L 802 856 M 816 856 L 816 842" stroke="{radar_stroke}" stroke-width="2" fill="none" opacity="0.6"/>')

    # ---- Stat tiles ----------------------------------------------------------
    for i, (label, value, suffix, caption, is_green) in enumerate(tiles):
        col, row = i % COLS, i // COLS
        x = PAD + col * (TILE_W + GAP)
        y = TILES_TOP + row * (TILE_H + GAP)
        start = i * TILE_STAGGER
        count_start = start + SLIDE_DUR * 0.6
        accent_color = green_col if is_green else ink_col
        accent_cls = "txt-green" if is_green else "txt-ink"

        parts.append(f'<g class="t" style="animation-delay:{start:.2f}s">')
        parts.append(f'<rect class="tile-rect" x="{x:.1f}" y="{y}" width="{TILE_W:.1f}" height="{TILE_H}" rx="10" '
                     f'fill="{tile_bg}" stroke="{frame_col}"/>')
        parts.append(f'<text class="txt-muted" x="{x+24:.1f}" y="{y+40}" fill="{muted_col}" font-size="22">$ {label}</text>')

        if i == 0:  # current streak radar indicator
            parts.append(f'<circle class="badge-dot" cx="{x+TILE_W-40:.1f}" cy="{y+36}" r="4" fill="{green_col}"/>'
                         f'<circle class="badge-ring" cx="{x+TILE_W-40:.1f}" cy="{y+36}" r="4" fill="none" stroke="{green_col}" stroke-width="1.5">'
                         f'<animate attributeName="r" values="4;14;4" dur="2.4s" repeatCount="indefinite"/>'
                         f'<animate attributeName="opacity" values="0.85;0;0.85" dur="2.4s" repeatCount="indefinite"/></circle>')

        # count-up frames: ease-out so it decelerates into the real number
        num_y = y + 100
        for k in range(1, FRAMES + 1):
            p = k / FRAMES
            v = value * (1 - (1 - p) ** 3)
            t_on = count_start + COUNT_DUR * (k - 1) / FRAMES
            t_off = count_start + COUNT_DUR * k / FRAMES
            anim = f'<set attributeName="opacity" to="1" begin="{t_on:.3f}s"/>'
            if k < FRAMES:
                anim += f'<set attributeName="opacity" to="0" begin="{t_off:.3f}s"/>'
            parts.append(
                f'<text class="{accent_cls}" x="{x+24:.1f}" y="{num_y}" opacity="0" font-size="54" font-weight="700" fill="{accent_color}">'
                f'{fmt(v, value)}<tspan class="txt-muted" font-size="24" font-weight="400" fill="{muted_col}">{suffix}</tspan>'
                f'{anim}</text>'
            )
        parts.append(f'<text class="txt-muted" x="{x+24:.1f}" y="{y+132}" fill="{muted_col}" font-size="20">{caption}</text>')
        parts.append('</g>')

    # ---- Monthly bars --------------------------------------------------------
    monthly = data["monthly"]
    chart_x, chart_w = PAD, W - PAD * 2
    chart_h = H - PAD - CHART_TOP
    parts.append(f'<g class="t" style="animation-delay:{BAR_START - 0.3:.2f}s">')
    parts.append(f'<rect class="tile-rect" x="{chart_x}" y="{CHART_TOP}" width="{chart_w}" height="{chart_h}" rx="10" '
                 f'fill="{tile_bg}" stroke="{frame_col}"/>')
    parts.append(f'<text class="txt-muted" x="{chart_x+24}" y="{CHART_TOP+40}" fill="{muted_col}" font-size="22">$ contributions / month</text>')
    parts.append(f'<g transform="translate(640, 580)">'
                 f'<text class="txt-muted" x="-8" y="11" fill="{muted_col}" font-size="11" text-anchor="end">SYSTEM PULSE</text>'
                 f'<rect class="pulse-bar" x="0" y="2" width="3.5" height="14" rx="1.5" fill="{pulse_col}" style="animation:eq1 1.00s infinite ease-in-out"/>'
                 f'<rect class="pulse-bar" x="6" y="2" width="3.5" height="14" rx="1.5" fill="{pulse_col}" style="animation:eq2 1.25s infinite ease-in-out"/>'
                 f'<rect class="pulse-bar" x="12" y="2" width="3.5" height="14" rx="1.5" fill="{pulse_col}" style="animation:eq3 1.50s infinite ease-in-out"/>'
                 f'<rect class="pulse-bar" x="18" y="2" width="3.5" height="14" rx="1.5" fill="{pulse_col}" style="animation:eq4 1.75s infinite ease-in-out"/>'
                 f'<rect class="pulse-bar" x="24" y="2" width="3.5" height="14" rx="1.5" fill="{pulse_col}" style="animation:eq2 1.00s infinite ease-in-out"/>'
                 f'<rect class="pulse-bar" x="30" y="2" width="3.5" height="14" rx="1.5" fill="{pulse_col}" style="animation:eq1 1.25s infinite ease-in-out"/>'
                 f'<rect class="pulse-bar" x="36" y="2" width="3.5" height="14" rx="1.5" fill="{pulse_col}" style="animation:eq4 1.50s infinite ease-in-out"/>'
                 f'<rect class="pulse-bar" x="42" y="2" width="3.5" height="14" rx="1.5" fill="{pulse_col}" style="animation:eq3 1.75s infinite ease-in-out"/>'
                 f'<rect class="pulse-bar" x="48" y="2" width="3.5" height="14" rx="1.5" fill="{pulse_col}" style="animation:eq2 1.00s infinite ease-in-out"/>'
                 f'<rect class="pulse-bar" x="54" y="2" width="3.5" height="14" rx="1.5" fill="{pulse_col}" style="animation:eq1 1.25s infinite ease-in-out"/>'
                 f'</g>')
    parts.append('</g>')

    plot_top = CHART_TOP + 64
    plot_bot = CHART_TOP + chart_h - 40
    plot_l, plot_r = chart_x + 24, chart_x + chart_w - 24
    slot = (plot_r - plot_l) / len(monthly)
    bar_w = slot * 0.62
    peak = max(m["total"] for m in monthly) or 1
    for i, m in enumerate(monthly):
        h = max(2, (plot_bot - plot_top) * m["total"] / peak)
        bx = plot_l + i * slot + (slot - bar_w) / 2
        is_peak = (m["total"] == peak)
        fill = bar_peak_col if is_peak else bar_col
        cls_bar = "b chart-bar-peak" if is_peak else "b chart-bar-reg"
        delay = BAR_START + i * BAR_STAGGER
        parts.append(f'<rect class="{cls_bar}" x="{bx:.1f}" y="{plot_bot - h:.1f}" width="{bar_w:.1f}" height="{h:.1f}" '
                     f'rx="3" fill="{fill}" style="animation-delay:{delay:.2f}s"/>')
        mon = datetime.date.fromisoformat(m["month"] + "-01").strftime("%b")[0]
        parts.append(f'<text class="txt-muted" x="{bx + bar_w/2:.1f}" y="{plot_bot + 28}" fill="{muted_col}" font-size="18" '
                     f'text-anchor="middle">{mon}</text>')
        if is_peak:
            parts.append(f'<text class="t txt-ink" style="animation-delay:{delay + BAR_DUR:.2f}s" x="{bx + bar_w/2:.1f}" '
                         f'y="{plot_bot - h - 10:.1f}" fill="{ink_col}" font-size="18" text-anchor="middle">{peak:,}</text>')

    parts.append('</svg>')
    return "".join(parts)


def main():
    src = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else DEFAULT_SRC
    custom_out = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(src):
        print(f"Error: {src} not found")
        sys.exit(1)

    with open(src, "r") as f:
        data = json.load(f)

    if custom_out:
        theme = "light" if "light" in custom_out.lower() else "dark"
        svg = build_stats_svg(data, theme=theme)
        with open(custom_out, "w") as f:
            f.write(svg)
        print(f"wrote {custom_out}: {W} x {H}, {len(svg)//1024} KB ({theme} mode)")
    else:
        # Default: render both dark and light
        dark_svg = build_stats_svg(data, theme="dark")
        with open(DEFAULT_DARK_OUT, "w") as f:
            f.write(dark_svg)
        print(f"wrote {DEFAULT_DARK_OUT}: {W} x {H}, {len(dark_svg)//1024} KB (dark mode + adaptive CSS)")

        light_svg = build_stats_svg(data, theme="light")
        with open(DEFAULT_LIGHT_OUT, "w") as f:
            f.write(light_svg)
        print(f"wrote {DEFAULT_LIGHT_OUT}: {W} x {H}, {len(light_svg)//1024} KB (light mode)")


if __name__ == "__main__":
    main()
