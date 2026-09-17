# EmberTide Spec

This is the single canonical definition of how the EmberTide palette maps to semantic
roles — comment, keyword, function, type, and so on — across every implementation.
[`embertide-vscode`](https://github.com/dannyc87/embertide-vscode) and
[`embertide-jetbrains`](https://github.com/dannyc87/embertide-jetbrains) both implement
this contract; this document exists so the two can be checked against a single source of
truth instead of drifting from each other one `build.py` at a time.

The palette itself, the OKLCH design methodology, and the contrast/saturation floors
every color is checked against are defined in this repo's [README](README.md#design) —
this document only covers the *role mapping*, not the color values or how they were
chosen.

## Core roles

| Role | Named color |
|---|---|
| Background | Ink Black |
| Foreground | Vanilla Custard |
| Cursor / accent | Golden Orange |
| Selection background | Deep Indigo |
| Dim / de-emphasized UI | Stone Gray (bright black) |

"Accent" and "dim" recur constantly below — accent marks the one CTA-like highlight
color (cursor, active-tab underline, primary buttons); dim marks anything intentionally
de-emphasized (comments, punctuation, borders, inactive UI).

## ANSI mapping

The terminal's 16 ANSI slots are the root of everything else — both editor themes reuse
this exact mapping for their embedded terminal/console panels (VS Code's `terminal.ansi*`
keys, JetBrains's `BLOCK_TERMINAL_*` and `CONSOLE_*_OUTPUT` keys).

| # | Role | Named color |
|---|---|---|
| 0 / 8 | Black / bright black | Ink Black / Stone Gray |
| 1 / 9 | Red / bright red | Crimson Ember / Molten Rust |
| 2 / 10 | Green / bright green | Forest Kelly / Neon Lime |
| 3 / 11 | Yellow / bright yellow | Golden Orange / Marigold |
| 4 / 12 | Blue / bright blue | Azure / Sky Flash |
| 5 / 13 | Magenta / bright magenta | Electric Violet / Lilac Flash |
| 6 / 14 | Cyan / bright cyan | Lagoon Teal / Pearl Aqua |
| 7 / 15 | White / bright white | Vanilla Custard / Warm Ivory |

See the main [README's color reference](README.md#color-reference) for exact hex values.

## Syntax roles

The core mapping, realized as a VS Code TextMate scope (+ semantic token type where it
adds real value) and a JetBrains `TextAttributesKey`. "—" means not implemented for that
platform; see [Known platform gaps](#known-platform-gaps) below for *why*, where it's a
real platform limitation rather than an oversight.

| Role | Color | VS Code scope(s) | JetBrains key(s) |
|---|---|---|---|
| Comment | dim, italic | `comment` | `DEFAULT_LINE_COMMENT`/`BLOCK_COMMENT`/`DOC_COMMENT` |
| String | green | `string` | `DEFAULT_STRING` |
| Regexp | cyan | `string.regexp` | `JS.REGEXP` |
| Number | accent | `constant.numeric` | `DEFAULT_NUMBER` |
| Language constant | magenta | `constant.language`/`constant.character` | `DEFAULT_CONSTANT` |
| Keyword | magenta (italic in the Italic variant) | `keyword.control`/`keyword.other`/`storage.type`/`storage.modifier` | `DEFAULT_KEYWORD` (+ explicit `PY.KEYWORD`/`JS.KEYWORD` — see gaps) |
| Control flow | red (italic in the Italic variant) | `keyword.control.flow`/`.trycatch`/`.exception` | — (see gaps) |
| Operator | foreground (plain) | `keyword.operator` | `DEFAULT_OPERATION_SIGN` |
| Function / method | blue | `entity.name.function`/`support.function`/`meta.function-call` (+ semantic `function`/`method`) | `DEFAULT_FUNCTION_DECLARATION`/`FUNCTION_CALL`/`INSTANCE_METHOD`/`STATIC_METHOD` |
| Class / type / interface | bright yellow | `entity.name.class`/`.type`/`support.class`/`support.type` (+ semantic `class`/`interface`/`enum`/`type`/`typeParameter`) | `DEFAULT_CLASS_NAME`/`INTERFACE_NAME`/`CLASS_REFERENCE` |
| Variable / property | foreground (plain) | `variable` (+ semantic `variable`/`property`) | `DEFAULT_IDENTIFIER`/`LOCAL_VARIABLE`/`INSTANCE_FIELD` |
| Parameter | bright cyan | `variable.parameter` (+ semantic `parameter`) | `DEFAULT_PARAMETER` |
| Language variable (`this`) | bright cyan, italic | `variable.language` | — for JS/TS, real for Python's `self` (see gaps) |
| Tag | red | `entity.name.tag` | `DEFAULT_TAG`/`HTML_TAG_NAME`/`XML_TAG_NAME` |
| Attribute name | bright yellow | `entity.other.attribute-name` | `HTML_ATTRIBUTE_NAME`/`XML_ATTRIBUTE_NAME` |
| Decorator / annotation | cyan | `meta.decorator`/`punctuation.decorator`/`entity.name.function.decorator` | `DEFAULT_METADATA`/`PY.DECORATOR` (+ semantic `decorator`) |
| Punctuation | dim | `punctuation` | `DEFAULT_BRACES`/`BRACKETS`/`DOT`/`SEMICOLON`/`COMMA`/`PARENTHS` |
| Template/string interpolation | foreground (plain) | `punctuation.definition.template-expression`/`meta.template.expression` | `DEFAULT_TEMPLATE_LANGUAGE_COLOR`/`PY.FSTRING_FRAGMENT_BRACES` |
| Invalid / bad character | red | `invalid`/`invalid.illegal` | `DEFAULT_INVALID_STRING_ESCAPE`/`BAD_CHARACTER` |
| Deprecated | strikethrough (no recolor) | not yet implemented in VS Code | `DEPRECATED_ATTRIBUTES`/`MARKED_FOR_REMOVAL_ATTRIBUTES` |
| Markdown heading | accent, bold | `markup.heading` | `MARKDOWN_HEADER_LEVEL_1`–`6` |
| Markdown bold / italic | foreground, bold/italic | `markup.bold`/`markup.italic` | `MARKDOWN_BOLD`/`MARKDOWN_ITALIC` |
| Markdown code span / block | bright cyan | `markup.inline.raw` | `MARKDOWN_CODE_SPAN`/`MARKDOWN_CODE_BLOCK`/`MARKDOWN_CODE_FENCE` |
| Markdown quote | dim, italic | `markup.quote` | `MARKDOWN_BLOCK_QUOTE` |
| Markdown link | blue, underlined | `string.other.link.title`/`markup.underline.link` | `MARKDOWN_LINK_TEXT`/`MARKDOWN_AUTO_LINK` |
| Markdown strikethrough | dim strikethrough | `markup.strikethrough` | `MARKDOWN_STRIKE_THROUGH` |
| YAML key | bright yellow | n/a (no dedicated VS Code rule yet) | `YAML_SCALAR_KEY` |
| YAML value | foreground (plain) | n/a | `YAML_SCALAR_VALUE`/`YAML_TEXT` |
| JSON property key | bright yellow | n/a | `JSON.PROPERTY_KEY` |
| Errors / unresolved references | red, wave-underline effect only (no recolor) | not yet implemented in VS Code | `ERRORS_ATTRIBUTES`/`WRONG_REFERENCES_ATTRIBUTES` |
| Warnings | bright yellow, wave-underline effect only | not yet implemented in VS Code | `WARNING_ATTRIBUTES` |

## Known platform gaps

These are real, verified platform limitations, not unfinished work — each was confirmed
against the actual platform source or documented behavior before being accepted rather
than assumed.

- **JetBrains cannot separate "control flow" keywords (`if`/`return`/`throw`/`await`)
  from general keywords (`class`/`const`/`private`).** The base `DefaultLanguageHighlighterColors`
  set has one `KEYWORD` bucket; there is no finer split, in Python or JS/TS. VS Code's
  TextMate grammars expose `keyword.control.flow` as a distinct scope, which is why the
  VS Code edition can give Control flow its own red while the JetBrains edition can't.
- **JetBrains cannot color JS/TS's `this` differently from other keywords, but Python's
  `self` works.** `self` isn't a real keyword — it's just a naming convention — so
  Python's plugin needs (and has) a dedicated `PY.SELF_PARAMETER` key to recognize it at
  all. `this` in JS/TS *is* a genuine reserved word, so it falls into the same flat
  keyword bucket as the control-flow keywords above. (There's an open JetBrains YouTrack
  request for semantic highlighting in JS/TS/JSON, which corroborates this — it wouldn't
  be a feature request if the distinction already existed.)
- **VS Code's semantic token coloring (imports/references resolved by real type, e.g. a
  class import rendering in the type color) only reaches usage/call sites, not the
  `import { ... }` declaration line itself.** TypeScript's semantic tokens provider
  classifies a name based on how it's used at a given reference, not at its declaration —
  confirmed via VS Code's own "Inspect Editor Tokens and Scopes" tool. JetBrains's
  semantic analysis extends to the import line itself; this is a genuine difference in
  how the two platforms scope semantic analysis, not a theme configuration gap.
- **Serverless Framework's own `${...}` variable syntax gets no special treatment in
  YAML**, even though GitHub Actions' `${{ }}` does. GitHub Actions has dedicated,
  purpose-built language-injection support scoped to `.github/workflows/*.yml` and
  `action.yml`; Serverless Framework's variable syntax has no equivalent parser
  recognizing it as an injected language, so there's no syntax node for any theme to
  color — this would need a Serverless-Framework-aware IDE plugin to exist first.

## Adding a new platform

If EmberTide ever grows a fourth implementation (Vim, Sublime, etc.), the process is:
find that platform's real scope/attribute-key names (never assume a naming convention
carries over from another platform — half the entries in Known platform gaps above exist
because it doesn't), add a row to the Syntax roles table above, and implement it.
