# sketchplot — Design Document

**A small Python library for rendering plots as plain text to stdout.**

## 1. Overview / Problem Statement

Graphical plotting libraries (matplotlib, plotly, etc.) require a display server, browser, or image backend. This makes them unusable or awkward in common scenarios: SSH sessions, CI pipeline logs, quick debugging, teaching in a terminal, and lightweight scripts where pulling in heavy dependencies is undesirable.

`sketchplot` renders line plots and histograms as text directly to stdout. It targets correctness and simplicity over visual fidelity. The output is deterministic, testable, and readable in any terminal.

## 2. Goals

- Render line plots and histograms as text in the terminal
- Simple, memorable API: `line(y)`, `line(x, y)`, `hist(data, bins=10)`
- Deterministic output for snapshot testing
- Zero dependencies beyond the Python standard library
- Use `uv` for Python environment and project management
- Use `ty` for type checking (https://docs.astral.sh/ty/)
- Use `pytest` for unit and snapshot tests
- Unicode by default, ASCII fallback with an explicit switch
- Print to stdout by default; return string on request
- Small codebase (~500–1000 LOC for v1)

## 3. Non-Goals

- Replacing matplotlib or any full-featured plotting library
- Color or ANSI escape code support (deferred)
- Interactive or animated output
- Image export
- Handling datasets larger than ~10k points efficiently
- Multiple subplots or composite layouts
- Pandas/NumPy integration (users can pass `.tolist()`)

## 4. Target Users and Use Cases

| User | Scenario |
|---|---|
| DevOps engineer | Plotting latency percentiles in a CI log |
| Student | Visualizing algorithm behavior in a terminal |
| Data scientist over SSH | Quick sanity check on a data pipeline |
| Script author | Adding a visual summary to a CLI tool |
| Library author | Embedding plot output in test assertions |

## 5. Proposed API Surface

### Public functions

```python
import sketchplot as sp

# Line plot — y only (x inferred as 0..n-1)
sp.line([1, 4, 2, 8, 5, 7])

# Line plot — explicit x and y
sp.line([0, 1, 2, 3], [10, 20, 15, 25], title="Requests/sec")

# Histogram
sp.hist([1.2, 1.3, 2.1, 2.4, 2.5, 3.0, 3.1], bins=5, title="Latency")

# Return string instead of printing
output = sp.line([1, 4, 2, 8], render="string")

# ASCII fallback
sp.line([1, 4, 2, 8], charset="ascii")
```

### Common parameters

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `width` | `int` | `60` | Canvas width in characters |
| `height` | `int` | `20` | Canvas height in characters |
| `title` | `str \| None` | `None` | Printed above the plot |
| `charset` | `"unicode" \| "ascii"` | `"unicode"` | Character set for drawing |
| `render` | `"print" \| "string"` | `"print"` | Output mode |

### Sample output

```
  Requests/sec
  25┤                        ╭
  20┤          ╭─────╮       │
  15┤          │     ╰───────╯
  10┤──────────╯
    └──┬──┬──┬──┬
       0  1  2  3
```

```
  Latency
  3 │ ██
  2 │ ██ ███
  1 │ ██ ███ ██
    └──────────
```

## 6. Internal Architecture

```
Public API (line, hist)
    │
    ▼
Data normalization & validation
    │
    ▼
Scale computation (data coords → canvas coords)
    │
    ▼
Rasterizer (writes characters to Canvas)
    │
    ▼
Layout engine (assembles axes, labels, title, canvas)
    │
    ▼
Renderer (joins rows → string, optionally prints)
```

Key internal types:

- **`Canvas`** — 2D grid of characters with `set(x, y, char)` and `to_string()`. Origin at bottom-left, y-axis pointing up. Internally stored as a list of lists (row-major, flipped on output).
- **`Scale`** — Maps a data range `[lo, hi]` to an integer pixel range `[0, size-1]`. Linear only in v1. Two methods: `apply(value) → int` and `ticks(n) → list[float]`.
- **`CharSet`** — Named collection of drawing characters (line segments, bar blocks, axes, corners). Two built-in instances: `UNICODE` and `ASCII`.

## 7. Rendering Model

### Line plots

1. Map each `(x, y)` pair to canvas coordinates `(cx, cy)` using `Scale`.
2. Walk consecutive point pairs. For each pair, rasterize a line segment using Bresenham's algorithm (integer arithmetic, deterministic, no floating-point drift).
3. Write characters to the canvas. Character choice depends on segment direction:
   - Horizontal: `─` (unicode) / `-` (ascii)
   - Vertical: `│` / `|`
   - Diagonal up-right: `╭` or `╯` / `/`
   - Diagonal down-right: `╰` or `╮` / `\`

This is deliberately simplified. We are not anti-aliasing or interpolating sub-character positions. Each canvas cell gets exactly one character.

**Tradeoff:** Bresenham gives clean diagonals but can look jagged for smooth curves. This is acceptable for v1 — the output is meant to convey shape, not precision.

### Histograms

1. Compute bin edges (linear spacing between `min(data)` and `max(data)`, or user-specified range).
2. Count values per bin.
3. Scale counts to canvas height.
4. Draw vertical bars using block characters (`█`, `▄` for unicode; `#` for ascii). Each column is one bin, with configurable bar width (default: 2 chars per bin with 1 char gap).

## 8. Data Normalization and Validation

Inputs are validated at the public API boundary:

- `y` (and `x` if provided) must be iterables of `int` or `float`. Converted to `list[float]` immediately.
- `len(x) == len(y)` is enforced when both are provided.
- Empty data raises `ValueError("empty data")`.
- `NaN` and `inf` values are rejected with `ValueError` — no silent dropping. This keeps behavior deterministic and avoids rendering surprises.
- `bins` must be a positive integer.
- `width` and `height` must be >= 10 (below this, output is meaningless).

No implicit type coercion from strings, datetimes, or complex objects. Users pass numbers.

## 9. Axes, Labels, and Layout Strategy

The canvas is embedded in a larger layout frame:

```
[optional title row]
[y-label] [y-axis] [canvas area]
          [x-axis row]
          [x-label row]
```

- **Y-axis**: Right-aligned numeric labels at top, middle, and bottom of the canvas (3 labels). A vertical `│` line with `┤` tick marks. Label width is computed from the formatted numbers.
- **X-axis**: A horizontal `─` line with `┬` tick marks. Labels placed at evenly spaced positions (3–5 labels depending on width). Labels are bottom-aligned and truncated if they overlap.
- **Title**: Centered above the plot. Truncated with `…` if wider than the total frame.

V1 does not support dense ticks, rotated labels, or legends.

## 10. Error Handling

- All validation errors are `ValueError` with descriptive messages.
- No warnings, no silent fallbacks, no partial rendering.
- If the terminal width is unknown, fall back to the default width (60). We will not call `shutil.get_terminal_size()` automatically — explicit sizing keeps output deterministic and testable.

## 11. Testing Strategy

- **Snapshot tests**: The primary testing mechanism. Each test calls a plotting function with `render="string"`, then asserts the result equals a committed `.txt` fixture. This catches any unintentional change to rendering output.
- **Unit tests** for `Canvas`, `Scale`, and `CharSet` independently.
- **Validation tests**: Confirm that bad inputs raise `ValueError` with expected messages.
- **ASCII/Unicode parity tests**: Every snapshot test runs in both charsets to ensure the fallback path works.
- Test framework: `pytest`. No test dependencies beyond pytest.
- Type checking: `ty` (https://docs.astral.sh/ty/) — run as part of the development workflow to catch type errors early.
- Determinism: Since all rendering is integer-arithmetic and there is no randomness or system-dependent behavior, tests should be fully reproducible across platforms.

## 12. Performance Considerations

V1 targets small datasets (up to ~10k points). Performance is not a primary concern, but we avoid obvious traps:

- Canvas is pre-allocated as a 2D list, not built by string concatenation.
- Bresenham's algorithm is O(pixels) per segment — already efficient.
- Histogram binning is a single pass over the data.
- No external dependencies — standard library only. No NumPy, which means we eat the cost of Python loops, but for the target dataset sizes and canvas sizes (max ~200x50 cells), this is negligible.

If profiling later shows a bottleneck, the most likely candidate is line rasterization with many points. The fix would be to downsample points to canvas resolution before rasterizing (deferred).

## 13. Package Structure

```
sketchplot/
├── __init__.py          # Public API: line(), hist()
├── canvas.py            # Canvas class
├── scale.py             # Scale class
├── charset.py           # CharSet definitions (UNICODE, ASCII)
├── rasterize.py         # Bresenham line drawing, bar drawing
├── layout.py            # Axis rendering, label placement, frame assembly
├── validate.py          # Input validation
tests/
├── test_line.py
├── test_hist.py
├── test_canvas.py
├── test_scale.py
├── test_validate.py
├── fixtures/            # Snapshot .txt files
```

Single flat package. No subpackages. ~8 modules, each under 150 LOC.

## 14. v1 Scope vs Deferred Features

| v1 | Deferred |
|---|---|
| Line plots | Scatter plots, bar charts, box plots |
| Histograms | Stacked/grouped histograms |
| Unicode + ASCII charsets | ANSI color support |
| Fixed-size canvas | Auto-detect terminal size |
| Print or return string | Write to file object |
| Linear scale | Log scale |
| Sparse axis labels (3–5) | Dense ticks, custom formatters |
| Single series per plot | Multiple series / legends |
| Standard library only (managed via `uv`) | Optional NumPy/Pandas integration |

## 15. Implementation Plan / Milestones

**Milestone 1 — Canvas and Scale primitives**
- `Canvas`: init, `set()`, `get()`, `to_string()`, fill with space
- `Scale`: `apply()`, `ticks()`
- `CharSet`: unicode and ascii definitions
- Unit tests for all three

**Milestone 2 — Line plot**
- Bresenham rasterizer
- `line()` public function: validation → scale → rasterize → layout → render
- Axis and label rendering
- Snapshot tests (unicode + ascii)

**Milestone 3 — Histogram**
- Bin computation
- Bar rasterizer
- `hist()` public function
- Snapshot tests

**Milestone 4 — Polish and packaging**
- Edge cases (single point, constant data, very small canvas)
- `pyproject.toml` (managed via `uv`), README with examples
- CI with snapshot test verification

## 16. Open Questions / Tradeoffs

**Q: Should `line()` connect points with interpolated segments or just plot markers?**
Recommendation: Connect with segments. Isolated dots are hard to read in text. Segments convey trend.

**Q: How should overlapping characters be handled on the canvas?**
Recommendation: Last-write-wins. For v1, we only support a single series, so conflicts are limited to axis lines crossing data — data should overwrite axes.

**Q: Should we support `file=` argument (like `print()`) instead of `render="string"`?**
Tradeoff: `file=` is more Pythonic for I/O redirection, but `render="string"` is simpler for testing. Recommendation: support both. `render="string"` returns the string; default behavior prints to stdout; `file=` is deferred to post-v1 to keep the API minimal.

**Q: Block characters for histograms — full blocks only, or half-blocks for finer resolution?**
Recommendation: Support half-blocks (`▄`) in unicode mode for 2x vertical resolution. ASCII mode uses `#` only. This is a small implementation cost for noticeably better-looking histograms.

**Q: What happens when the data range is zero (e.g., `line([5, 5, 5])`)?**
Recommendation: Render a flat horizontal line at the vertical center of the canvas. Y-axis shows only the single value. No error.
