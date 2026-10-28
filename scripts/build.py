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
    "Crimson Ember": "c23626", "Molten Rust": "f26e3f",
    "Forest Kelly": "199647", "Neon Lime": "8fe259",
    "Azure": "00b4d8", "Sky Flash": "0ad6ff",
    "Electric Violet": "ab51e3", "Lilac Flash": "cf76ff",
    "Lagoon Teal": "008388", "Pearl Aqua": "65dcb9",
    "Stone Gray": "566165", "Marigold": "febd5c", "Warm Ivory": "f6ebca",
    "Deep Indigo": "4376c2", "Deep Slate": "1c3139", "Slate Mist": "8d9ba0",
    "Night Indigo": "2c5084",
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

    "bright_black": "566165", "bright_red": "f26e3f", "bright_green": "8fe259",
    "bright_yellow": "febd5c", "bright_blue": "0ad6ff", "bright_magenta": "cf76ff",
    "bright_cyan": "65dcb9", "bright_white": "f6ebca",

    # UI roles beyond the terminal, for app themes built on EmberTide (Faena):
    # a card surface, dim text that stays readable on it, a blue for links and
    # charts, and a selection fill strong enough for bright-white text.
    "card": "1c3139", "dim_text": "8d9ba0", "indigo": "4376c2",
    "selection_strong": "2c5084",
}

# ---------------------------------------------------------------------------
# EmberTide Light: the same roles and named hues, re-solved for a light
# background. Each accent keeps its dark counterpart's OKLCH hue; only
# lightness and chroma move, so a name means the same hue in both variants.
# On light, "bright" means *further from the background* -- darker, higher
# contrast -- which is the same relationship the dark variant has, mirrored.
# Black and white swap ends: black is the background (as in dark), white is a
# deep slate and bright white is Ink Black, the foreground.
# ---------------------------------------------------------------------------
PALETTE_LIGHT = {
    "Ink Black": "001219", "Ivory Mist": "faf3e0", "Golden Orange": "a8701c",
    "Crimson Ember": "d33120", "Molten Rust": "ab3803",
    "Forest Kelly": "199245", "Neon Lime": "2b5506",
    "Azure": "137289", "Sky Flash": "0e596a",
    "Electric Violet": "ba3eff", "Lilac Flash": "861ab4",
    "Lagoon Teal": "008d92", "Pearl Aqua": "006f57",
    "Stone Gray": "7d888d", "Marigold": "845800", "Deep Slate": "1c3139",
    "Indigo Mist": "b6d0f6", "Paper White": "fefdf9", "Slate Mist": "57666b",
    "Deep Indigo": "2268cb",
}

FINAL_LIGHT = {
    "background": "faf3e0", "foreground": "001219",
    "cursor": "a8701c", "cursor_text": "001219",
    "selection_bg": "b6d0f6", "selection_fg": "001219",

    "black": "faf3e0", "red": "d33120", "green": "199245", "yellow": "a8701c",
    "blue": "137289", "magenta": "ba3eff", "cyan": "008d92", "white": "1c3139",

    "bright_black": "7d888d", "bright_red": "ab3803", "bright_green": "2b5506",
    "bright_yellow": "845800", "bright_blue": "0e596a", "bright_magenta": "861ab4",
    "bright_cyan": "006f57", "bright_white": "001219",

    "card": "fefdf9", "dim_text": "57666b", "indigo": "2268cb",
    "selection_strong": "b6d0f6",
}

class Variant:
    """One shipped variant: its name, colors, and where its files go. Dark
    keeps the original, unsuffixed file names; light adds "-light"."""
    def __init__(self, title, mode, palette, final, suffix):
        self.title, self.mode, self.palette, self.final = title, mode, palette, final
        self.Stem = "EmberTide" + suffix.title()    # EmberTide / EmberTide-Light
        self.stem = "embertide" + suffix            # embertide / embertide-light
        self.suffix = suffix
        self.swatch_dir = "assets/swatches" + ("/" + suffix.lstrip("-") if suffix else "")

    def h(self, role):
        return self.final[role]

