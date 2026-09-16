#!/usr/bin/env python3
"""Single source of truth for the EmberTide theme.

Regenerates every terminal config and the reference SVGs from one
palette dict, then asserts the properties the README claims (unique
ANSI slots outside the intentional white/bright-white/bright-yellow
group, bright > normal lightness per hue family, WCAG contrast
floors). Run from the repo root: `python3 scripts/build.py`.
"""
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# The palette: every distinct color the theme actually uses, named, as one
# set. Earlier revisions split this into "source" (the original 10-stop
# gradient) and "specified" (hand-picked additions), but that distinction
# stopped meaning much once most of the original 10 had been adjusted,
# replaced, or dropped entirely — Dark Teal, Burnt Caramel, and Brown Red
# no longer appear anywhere in FINAL below. Treating everything as one
# palette is what makes an honest intensity/consistency pass possible.
# ---------------------------------------------------------------------------
PALETTE = {
    "Ink Black": "001219", "Vanilla Custard": "e9d8a6", "Golden Orange": "ee9b00",
    "Crimson Ember": "c23626", "Molten Rust": "da5b2d",
    "Forest Kelly": "199647", "Neon Lime": "8fe259",
    "Azure": "00b4d8", "Sky Flash": "0ad6ff",
    "Electric Violet": "ab51e3", "Lilac Flash": "cf76ff",
    "Lagoon Teal": "008388", "Pearl Aqua": "65dcb9",
    "Stone Gray": "566165", "Marigold": "febd5c", "Warm Ivory": "f6ebca",
    "Deep Indigo": "4376c2",
}

# ---------------------------------------------------------------------------
# Final palette: every ANSI slot and special role, assembled from PALETTE.
# ---------------------------------------------------------------------------
FINAL = {
    "background": "001219", "foreground": "e9d8a6",
    "cursor": "ee9b00", "cursor_text": "001219",
    "selection_bg": "4376c2", "selection_fg": "e9d8a6",

    "black": "001219", "red": "c23626", "green": "199647", "yellow": "ee9b00",
    "blue": "00b4d8", "magenta": "ab51e3", "cyan": "008388", "white": "e9d8a6",

    "bright_black": "566165", "bright_red": "da5b2d", "bright_green": "8fe259",
    "bright_yellow": "febd5c", "bright_blue": "0ad6ff", "bright_magenta": "cf76ff",
    "bright_cyan": "65dcb9", "bright_white": "f6ebca",
}

ANSI_ORDER = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
              "bright_black", "bright_red", "bright_green", "bright_yellow",
              "bright_blue", "bright_magenta", "bright_cyan", "bright_white"]

# ---------------------------------------------------------------------------
# Color math (sRGB <-> OKLab/OKLCH, WCAG contrast) — used only to verify
# the FINAL dict above, not to derive it (it was already derived offline).
# ---------------------------------------------------------------------------
def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def hex_to_rgb01(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

def rel_lum(rgb01):
    return (0.2126 * srgb_to_linear(rgb01[0]) + 0.7152 * srgb_to_linear(rgb01[1])
            + 0.0722 * srgb_to_linear(rgb01[2]))

def contrast(hex1, hex2):
    l1, l2 = rel_lum(hex_to_rgb01(hex1)), rel_lum(hex_to_rgb01(hex2))
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)

def rgb_to_oklab(hex_color):
    r, g, b = (srgb_to_linear(c) for c in hex_to_rgb01(hex_color))
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (x ** (1 / 3) if x >= 0 else -((-x) ** (1 / 3)) for x in (l, m, s))
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    b2 = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return L, a, b2

def oklab_L(hex_color):
    return rgb_to_oklab(hex_color)[0]

def linear_to_srgb_raw(c):
    # unclamped -- needed to detect out-of-gamut values, unlike the display path
    sign, c = (1, c) if c >= 0 else (-1, -c)
    v = 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055
    return sign * v

