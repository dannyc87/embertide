# EmberTide

A dark terminal theme built from a 10-stop teal→ember gradient.

![Palette](assets/palette.svg)

## Preview

![ANSI color grid](assets/ansi-grid.svg)

## Why this exists

The source is a 10-color data-viz gradient (teal → cyan → aqua → gold → caramel → red) with
no true green, blue, or magenta stop. A naive first pass reused the same dark teal for
green, blue, *and* bright-black — which breaks things like `ls` (directories vs.
executables), git prompts, and diff highlighting, all of which depend on those colors
actually being distinguishable.

EmberTide fixes that instead of hiding it:

- **Green, blue, and magenta are all specified directly**, not synthesized from an
  arbitrary hue target. In each pair, one color was hand-picked and the other derived
  only to match its hue at a passing contrast: bright green (`#8fe259`) and bright blue
  (`#0ad6ff`) came with a derived darker normal (`#0a883d`, `#00b4d8`); normal magenta
  (`#ab51e3`) came with a derived lighter bright (`#cf76ff`).
- **Cyan is deepened**, not untouched — once blue moved to a vivid, light azure
  (`#00b4d8`), the original Dark Cyan (`#0a9396`) sat too close to it in OKLab space to
  read as clearly different. Cyan keeps its original hue but drops in lightness and
  gains chroma (`#008388`, 4.2:1) to stay visually distinct.
- **Red is lifted** just enough to clear its text-contrast floor against the `#001219`
  background — the original `#ae2012` sat at ~2.7:1 contrast, unreadable as body text.
- **Bright black, bright yellow, and bright white are specified as real colors** —
  the source palette only had one light stop (Vanilla Custard), so a naive pass left
  white, bright yellow, and bright white all identical, and bright-black nearly
  invisible against the background (2.2:1). Bright black is now an actual neutral gray
  (`#6d787c`, 4.2:1) instead of a colored, barely-there tone; bright yellow (`#febd5c`)
  and bright white (`#f6ebca`) are each distinct from normal white and from each other.
- **Background, foreground, yellow, white, cursor, and selection are untouched** — they
  were already hue-accurate and high-contrast in the source palette.
- **Contrast floors:** ≥3.5:1 for the normal row and for bright-black (it needs to
  actually be visible, not just technically non-black), ≥5:1 for the rest of the
  bright row.

Every claim above is asserted by [`scripts/build.py`](scripts/build.py) — see
[Regenerating](#regenerating) — so it can't silently drift from what's documented here.

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
| Selection background | `#005f73` |

### ANSI — normal

| # | Role | Hex | Contrast vs. bg |
|---|---|---|---|
| 0 | Black | `#001219` | — |
| 1 | Red | `#c23626` | 3.5:1 |
| 2 | Green | `#0a883d` | 4.2:1 |
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
| 14 | Bright cyan | `#94d2bd` | 11.1:1 |
| 15 | Bright white | `#f6ebca` | 16.0:1 |

All 16 slots are unique.

### Palette

Two groups: the original 10-stop source gradient, and the colors specified (or, for
Lagoon Teal, adjusted) by hand rather than derived from a source stop.

**Source (10-stop gradient)**

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

**Specified additions**

| Name | Hex | Used as |
|---|---|---|
| Azure | `#00b4d8` | blue |
| Sky Flash | `#0ad6ff` | bright blue |
| Forest Kelly | `#0a883d` | green |
| Neon Lime | `#8fe259` | bright green |
| Electric Violet | `#ab51e3` | magenta |
| Lilac Flash | `#cf76ff` | bright magenta |
| Lagoon Teal | `#008388` | cyan (deepened from Dark Cyan) |
| Stone Gray | `#6d787c` | bright black |
| Marigold | `#febd5c` | bright yellow |
| Warm Ivory | `#f6ebca` | bright white |

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
  background, and every other bright-row color clears 5:1.

If an edit fails one of those, the script exits with an assertion error instead of
writing a file that quietly breaks the guarantees above.

## License

MIT — see [LICENSE](LICENSE).