DARK = Variant("EmberTide", "dark", PALETTE, FINAL, "")
LIGHT = Variant("EmberTide Light", "light", PALETTE_LIGHT, FINAL_LIGHT, "-light")
VARIANTS = [DARK, LIGHT]

ANSI_ORDER = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
              "bright_black", "bright_red", "bright_green", "bright_yellow",
              "bright_blue", "bright_magenta", "bright_cyan", "bright_white"]

# ---------------------------------------------------------------------------
# Color math (sRGB <-> OKLab/OKLCH, WCAG contrast) — used only to verify
# the FINAL dicts above, not to derive them (they were derived offline).
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

ACCENT_ROLES = ["red", "green", "yellow", "blue", "magenta", "cyan",
                "bright_red", "bright_green", "bright_yellow",
                "bright_blue", "bright_magenta", "bright_cyan"]

def oklch_H(hex_color):
    _, a, b = rgb_to_oklab(hex_color)
    return math.degrees(math.atan2(b, a)) % 360

def delta_e(hex1, hex2):
    return math.dist(rgb_to_oklab(hex1), rgb_to_oklab(hex2))

def verify(v):
    final = v.final
    bg = final["background"]
    hexes = [final[r] for r in ANSI_ORDER]
    dupes = {h: roles for h, roles in
             {h: [r for r, x in zip(ANSI_ORDER, hexes) if x == h] for h in hexes}.items()
             if len(roles) > 1}
    assert not dupes, f"{v.title}: unexpected ANSI collisions: {dupes}"
    assert len(set(hexes)) == 16, f"{v.title}: expected 16 unique ANSI hexes, got {len(set(hexes))}"

    # "Bright" means further from the background in OKLab L than its normal
    # counterpart: lighter on dark, darker on light. Same rule, both variants.
    bg_L = oklab_L(bg)
    for family in ANSI_ORDER[:8]:
        normal_d = abs(oklab_L(final[family]) - bg_L)
        bright_d = abs(oklab_L(final["bright_" + family]) - bg_L)
        assert bright_d > normal_d, (
            f"{v.title}: bright_{family} should sit further from the background than {family}")

    floors_normal = {"red": 3.5, "green": 3.5, "blue": 3.5, "magenta": 3.5,
                      "yellow": 3.5, "cyan": 3.5, "white": 3.5}
    for role, floor in floors_normal.items():
        cr = contrast(final[role], bg)
        assert cr >= floor - 0.05, f"{v.title}: {role} contrast {cr:.2f} below floor {floor}"

    floors_bright = {"bright_red": 5.0, "bright_green": 5.0, "bright_blue": 5.0,
                      "bright_magenta": 5.0, "bright_yellow": 5.0, "bright_cyan": 5.0,
                      "bright_white": 5.0, "bright_black": 2.9}
    for role, floor in floors_bright.items():
        cr = contrast(final[role], bg)
        assert cr >= floor - 0.05, f"{v.title}: {role} contrast {cr:.2f} below floor {floor}"

    # bright-black doubles as a background fill (e.g. Claude Code's active-prompt
    # highlight bar), with foreground text drawn on top of it -- that pairing
    # needs its own WCAG-AA floor, independent of bright-black's contrast against
    # the main background above. This is what caught the original #6d787c
    # (foreground-on-it was only 3.21:1, visibly hard to read).
    fg_on_bright_black = contrast(final["foreground"], final["bright_black"])
    assert fg_on_bright_black >= 4.5 - 0.05, (
        f"{v.title}: foreground-on-bright_black contrast {fg_on_bright_black:.2f} below 4.5 floor")

    # Selection: selected text must stay readable on the selection fill (3:1,
    # WCAG's large-text/UI floor -- dark's Deep Indigo sits at 3.2:1), and the
    # fill itself must read as distinct from the background (same ΔE floor as
    # the accents below).
    sel = contrast(final["selection_fg"], final["selection_bg"])
    assert sel >= 3.0 - 0.05, f"{v.title}: selection text contrast {sel:.2f} below 3.0 floor"
    sel_de = delta_e(final["selection_bg"], bg)
    assert sel_de >= 0.08, f"{v.title}: selection ΔE {sel_de:.3f} from background below 0.08"

    # Saturation consistency: the 12 hue-bearing accent roles (excludes
    # black/white/bright-black/bright-white, which are neutrals by design)
    # must sit reasonably close to the sRGB gamut edge for their own L,H, so
    # nothing reads as unintentionally "pastel" next to everything else's
    # "neon." 65% floor gives headroom below the current worst case (~75%).
    for role in ACCENT_ROLES:
        sat = saturation_ratio(final[role])
        assert sat >= 0.65 - 0.01, f"{v.title}: {role} saturation {sat*100:.1f}% below 65% floor"

    # Hue separation: every pair of accents, same family included, must be at
    # least 0.08 apart as OKLab ΔE -- distance in lightness and chroma counts,
    # not just hue angle. Dark's closest pair (red / bright red) is ~0.088.
    for i, a in enumerate(ACCENT_ROLES):
        for b in ACCENT_ROLES[i + 1:]:
            de = delta_e(final[a], final[b])
            assert de >= 0.08, f"{v.title}: {a} / {b} ΔE {de:.3f} below 0.08 floor"

    # UI roles. Dim text is a readable step between Stone Gray and the
    # foreground, on the background and on a card. Ink Black text must read on
    # the accent (buttons), bright red must read as text on a card, the indigo
    # must read against the background and stay apart from blue, and the
    # strong selection fill must carry bright-white text.
    card = final["card"]
    dim = final["dim_text"]
    for surface in (bg, card):
        cr = contrast(dim, surface)
        assert cr >= 4.5, f"{v.title}: dim_text contrast {cr:.2f} on #{surface} below 4.5"
    dim_d = abs(oklab_L(dim) - bg_L)
    assert (abs(oklab_L(final["bright_black"]) - bg_L) < dim_d
            < abs(oklab_L(final["foreground"]) - bg_L)), (
        f"{v.title}: dim_text should sit between bright_black and foreground")
    ink_on_accent = contrast(PALETTE["Ink Black"], final["cursor"])
    assert ink_on_accent >= 4.5, f"{v.title}: Ink Black on accent {ink_on_accent:.2f} below 4.5"
    red_on_card = contrast(final["bright_red"], card)
    assert red_on_card >= 4.5, f"{v.title}: bright_red on card {red_on_card:.2f} below 4.5"
    cr = contrast(final["indigo"], bg)
    assert cr >= 3.0, f"{v.title}: indigo contrast {cr:.2f} below 3.0"
    de = delta_e(final["indigo"], final["blue"])
    assert de >= 0.08, f"{v.title}: indigo / blue ΔE {de:.3f} below 0.08"
    dh = abs(oklch_H(final["indigo"]) - oklch_H(FINAL["indigo"]))
    assert min(dh, 360 - dh) <= 5, f"{v.title}: indigo hue drifted from the dark variant"
    sel = final["selection_strong"]
    cr = contrast(final["bright_white"], sel)
    assert cr >= 4.5, f"{v.title}: bright_white on selection_strong {cr:.2f} below 4.5"
    for surface in (bg, card):
        de = delta_e(sel, surface)
        assert de >= 0.08, f"{v.title}: selection_strong ΔE {de:.3f} from #{surface} below 0.08"

    # A name means one hue in every variant: a light accent may move in
    # lightness and chroma, but stays within 5° of its dark counterpart's hue.
    for role in ACCENT_ROLES:
        dh = abs(oklch_H(final[role]) - oklch_H(FINAL[role]))
        dh = min(dh, 360 - dh)
        assert dh <= 5, f"{v.title}: {role} hue drifted {dh:.1f}° from the dark variant"

    print(f"verify {v.title}: OK — 16/16 unique ANSI slots, all bright further from "
          "background than normal, contrast floors met (normal >=3.5:1, bright >=5:1, "
          "bright-black >=2.9:1 vs background, foreground-on-bright-black >=4.5:1, "
          "selection text >=3:1), accent saturation >=65% of gamut, accent ΔE >=0.08, "
          "hues within 5° of dark, UI roles (dim text, ink on accent, red on card, "
          "indigo, strong selection) readable")