def oklab_to_rgb01_raw(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    r = +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    b3 = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return (linear_to_srgb_raw(r), linear_to_srgb_raw(g), linear_to_srgb_raw(b3))

def in_gamut(L, C, H):
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    return all(-1e-4 <= c <= 1 + 1e-4 for c in oklab_to_rgb01_raw(L, a, b))

def max_chroma(L, H, hi_start=0.5):
    if in_gamut(L, hi_start, H):
        return hi_start
    lo, hi = 0.0, hi_start
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if in_gamut(L, mid, H) else (lo, mid)
    return lo

def saturation_ratio(hex_color):
    """Chroma as a fraction of the max chroma reachable at this exact L,H --
    i.e. how close to the sRGB gamut edge a color sits. This is what actually
    separates "neon" from "pastel," independent of how light or dark the
    color is (unlike raw chroma, which shrinks near black and white anyway).
    """
    L, a, b = rgb_to_oklab(hex_color)
    C = math.hypot(a, b)
    H = math.degrees(math.atan2(b, a)) % 360
    cmax = max_chroma(L, H)
    return C / cmax if cmax > 0 else 0.0

def verify():
    bg = FINAL["background"]
    hexes = [FINAL[r] for r in ANSI_ORDER]
    dupes = {h: roles for h, roles in
             {h: [r for r, x in zip(ANSI_ORDER, hexes) if x == h] for h in hexes}.items()
             if len(roles) > 1}
    assert not dupes, f"Unexpected ANSI collisions: {dupes}"
    assert len(set(hexes)) == 16, f"Expected 16 unique ANSI hexes, got {len(set(hexes))}"

    for family in ANSI_ORDER[:8]:
        normal_L = oklab_L(FINAL[family])
        bright_L = oklab_L(FINAL["bright_" + family])
        assert bright_L > normal_L, f"bright_{family} should be lighter than {family}"

    floors_normal = {"red": 3.5, "green": 3.5, "blue": 3.5, "magenta": 3.5,
                      "yellow": 3.5, "cyan": 3.5, "white": 3.5}
    for role, floor in floors_normal.items():
        cr = contrast(FINAL[role], bg)
        assert cr >= floor - 0.05, f"{role} contrast {cr:.2f} below floor {floor}"

    floors_bright = {"bright_red": 5.0, "bright_green": 5.0, "bright_blue": 5.0,
                      "bright_magenta": 5.0, "bright_yellow": 5.0, "bright_cyan": 5.0,
                      "bright_white": 5.0, "bright_black": 2.9}
    for role, floor in floors_bright.items():
        cr = contrast(FINAL[role], bg)
        assert cr >= floor - 0.05, f"{role} contrast {cr:.2f} below floor {floor}"

    # bright-black doubles as a background fill (e.g. Claude Code's active-prompt
    # highlight bar), with foreground text drawn on top of it -- that pairing
    # needs its own WCAG-AA floor, independent of bright-black's contrast against
    # the main background above. This is what caught the original #6d787c
    # (foreground-on-it was only 3.21:1, visibly hard to read).
    fg_on_bright_black = contrast(FINAL["foreground"], FINAL["bright_black"])
    assert fg_on_bright_black >= 4.5 - 0.05, (
        f"foreground-on-bright_black contrast {fg_on_bright_black:.2f} below 4.5 floor")

    # Saturation consistency: the 12 hue-bearing accent roles (excludes
    # black/white/bright-black/bright-white, which are neutrals by design)
    # must sit reasonably close to the sRGB gamut edge for their own L,H, so
    # nothing reads as unintentionally "pastel" next to everything else's
    # "neon." 65% floor gives headroom below the current worst case (~75%).
    accent_roles = ["red", "green", "yellow", "blue", "magenta", "cyan",
                     "bright_red", "bright_green", "bright_yellow",
                     "bright_blue", "bright_magenta", "bright_cyan"]
    for role in accent_roles:
        sat = saturation_ratio(FINAL[role])
        assert sat >= 0.65 - 0.01, f"{role} saturation {sat*100:.1f}% below 65% floor"

    print("verify: OK — 16/16 unique ANSI slots, all bright>normal, "
          "contrast floors met (normal >=3.5:1, bright >=5:1, bright-black >=2.9:1 "
          "vs background, foreground-on-bright-black >=4.5:1), "
          "accent saturation >=65% of gamut")

# ---------------------------------------------------------------------------
# Generators — one function per terminal, all reading from FINAL
# ---------------------------------------------------------------------------
def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f:
        f.write(content)
    print("wrote", path)

def h(role):
    return FINAL[role]

def gen_iterm2():
    def comp(hexcol):
        r, g, b = hex_to_rgb01(hexcol)
        return f'\t\t<key>Red Component</key><real>{r:.6f}</real>\n\t\t<key>Green Component</key><real>{g:.6f}</real>\n\t\t<key>Blue Component</key><real>{b:.6f}</real>\n\t\t<key>Alpha Component</key><real>1</real>'

    def block(key, hexcol):
        return (f'\t<key>{key}</key>\n\t<dict>\n\t\t<key>Color Space</key><string>sRGB</string>\n'
                f'{comp(hexcol)}\n\t</dict>')

    parts = [block(f"Ansi {i} Color", h(role)) for i, role in enumerate(ANSI_ORDER)]
    parts += [
        block("Background Color", h("background")),
        block("Foreground Color", h("foreground")),
        block("Bold Color", h("foreground")),
        block("Cursor Color", h("cursor")),
        block("Cursor Text Color", h("cursor_text")),
        block("Selection Color", h("selection_bg")),
        block("Selected Text Color", h("selection_fg")),
        block("Link Color", h("cursor")),
    ]
    body = "\n".join(parts)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
        '<plist version="1.0">\n<dict>\n' + body + '\n</dict>\n</plist>\n'
    )
    write("iterm2/EmberTide.itermcolors", xml)

