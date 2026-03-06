from sketchplot.canvas import Canvas
from sketchplot.charset import CharSet


def _choose_char(dx: int, dy: int, cs: CharSet) -> str:
    """Choose a drawing character based on the direction of a line segment step."""
    if dx == 0 and dy == 0:
        return cs.horizontal
    if dy == 0:
        return cs.horizontal
    if dx == 0:
        return cs.vertical
    if dy > 0 and dx > 0:
        return cs.diagonal_up
    if dy < 0 and dx > 0:
        return cs.diagonal_down
    if dy > 0 and dx < 0:
        return cs.diagonal_up
    return cs.diagonal_down


def draw_line_segment(
    canvas: Canvas, x0: int, y0: int, x1: int, y1: int, cs: CharSet
) -> None:
    """Draw a line segment on the canvas using Bresenham's algorithm."""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    cx, cy = x0, y0
    while True:
        # Determine character based on direction to next point
        step_dx = 0
        step_dy = 0
        if cx != x1 or cy != y1:
            e2 = 2 * err
            if e2 > -dy:
                step_dx = sx
            if e2 < dx:
                step_dy = sy

        char = _choose_char(step_dx, step_dy, cs)
        canvas.set(cx, cy, char)

        if cx == x1 and cy == y1:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            cx += sx
        if e2 < dx:
            err += dx
            cy += sy


def compute_bins(
    data: list[float], bins: int
) -> tuple[list[float], list[int]]:
    """Compute histogram bin edges and counts.

    Returns (edges, counts) where edges has bins+1 elements
    and counts has bins elements.
    """
    lo = min(data)
    hi = max(data)
    if lo == hi:
        hi = lo + 1.0

    bin_width = (hi - lo) / bins
    edges = [lo + i * bin_width for i in range(bins + 1)]
    counts = [0] * bins

    for v in data:
        idx = int((v - lo) / bin_width)
        if idx >= bins:
            idx = bins - 1
        counts[idx] += 1

    return edges, counts


def draw_bars(
    canvas: Canvas,
    counts: list[int],
    max_count: int,
    cs: CharSet,
    bar_width: int = 2,
    gap: int = 1,
) -> None:
    """Draw histogram bars on the canvas."""
    for i, count in enumerate(counts):
        if count == 0:
            continue
        x_start = i * (bar_width + gap)
        if max_count == 0:
            bar_height_exact = 0.0
        else:
            bar_height_exact = count / max_count * canvas.height

        full_rows = int(bar_height_exact)
        has_half = bar_height_exact - full_rows >= 0.5

        for bx in range(bar_width):
            x = x_start + bx
            for y in range(full_rows):
                canvas.set(x, y, cs.block_full)
            if has_half:
                canvas.set(x, full_rows, cs.block_half)
