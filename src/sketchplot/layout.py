from sketchplot.canvas import Canvas
from sketchplot.charset import CharSet
from sketchplot.scale import Scale


def _format_tick(value: float) -> str:
    """Format a tick value for display."""
    if value == int(value) and abs(value) < 1e10:
        return str(int(value))
    formatted = f"{value:.2f}"
    # Strip trailing zeros after decimal
    if "." in formatted:
        formatted = formatted.rstrip("0").rstrip(".")
    return formatted


def assemble_line_plot(
    canvas: Canvas,
    x_scale: Scale,
    y_scale: Scale,
    cs: CharSet,
    title: str | None = None,
    width: int = 60,
) -> str:
    """Assemble the full plot frame with axes, labels, and title."""
    # Y-axis ticks (3 labels: bottom, middle, top)
    y_ticks = y_scale.ticks(3)
    y_labels = [_format_tick(v) for v in y_ticks]
    y_label_width = max(len(lbl) for lbl in y_labels)

    # X-axis ticks
    n_x_ticks = min(5, max(3, canvas.width // 12))
    x_ticks = x_scale.ticks(n_x_ticks)
    x_labels = [_format_tick(v) for v in x_ticks]
    x_pixel_positions = [x_scale.apply(v) for v in x_ticks]

    canvas_str = canvas.to_string()
    canvas_lines = canvas_str.split("\n")

    # Y-axis pixel positions for tick marks
    y_tick_pixels = [y_scale.apply(v) for v in y_ticks]

    lines: list[str] = []

    # Title
    if title is not None:
        total_width = y_label_width + 1 + canvas.width
        if len(title) > total_width:
            title = title[: total_width - 1] + "\u2026"
        padding = (total_width - len(title)) // 2
        lines.append(" " * padding + title)

    # Canvas rows with y-axis
    for row_idx, canvas_line in enumerate(canvas_lines):
        # row_idx 0 = top of canvas = y = height-1
        y_val = canvas.height - 1 - row_idx

        # Check if this row has a tick mark
        y_label_str = ""
        tick_char = cs.vertical
        for i, tp in enumerate(y_tick_pixels):
            if tp == y_val:
                y_label_str = y_labels[i]
                tick_char = cs.tick_y
                break

        padded_label = y_label_str.rjust(y_label_width)
        lines.append(f"{padded_label}{tick_char}{canvas_line}")

    # X-axis line
    x_axis_chars = [cs.horizontal] * canvas.width
    for px in x_pixel_positions:
        if 0 <= px < canvas.width:
            x_axis_chars[px] = cs.tick_x

    x_axis_prefix = " " * y_label_width + cs.corner_bl
    lines.append(x_axis_prefix + "".join(x_axis_chars))

    # X-axis labels
    label_line = [" "] * (y_label_width + 1 + canvas.width)
    for i, px in enumerate(x_pixel_positions):
        lbl = x_labels[i]
        pos = y_label_width + 1 + px - len(lbl) // 2
        pos = max(0, pos)
        # Check for overlap with previous label
        for j, ch in enumerate(lbl):
            p = pos + j
            if p < len(label_line):
                label_line[p] = ch

    lines.append("".join(label_line).rstrip())

    return "\n".join(lines)


def assemble_hist_plot(
    canvas: Canvas,
    counts: list[int],
    edges: list[float],
    y_scale: Scale,
    cs: CharSet,
    title: str | None = None,
    bar_width: int = 2,
    gap: int = 1,
) -> str:
    """Assemble histogram plot with axes and labels."""
    # Y-axis: show count ticks
    max_count = max(counts) if counts else 0
    y_ticks = y_scale.ticks(3)
    y_labels = [_format_tick(v) for v in y_ticks]
    y_label_width = max(len(lbl) for lbl in y_labels)

    y_tick_pixels = [y_scale.apply(v) for v in y_ticks]

    canvas_str = canvas.to_string()
    canvas_lines = canvas_str.split("\n")

    lines: list[str] = []

    # Title
    if title is not None:
        total_width = y_label_width + 1 + canvas.width
        if len(title) > total_width:
            title = title[: total_width - 1] + "\u2026"
        padding = (total_width - len(title)) // 2
        lines.append(" " * padding + title)

    # Canvas rows with y-axis
    for row_idx, canvas_line in enumerate(canvas_lines):
        y_val = canvas.height - 1 - row_idx

        y_label_str = ""
        tick_char = cs.vertical
        for i, tp in enumerate(y_tick_pixels):
            if tp == y_val:
                y_label_str = y_labels[i]
                tick_char = cs.tick_y
                break

        padded_label = y_label_str.rjust(y_label_width)
        lines.append(f"{padded_label}{tick_char}{canvas_line}")

    # X-axis line
    x_axis_prefix = " " * y_label_width + cs.corner_bl
    x_axis_line = cs.horizontal * canvas.width
    lines.append(x_axis_prefix + x_axis_line)

    # X-axis labels: show bin edge values under each bar center
    n_bins = len(counts)
    label_line = [" "] * (y_label_width + 1 + canvas.width)

    # Show a few evenly spaced bin edge labels
    n_labels = min(n_bins + 1, 5)
    if n_labels <= 1:
        label_indices = [0]
    else:
        label_indices = [
            round(i * n_bins / (n_labels - 1)) for i in range(n_labels)
        ]
    label_indices = sorted(set(label_indices))

    last_end = -1
    for idx in label_indices:
        if idx > len(edges) - 1:
            continue
        lbl = _format_tick(edges[idx])
        if idx < n_bins:
            px = idx * (bar_width + gap) + bar_width // 2
        else:
            px = (n_bins - 1) * (bar_width + gap) + bar_width
        pos = y_label_width + 1 + px - len(lbl) // 2
        pos = max(0, pos)
        # Skip if overlapping with previous label
        if pos <= last_end:
            continue
        for j, ch in enumerate(lbl):
            p = pos + j
            if p < len(label_line):
                label_line[p] = ch
        last_end = pos + len(lbl)

    lines.append("".join(label_line).rstrip())

    return "\n".join(lines)