def gen_alacritty():
    n = lambda r: f'"#{h(r)}"'
    content = f"""# EmberTide — dark terminal theme for Alacritty
# Save as ~/.config/alacritty/themes/embertide.toml, then in alacritty.toml:
#   [general]
#   import = ["~/.config/alacritty/themes/embertide.toml"]
# Generated by scripts/build.py — do not hand-edit.

[colors]
draw_bold_text_with_bright_colors = true

[colors.primary]
background = {n('background')}
foreground = {n('foreground')}

[colors.cursor]
text = {n('cursor_text')}
cursor = {n('cursor')}

[colors.selection]
text = {n('selection_fg')}
background = {n('selection_bg')}

[colors.normal]
black   = {n('black')}
red     = {n('red')}
green   = {n('green')}
yellow  = {n('yellow')}
blue    = {n('blue')}
magenta = {n('magenta')}
cyan    = {n('cyan')}
white   = {n('white')}

[colors.bright]
black   = {n('bright_black')}
red     = {n('bright_red')}
green   = {n('bright_green')}
yellow  = {n('bright_yellow')}
blue    = {n('bright_blue')}
magenta = {n('bright_magenta')}
cyan    = {n('bright_cyan')}
white   = {n('bright_white')}
"""
    write("alacritty/embertide.toml", content)

def gen_ghostty():
    lines = [f"palette = {i}=#{h(role)}" for i, role in enumerate(ANSI_ORDER)]
    content = f"""# EmberTide — dark terminal theme for Ghostty
# Save as ~/.config/ghostty/themes/EmberTide (no extension — the filename
# is the theme name), then in ~/.config/ghostty/config:
#   theme = EmberTide
# Generated by scripts/build.py — do not hand-edit.

background = {h('background')}
foreground = {h('foreground')}
cursor-color = {h('cursor')}
cursor-text = {h('cursor_text')}
selection-background = {h('selection_bg')}
selection-foreground = {h('selection_fg')}
bold-is-bright = true

{chr(10).join(lines)}
"""
    write("ghostty/EmberTide", content)

