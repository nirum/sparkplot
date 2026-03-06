# sketchplot

A small Python library for rendering plots as plain text to stdout. No dependencies beyond the Python standard library.

## Install

```
pip install sketchplot
```

## Usage

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

## Sample Output

### Line plot

```
  25┤                                                           ─
    │                                                         ─/
    │                                                        /
    │                                                      ─/
    │                                                     /
    │                                                   ─/
    │                    ─\                            /
    │                  ─/  ──\                       ─/
    │                 /       ─\                   ─/
17.5┤               ─/          ──\               /
    │              /               ──\          ─/
    │            ─/                   ─\       /
    │           /                       ──\  ─/
    │         ─/                           ─/
    │       ─/
    │      /
    │    ─/
    │   /
    │ ─/
  10┤/
    └┬──────────────┬──────────────┬─────────────┬──────────────┬
     0            0.75            1.5          2.25             3
```

### Histogram

```
    Latency
2┤██       ██ ██
 │██       ██ ██
 │██       ██ ██
 │██       ██ ██
 │██       ██ ██
 │██       ██ ██
 │██       ██ ██
 │██       ██ ██
 │██       ██ ██
1┤██       ██ ██
 │██    ██ ██ ██
 │██    ██ ██ ██
 │██    ██ ██ ██
 │██    ██ ██ ██
 │██    ██ ██ ██
 │██    ██ ██ ██
 │██    ██ ██ ██
 │██    ██ ██ ██
 │██    ██ ██ ██
0┤██    ██ ██ ██
 └──────────────
  1.2  1.96  2.7
```

## Parameters

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `width` | `int` | `60` | Canvas width in characters |
| `height` | `int` | `20` | Canvas height in characters |
| `title` | `str \| None` | `None` | Printed above the plot |
| `charset` | `"unicode" \| "ascii"` | `"unicode"` | Character set for drawing |
| `render` | `"print" \| "string"` | `"print"` | Output mode |
| `bins` | `int` | `10` | Number of bins (hist only) |

## Development

```bash
uv sync
uv run pytest
uv tool run ty check
```