# ---------------------------------------------------------------------------
# Generators — one function per terminal, each reading one variant's final dict
# ---------------------------------------------------------------------------
def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f:
        f.write(content)
    print("wrote", path)

def gen_iterm2(v):
    h = v.h
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
    write(f"iterm2/{v.Stem}.itermcolors", xml)

def gen_alacritty(v):
    h = v.h
    n = lambda r: f'"#{h(r)}"'
    content = f"""# {v.title} — {v.mode} terminal theme for Alacritty
# Save as ~/.config/alacritty/themes/{v.stem}.toml, then in alacritty.toml:
#   [general]
#   import = ["~/.config/alacritty/themes/{v.stem}.toml"]
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
    write(f"alacritty/{v.stem}.toml", content)

def gen_ghostty(v):
    h = v.h
    lines = [f"palette = {i}=#{h(role)}" for i, role in enumerate(ANSI_ORDER)]
    content = f"""# {v.title} — {v.mode} terminal theme for Ghostty
# Save as ~/.config/ghostty/themes/{v.Stem} (no extension — the filename
# is the theme name), then in ~/.config/ghostty/config:
#   theme = {v.Stem}
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
    write(f"ghostty/{v.Stem}", content)

def gen_kitty(v):
    h = v.h
    lines = [f"color{i:<2} #{h(role)}" for i, role in enumerate(ANSI_ORDER)]
    content = f"""# {v.title} — {v.mode} terminal theme for kitty
# Save as ~/.config/kitty/themes/{v.stem}.conf, then in kitty.conf:
#   include themes/{v.stem}.conf
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
    write(f"kitty/{v.stem}.conf", content)

def gen_wezterm(v):
    h = v.h
    ansi = ", ".join(f'"#{h(r)}"' for r in ANSI_ORDER[:8])
    bright = ", ".join(f'"#{h(r)}"' for r in ANSI_ORDER[8:])
    content = f"""# {v.title} — {v.mode} terminal theme for WezTerm