def gen_kitty():
    lines = [f"color{i:<2} #{h(role)}" for i, role in enumerate(ANSI_ORDER)]
    content = f"""# EmberTide — dark terminal theme for kitty
# Save as ~/.config/kitty/themes/embertide.conf, then in kitty.conf:
#   include themes/embertide.conf
# Generated by scripts/build.py — do not hand-edit.

background            #{h('background')}
foreground             #{h('foreground')}
cursor                 #{h('cursor')}
cursor_text_color      #{h('cursor_text')}
selection_background   #{h('selection_bg')}
selection_foreground   #{h('selection_fg')}
bold_font              auto

{chr(10).join(lines)}
"""
    write("kitty/embertide.conf", content)

def gen_wezterm():
    ansi = ", ".join(f'"#{h(r)}"' for r in ANSI_ORDER[:8])
    bright = ", ".join(f'"#{h(r)}"' for r in ANSI_ORDER[8:])
    content = f"""# EmberTide — dark terminal theme for WezTerm
# Save as ~/.config/wezterm/colors/EmberTide.toml, then in wezterm.lua:
#   config.color_scheme = 'EmberTide'
# Generated by scripts/build.py — do not hand-edit.

[colors]
foreground = "#{h('foreground')}"
background = "#{h('background')}"
cursor_bg = "#{h('cursor')}"
cursor_fg = "#{h('cursor_text')}"
cursor_border = "#{h('cursor')}"
selection_fg = "#{h('selection_fg')}"
selection_bg = "#{h('selection_bg')}"

ansi = [{ansi}]
brights = [{bright}]
"""
    write("wezterm/EmberTide.toml", content)

def gen_windows_terminal():
    content = f"""{{
  "//": "EmberTide — Windows Terminal color scheme. Generated by scripts/build.py — do not hand-edit.",
  "//install": "Paste into the \\"schemes\\" array in settings.json, then set \\"colorScheme\\": \\"EmberTide\\" on a profile.",
  "name": "EmberTide",
  "background": "#{h('background')}",
  "foreground": "#{h('foreground')}",
  "cursorColor": "#{h('cursor')}",
  "selectionBackground": "#{h('selection_bg')}",
  "black": "#{h('black')}",
  "red": "#{h('red')}",
  "green": "#{h('green')}",
  "yellow": "#{h('yellow')}",
  "blue": "#{h('blue')}",
  "purple": "#{h('magenta')}",
  "cyan": "#{h('cyan')}",
  "white": "#{h('white')}",
  "brightBlack": "#{h('bright_black')}",
  "brightRed": "#{h('bright_red')}",
  "brightGreen": "#{h('bright_green')}",
  "brightYellow": "#{h('bright_yellow')}",
  "brightBlue": "#{h('bright_blue')}",
  "brightPurple": "#{h('bright_magenta')}",
  "brightCyan": "#{h('bright_cyan')}",
  "brightWhite": "#{h('bright_white')}"
}}
"""
    write("windows-terminal/embertide.json", content)

