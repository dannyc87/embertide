# EmberTide

A dark terminal theme, built and checked in OKLCH for consistent contrast, hue
separation, and saturation across every ANSI slot.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![WCAG 2.1 | AA](https://img.shields.io/badge/WCAG_2.1_%7C_AA-001219?logo=w3c&logoColor=e9d8a6&style=flat-square)](https://www.w3.org/TR/WCAG21/#contrast-minimum)

![Palette](assets/palette.svg)

## Origin

EmberTide started as a 10-stop teal-to-ember gradient — a mood board more than a
literal spec. It set the shape of the theme (a cool dark end, a warm bright end) but
most of the individual stops have since been adjusted, replaced, or dropped; Dark Teal,
Burnt Caramel, and Brown Red don't appear anywhere in the current palette.

| Name | Hex |
|---|---|
| Ink Black | `#001219` |
| Dark Teal | `#005f73` |
| Dark Cyan | `#0a9396` |
| Pearl Aqua | `#94d2bd` |
| Vanilla Custard | `#e9d8a6` |
| Golden Orange | `#ee9b00` |
| Burnt Caramel | `#ca6702` |
| Rusty Spice | `#bb3e03` |
| Oxidized Iron | `#ae2012` |
| Brown Red | `#9b2226` |

## Design

Colors are worked and checked in OKLCH (via OKLab), not sRGB directly, since perceptual
lightness and chroma are what actually determine how a color reads against a
background — raw hex values don't.

- **Contrast** — every normal-row ANSI color clears ≥3.5:1 against the `#001219`
  background and every other bright-row color clears ≥5:1. Bright-black clears a lower
  ≥2.9:1 against the background, because it also doubles as a *background fill* in some
  UIs (Claude Code's active-prompt highlight bar is one) — what actually matters there
  is foreground text drawn on top of it, which is checked separately and held to a
  real ≥4.5:1 (the original `#6d787c` only managed 3.21:1 there, visibly hard to read).
- **Hue separation** — neighboring accent colors are compared as OKLab distance (ΔE),
  not just hue angle, since two colors can share a hue and still read as distinct if
  their lightness or chroma differs enough — or sit far apart in hue and still look
  confusable if lightness and chroma coincide.
- **Saturation** — measured as chroma relative to the maximum chroma reachable at a
  color's own lightness and hue (its distance to the sRGB gamut edge), rather than raw
  chroma, which shrinks near black and white regardless of how vivid a color feels. The
  12 hue-bearing ANSI roles (red/green/yellow/blue/magenta/cyan, normal and bright) are
  held to ≥65% of that ceiling, so nothing reads as unintentionally pastel next to the
  rest.
- Every rule above is asserted by [`scripts/build.py`](scripts/build.py) before it
  writes a single file — see [Regenerating](#regenerating).

How this palette maps to semantic syntax roles (comment, keyword, function, type, and so
on) across the editor editions is defined once, canonically, in [SPEC.md](SPEC.md) — the
contract both [embertide-vscode](https://github.com/dannyc87/embertide-vscode) and
[embertide-jetbrains](https://github.com/dannyc87/embertide-jetbrains) implement.

## Preview

![ANSI color grid](assets/ansi-grid.svg)

## Supported terminals

| Terminal | File | Install |
|---|---|---|
| [iTerm2](#iterm2) | `iterm2/EmberTide.itermcolors` | Import via Preferences |
| [Alacritty](#alacritty) | `alacritty/embertide.toml` | `import` in `alacritty.toml` |
| [Ghostty](#ghostty) | `ghostty/EmberTide` | `theme = EmberTide` |
| [kitty](#kitty) | `kitty/embertide.conf` | `include` in `kitty.conf` |
| [WezTerm](#wezterm) | `wezterm/EmberTide.toml` | `color_scheme` in `wezterm.lua` |
| [Windows Terminal](#windows-terminal) | `windows-terminal/embertide.json` | paste into `settings.json` |
| [Warp](#warp) | `warp/embertide.yaml` | drop into `~/.warp/themes` |
| [tmux](#tmux) | `tmux/embertide.tmux` | `source-file` in `.tmux.conf` |
| [VS Code](#vs-code-integrated-terminal) | `vscode/embertide.settings.json` | merge into `settings.json` |

### iTerm2

1. Preferences → Profiles → Colors → Color Presets… → Import…
2. Select `iterm2/EmberTide.itermcolors`.
3. Choose **EmberTide** from the Color Presets dropdown.

### Alacritty

```sh
mkdir -p ~/.config/alacritty/themes
cp alacritty/embertide.toml ~/.config/alacritty/themes/
```

In `~/.config/alacritty/alacritty.toml`:

```toml
[general]
import = ["~/.config/alacritty/themes/embertide.toml"]
```

### Ghostty

```sh
mkdir -p ~/.config/ghostty/themes
cp ghostty/EmberTide ~/.config/ghostty/themes/EmberTide
```

In `~/.config/ghostty/config`:

```
theme = EmberTide
```

### kitty

```sh
mkdir -p ~/.config/kitty/themes
cp kitty/embertide.conf ~/.config/kitty/themes/
```

In `~/.config/kitty/kitty.conf`:

```
include themes/embertide.conf
```

### WezTerm

```sh
mkdir -p ~/.config/wezterm/colors
cp wezterm/EmberTide.toml ~/.config/wezterm/colors/
```

In `~/.config/wezterm/wezterm.lua`:

```lua
config.color_scheme = 'EmberTide'
```

### Windows Terminal

Open `settings.json` (Settings → Open JSON file), paste the contents of
`windows-terminal/embertide.json` into the `"schemes"` array, then set
`"colorScheme": "EmberTide"` on the profile(s) you want themed.

### Warp

```sh
mkdir -p ~/.warp/themes
cp warp/embertide.yaml ~/.warp/themes/
```

Settings → Appearance → Themes → **EmberTide**.

### tmux

```sh
mkdir -p ~/.config/tmux
cp tmux/embertide.tmux ~/.config/tmux/
```

In `~/.tmux.conf`:

```
source-file ~/.config/tmux/embertide.tmux
```

tmux inherits its 16 ANSI colors from the terminal emulator underneath it — pair this
with one of the terminal themes above for the pane content, not just the status bar.

### VS Code integrated terminal

Merge the `workbench.colorCustomizations` block from `vscode/embertide.settings.json`
into your user or workspace `settings.json`. For a full editor theme (workbench UI and
syntax highlighting, not just the terminal panel), see [Editor themes](#editor-themes)
below instead.

## Editor themes

Full editor themes (workbench UI and syntax highlighting, not just the terminal panel)
are companion repos generated from this same palette, implementing the shared
[SPEC.md](SPEC.md) role mapping:

| Editor | Repo |
|---|---|
| VS Code | [dannyc87/embertide-vscode](https://github.com/dannyc87/embertide-vscode) |
| JetBrains IDEs (IntelliJ IDEA, PyCharm, WebStorm, etc.) | [dannyc87/embertide-jetbrains](https://github.com/dannyc87/embertide-jetbrains) |

## Color reference

### Core roles

| Swatch | Role | Hex |
|---|---|---|
| ![](assets/swatches/ink-black.svg) | Background | `#001219` |
| ![](assets/swatches/vanilla-custard.svg) | Foreground | `#e9d8a6` |
| ![](assets/swatches/golden-orange.svg) | Cursor | `#ee9b00` |
| ![](assets/swatches/deep-indigo.svg) | Selection background | `#4376c2` |

### ANSI — normal

| # | Swatch | Role | Hex | Contrast vs. bg |
|---|---|---|---|---|
| 0 | ![](assets/swatches/ink-black.svg) | Black | `#001219` | — |
| 1 | ![](assets/swatches/crimson-ember.svg) | Red | `#c23626` | 3.5:1 |
| 2 | ![](assets/swatches/forest-kelly.svg) | Green | `#199647` | 5.0:1 |
| 3 | ![](assets/swatches/golden-orange.svg) | Yellow | `#ee9b00` | 8.5:1 |
| 4 | ![](assets/swatches/azure.svg) | Blue | `#00b4d8` | 7.7:1 |
| 5 | ![](assets/swatches/electric-violet.svg) | Magenta | `#ab51e3` | 4.6:1 |
| 6 | ![](assets/swatches/lagoon-teal.svg) | Cyan | `#008388` | 4.2:1 |
| 7 | ![](assets/swatches/vanilla-custard.svg) | White | `#e9d8a6` | 13.5:1 |

### ANSI — bright

| # | Swatch | Role | Hex | Contrast vs. bg |
|---|---|---|---|---|
| 8 | ![](assets/swatches/stone-gray.svg) | Bright black | `#566165` | 3.0:1 |
| 9 | ![](assets/swatches/molten-rust.svg) | Bright red | `#da5b2d` | 5.0:1 |
| 10 | ![](assets/swatches/neon-lime.svg) | Bright green | `#8fe259` | 12.0:1 |
| 11 | ![](assets/swatches/marigold.svg) | Bright yellow | `#febd5c` | 11.5:1 |
| 12 | ![](assets/swatches/sky-flash.svg) | Bright blue | `#0ad6ff` | 11.0:1 |
| 13 | ![](assets/swatches/lilac-flash.svg) | Bright magenta | `#cf76ff` | 7.0:1 |
| 14 | ![](assets/swatches/pearl-aqua.svg) | Bright cyan | `#65dcb9` | 11.3:1 |
| 15 | ![](assets/swatches/warm-ivory.svg) | Bright white | `#f6ebca` | 16.0:1 |

All 16 slots are unique.

### Palette

Every color the current theme actually uses, named:

| Swatch | Name | Hex | Used as |
|---|---|---|---|
| ![](assets/swatches/ink-black.svg) | Ink Black | `#001219` | background, black |
| ![](assets/swatches/vanilla-custard.svg) | Vanilla Custard | `#e9d8a6` | foreground, white, selection text |
| ![](assets/swatches/golden-orange.svg) | Golden Orange | `#ee9b00` | cursor, yellow |
| ![](assets/swatches/crimson-ember.svg) | Crimson Ember | `#c23626` | red |
| ![](assets/swatches/molten-rust.svg) | Molten Rust | `#da5b2d` | bright red |
| ![](assets/swatches/forest-kelly.svg) | Forest Kelly | `#199647` | green |
| ![](assets/swatches/neon-lime.svg) | Neon Lime | `#8fe259` | bright green |
| ![](assets/swatches/azure.svg) | Azure | `#00b4d8` | blue |
| ![](assets/swatches/sky-flash.svg) | Sky Flash | `#0ad6ff` | bright blue |
| ![](assets/swatches/electric-violet.svg) | Electric Violet | `#ab51e3` | magenta |
| ![](assets/swatches/lilac-flash.svg) | Lilac Flash | `#cf76ff` | bright magenta |
| ![](assets/swatches/lagoon-teal.svg) | Lagoon Teal | `#008388` | cyan |
| ![](assets/swatches/pearl-aqua.svg) | Pearl Aqua | `#65dcb9` | bright cyan |
| ![](assets/swatches/stone-gray.svg) | Stone Gray | `#566165` | bright black |
| ![](assets/swatches/marigold.svg) | Marigold | `#febd5c` | bright yellow |
| ![](assets/swatches/warm-ivory.svg) | Warm Ivory | `#f6ebca` | bright white |
| ![](assets/swatches/deep-indigo.svg) | Deep Indigo | `#4376c2` | selection background |

## Regenerating

Every file in this repo (all nine terminal configs, the two reference SVGs, and the
per-color swatch images used in the tables above) is generated from a single palette
dict in [`scripts/build.py`](scripts/build.py). To change a color, edit `FINAL` in that
file and re-run:

```sh
python3 scripts/build.py
```

The script asserts, before writing anything:

- all 16 ANSI hexes are unique — no collisions, intentional or otherwise,
- every bright color is lighter (higher OKLab L) than its normal counterpart,
- every normal-row color clears 3.5:1 contrast against the background, every other
  bright-row color clears 5:1, and bright-black clears 2.9:1 against the background
  *and* 4.5:1 with foreground text drawn on top of it,
- every hue-bearing accent color sits at ≥65% of the maximum chroma reachable at its
  own lightness and hue.

If an edit fails one of those, the script exits with an assertion error instead of
writing a file that quietly breaks the guarantees above.

## License

MIT — see [LICENSE](LICENSE).