# Save as ~/.config/wezterm/colors/{v.Stem}.toml, then in wezterm.lua:
#   config.color_scheme = '{v.Stem}'
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
    write(f"wezterm/{v.Stem}.toml", content)

def gen_windows_terminal(v):
    h = v.h
    content = f"""{{
  "//": "{v.title} — Windows Terminal color scheme. Generated by scripts/build.py — do not hand-edit.",
  "//install": "Paste into the \\"schemes\\" array in settings.json, then set \\"colorScheme\\": \\"{v.title}\\" on a profile.",
  "name": "{v.title}",
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
    write(f"windows-terminal/{v.stem}.json", content)

def gen_tmux(v):
    h = v.h
    content = f"""# {v.title} — tmux status bar & chrome theme
# tmux inherits its 16 ANSI colors from the underlying terminal emulator —
# pair this with one of the terminal themes in this repo. This file only
# themes tmux's own UI: status bar, pane borders, messages, copy mode.
#
# Source it from ~/.tmux.conf:
#   source-file ~/.config/tmux/{v.stem}.tmux
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
    write(f"tmux/{v.stem}.tmux", content)

def gen_vscode(v):
    h = v.h
    content = f"""{{
  "//": "{v.title} — VS Code integrated terminal colors. Generated by scripts/build.py — do not hand-edit.",
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
    write(f"vscode/{v.stem}.settings.json", content)

def gen_warp(v):
    h = v.h
    content = f"""# {v.title} — {v.mode} terminal theme for Warp