def gen_tmux():
    content = f"""# EmberTide — tmux status bar & chrome theme
# tmux inherits its 16 ANSI colors from the underlying terminal emulator —
# pair this with one of the terminal themes in this repo. This file only
# themes tmux's own UI: status bar, pane borders, messages, copy mode.
#
# Source it from ~/.tmux.conf:
#   source-file ~/.config/tmux/embertide.tmux
# Generated by scripts/build.py — do not hand-edit.

set -g status-style "bg=#{h('background')},fg=#{h('foreground')}"
set -g status-left "#[bg=#{h('cursor')},fg=#{h('cursor_text')},bold] #S #[bg=#{h('background')},fg=#{h('cursor')}]"
set -g status-right "#[fg=#{h('cyan')}]%Y-%m-%d #[fg=#{h('foreground')}]%H:%M "
set -g window-status-current-style "bg=#{h('selection_bg')},fg=#{h('foreground')},bold"
set -g window-status-style "bg=#{h('background')},fg=#{h('bright_black')}"

set -g pane-border-style "fg=#{h('selection_bg')}"
set -g pane-active-border-style "fg=#{h('cursor')}"

set -g message-style "bg=#{h('selection_bg')},fg=#{h('foreground')}"
set -g message-command-style "bg=#{h('selection_bg')},fg=#{h('foreground')}"

set -g mode-style "bg=#{h('selection_bg')},fg=#{h('foreground')}"
"""
    write("tmux/embertide.tmux", content)

def gen_vscode():
    content = f"""{{
  "//": "EmberTide — VS Code integrated terminal colors. Generated by scripts/build.py — do not hand-edit.",
  "//install": "Merge the workbench.colorCustomizations block into your settings.json.",
  "workbench.colorCustomizations": {{
    "terminal.background": "#{h('background')}",
    "terminal.foreground": "#{h('foreground')}",
    "terminalCursor.background": "#{h('cursor_text')}",
    "terminalCursor.foreground": "#{h('cursor')}",
    "terminal.selectionBackground": "#{h('selection_bg')}",
    "terminal.ansiBlack": "#{h('black')}",
    "terminal.ansiRed": "#{h('red')}",
    "terminal.ansiGreen": "#{h('green')}",
    "terminal.ansiYellow": "#{h('yellow')}",
    "terminal.ansiBlue": "#{h('blue')}",
    "terminal.ansiMagenta": "#{h('magenta')}",
    "terminal.ansiCyan": "#{h('cyan')}",
    "terminal.ansiWhite": "#{h('white')}",
    "terminal.ansiBrightBlack": "#{h('bright_black')}",
    "terminal.ansiBrightRed": "#{h('bright_red')}",
    "terminal.ansiBrightGreen": "#{h('bright_green')}",
    "terminal.ansiBrightYellow": "#{h('bright_yellow')}",
    "terminal.ansiBrightBlue": "#{h('bright_blue')}",
    "terminal.ansiBrightMagenta": "#{h('bright_magenta')}",
    "terminal.ansiBrightCyan": "#{h('bright_cyan')}",
    "terminal.ansiBrightWhite": "#{h('bright_white')}"
  }}
}}
"""
    write("vscode/embertide.settings.json", content)

def gen_warp():
    content = f"""# EmberTide — dark terminal theme for Warp
# Save as ~/.warp/themes/embertide.yaml, then select "EmberTide" in
# Warp -> Settings -> Appearance -> Themes.
# Generated by scripts/build.py — do not hand-edit.

name: EmberTide
accent: "#{h('cursor')}"
background: "#{h('background')}"
foreground: "#{h('foreground')}"
details: darker
terminal_colors:
  normal:
    black: "#{h('black')}"
    red: "#{h('red')}"
    green: "#{h('green')}"
    yellow: "#{h('yellow')}"
    blue: "#{h('blue')}"
    magenta: "#{h('magenta')}"
    cyan: "#{h('cyan')}"
    white: "#{h('white')}"
  bright:
    black: "#{h('bright_black')}"
    red: "#{h('bright_red')}"
    green: "#{h('bright_green')}"
    yellow: "#{h('bright_yellow')}"
    blue: "#{h('bright_blue')}"
    magenta: "#{h('bright_magenta')}"
    cyan: "#{h('bright_cyan')}"
    white: "#{h('bright_white')}"
"""
    write("warp/embertide.yaml", content)

