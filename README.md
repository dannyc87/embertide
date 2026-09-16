# EmberTide

A dark terminal theme, built and checked in OKLCH for consistent contrast, hue
separation, and saturation across every ANSI slot.

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

- **Contrast** — every normal-row ANSI color and bright-black clear ≥3.5:1 against the
  `#001219` background; every other bright-row color clears ≥5:1.
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
into your user or workspace `settings.json`.

## Color reference

### Core roles

| Role | Hex |
|---|---|
| Background | `#001219` |
| Foreground | `#e9d8a6` |
| Cursor | `#ee9b00` |
| Selection background | `#4376c2` |

### ANSI — normal

| # | Role | Hex | Contrast vs. bg |
|---|---|---|---|
| 0 | Black | `#001219` | — |
| 1 | Red | `#c23626` | 3.5:1 |
| 2 | Green | `#199647` | 5.0:1 |
| 3 | Yellow | `#ee9b00` | 8.5:1 |
| 4 | Blue | `#00b4d8` | 7.7:1 |
| 5 | Magenta | `#ab51e3` | 4.6:1 |
| 6 | Cyan | `#008388` | 4.2:1 |
| 7 | White | `#e9d8a6` | 13.5:1 |

### ANSI — bright

| # | Role | Hex | Contrast vs. bg |
|---|---|---|---|
| 8 | Bright black | `#6d787c` | 4.2:1 |
| 9 | Bright red | `#da5b2d` | 5.0:1 |
| 10 | Bright green | `#8fe259` | 12.0:1 |
| 11 | Bright yellow | `#febd5c` | 11.5:1 |
| 12 | Bright blue | `#0ad6ff` | 11.0:1 |
| 13 | Bright magenta | `#cf76ff` | 7.0:1 |
| 14 | Bright cyan | `#65dcb9` | 11.3:1 |
| 15 | Bright white | `#f6ebca` | 16.0:1 |

All 16 slots are unique.

### Palette

Every color the current theme actually uses, named:

| Name | Hex | Used as |
|---|---|---|
| Ink Black | `#001219` | background, black |
| Vanilla Custard | `#e9d8a6` | foreground, white, selection text |
| Golden Orange | `#ee9b00` | cursor, yellow |
| Crimson Ember | `#c23626` | red |
| Molten Rust | `#da5b2d` | bright red |
| Forest Kelly | `#199647` | green |
| Neon Lime | `#8fe259` | bright green |
| Azure | `#00b4d8` | blue |
| Sky Flash | `#0ad6ff` | bright blue |
| Electric Violet | `#ab51e3` | magenta |
| Lilac Flash | `#cf76ff` | bright magenta |
| Lagoon Teal | `#008388` | cyan |
| Pearl Aqua | `#65dcb9` | bright cyan |
| Stone Gray | `#6d787c` | bright black |
| Marigold | `#febd5c` | bright yellow |
| Warm Ivory | `#f6ebca` | bright white |
| Deep Indigo | `#4376c2` | selection background |

## Regenerating

Every file in this repo (all nine terminal configs plus the two reference SVGs) is
generated from a single palette dict in [`scripts/build.py`](scripts/build.py). To
change a color, edit `FINAL` in that file and re-run:

```sh
python3 scripts/build.py
```

The script asserts, before writing anything:

- all 16 ANSI hexes are unique — no collisions, intentional or otherwise,
- every bright color is lighter (higher OKLab L) than its normal counterpart,
- every normal-row color (and bright-black) clears 3.5:1 contrast against the
  background, and every other bright-row color clears 5:1,
- every hue-bearing accent color sits at ≥65% of the maximum chroma reachable at its
  own lightness and hue.

If an edit fails one of those, the script exits with an assertion error instead of
writing a file that quietly breaks the guarantees above.

## License

MIT — see [LICENSE](LICENSE).