# Save as ~/.warp/themes/{v.stem}.yaml, then select "{v.title}" in
# Warp -> Settings -> Appearance -> Themes.
# Generated by scripts/build.py — do not hand-edit.

name: {v.title}
accent: "#{h('cursor')}"
background: "#{h('background')}"
foreground: "#{h('foreground')}"
details: {"darker" if v.mode == "dark" else "lighter"}
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
    write(f"warp/{v.stem}.yaml", content)

# ---------------------------------------------------------------------------
# SVGs
# ---------------------------------------------------------------------------
def svg_wrap(width, height, body, bg="#f5f1e6"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}">\n<rect width="{width}" height="{height}" fill="{bg}"/>\n{body}</svg>\n')

def gen_palette_svg(v):
    sw, gap, margin = 76, 12, 20
    label_h, row_gap, per_row = 34, 22, 9
    width = margin * 2 + per_row * sw + (per_row - 1) * gap

    items = list(v.palette.items())
    rows = [items[i:i + per_row] for i in range(0, len(items), per_row)]

    parts = [f'<text x="{margin}" y="28" font-family="IBM Plex Mono, monospace" font-size="11" '
             f'fill="#756c5b" letter-spacing="1">PALETTE ({len(items)} colors)</text>']
    y = 38
    for row_items in rows:
        x = margin
        for name, hexcol in row_items:
            parts.append(f'<rect x="{x}" y="{y}" width="{sw}" height="{sw}" rx="8" fill="#{hexcol}" '
                          f'stroke="#00000022"/>')
            parts.append(f'<text x="{x + sw/2}" y="{y + sw + 17}" font-family="IBM Plex Sans, sans-serif" '
                          f'font-size="10" font-weight="600" fill="#211d15" text-anchor="middle">{name}</text>')
            parts.append(f'<text x="{x + sw/2}" y="{y + sw + 30}" font-family="IBM Plex Mono, monospace" '
                          f'font-size="9" fill="#756c5b" text-anchor="middle">#{hexcol}</text>')
            x += sw + gap
        y += sw + label_h + row_gap
    y = y - row_gap + 8

    write(f"assets/palette{v.suffix}.svg", svg_wrap(width, y, "\n".join(parts)))

def gen_ansi_grid_svg(v):
    h = v.h
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

    write(f"assets/ansi-grid{v.suffix}.svg", svg_wrap(width, y, "\n".join(body)))

def slugify(name):
    return name.lower().replace(" ", "-")

def gen_swatches(v):
    """One small standalone swatch SVG per named color, for embedding inline
    in README tables (<img src="assets/swatches/slug.svg">) -- generated
    locally rather than depending on an external color-swatch image service,
    consistent with how palette.svg/ansi-grid.svg are already produced."""
    w, hgt = 48, 20
    for name, hexcol in v.palette.items():
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{hgt}" '
               f'viewBox="0 0 {w} {hgt}">\n'
               f'<rect width="{w}" height="{hgt}" rx="4" fill="#{hexcol}" '
               f'stroke="#00000022"/>\n</svg>\n')
        write(f"{v.swatch_dir}/{slugify(name)}.svg", svg)

if __name__ == "__main__":
    for v in VARIANTS:
        verify(v)
    for v in VARIANTS:
        gen_iterm2(v)
        gen_alacritty(v)
        gen_ghostty(v)
        gen_kitty(v)
        gen_wezterm(v)
        gen_windows_terminal(v)
        gen_tmux(v)
        gen_vscode(v)
        gen_warp(v)
        gen_palette_svg(v)
        gen_ansi_grid_svg(v)
        gen_swatches(v)
    print("done")