# ---------------------------------------------------------------------------
# SVGs
# ---------------------------------------------------------------------------
def svg_wrap(width, height, body, bg="#f5f1e6"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}">\n<rect width="{width}" height="{height}" fill="{bg}"/>\n{body}</svg>\n')

def gen_palette_svg():
    sw, gap, margin = 76, 12, 20
    label_h, row_gap, per_row = 34, 22, 9
    width = margin * 2 + per_row * sw + (per_row - 1) * gap

    items = list(PALETTE.items())
    rows = [items[i:i + per_row] for i in range(0, len(items), per_row)]

    parts = [f'<text x="{margin}" y="28" font-family="IBM Plex Mono, monospace" font-size="11" '
             f'fill="#756c5b" letter-spacing="1">PALETTE ({len(items)} colors)</text>']
    y = 38
    for row_items in rows:
        x = margin
        for name, hexcol in row_items:
            parts.append(f'<rect x="{x}" y="{y}" width="{sw}" height="{sw}" rx="8" fill="#{hexcol}"/>')
            parts.append(f'<text x="{x + sw/2}" y="{y + sw + 17}" font-family="IBM Plex Sans, sans-serif" '
                          f'font-size="10" font-weight="600" fill="#211d15" text-anchor="middle">{name}</text>')
            parts.append(f'<text x="{x + sw/2}" y="{y + sw + 30}" font-family="IBM Plex Mono, monospace" '
                          f'font-size="9" fill="#756c5b" text-anchor="middle">#{hexcol}</text>')
            x += sw + gap
        y += sw + label_h + row_gap
    y = y - row_gap + 8

    write("assets/palette.svg", svg_wrap(width, y, "\n".join(parts)))

def gen_ansi_grid_svg():
    cols, sw, gap, margin = 8, 78, 12, 20
    header_h, label_h, row_gap = 20, 28, 22
    width = margin * 2 + cols * sw + (cols - 1) * gap

    def row(y, title, roles):
        parts = [f'<text x="{margin}" y="{y}" font-family="IBM Plex Mono, monospace" font-size="11" '
                 f'fill="#756c5b" letter-spacing="1">{title}</text>']
        sy = y + 10
        x = margin
        for role in roles:
            hexcol = h(role)
            label = role.replace("bright_", "br.").replace("_", " ")
            parts.append(f'<rect x="{x}" y="{sy}" width="{sw}" height="{sw}" rx="6" fill="#{hexcol}" '
                          f'stroke="#00000022"/>')
            parts.append(f'<text x="{x + sw/2}" y="{sy + sw + 14}" font-family="IBM Plex Sans, sans-serif" '
                          f'font-size="9.5" fill="#211d15" text-anchor="middle">{label}</text>')
            parts.append(f'<text x="{x + sw/2}" y="{sy + sw + 26}" font-family="IBM Plex Mono, monospace" '
                          f'font-size="8.5" fill="#756c5b" text-anchor="middle">#{hexcol}</text>')
            x += sw + gap
        return "\n".join(parts), sy + sw + label_h

    y = 28
    body = []
    core = ["background", "foreground", "cursor", "selection_bg"]
    r, y2 = row(y, "CORE ROLES", core)
    body.append(r)
    y = y2 + row_gap
    r, y2 = row(y, "NORMAL (0-7)", ANSI_ORDER[0:8])
    body.append(r)
    y = y2 + row_gap
    r, y2 = row(y, "BRIGHT (8-15)", ANSI_ORDER[8:16])
    body.append(r)
    y = y2 + 8

    write("assets/ansi-grid.svg", svg_wrap(width, y, "\n".join(body)))

if __name__ == "__main__":
    verify()
    gen_iterm2()
    gen_alacritty()
    gen_ghostty()
    gen_kitty()
    gen_wezterm()
    gen_windows_terminal()
    gen_tmux()
    gen_vscode()
    gen_warp()
    gen_palette_svg()
    gen_ansi_grid_svg()
    print("done")
