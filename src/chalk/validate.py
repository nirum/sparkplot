import math
from typing import Literal


def validate_numbers(data: object, name: str = "data") -> list[float]:
    """Validate that data is an iterable of int/float and convert to list[float]."""
    try:
        items = list(data)  # type: ignore[arg-type]
    except TypeError:
        raise ValueError(f"{name} must be an iterable of numbers")
    if len(items) == 0:
        raise ValueError("empty data")
    result: list[float] = []
    for i, v in enumerate(items):
        if not isinstance(v, (int, float)):
            raise ValueError(f"{name}[{i}] is not a number: {v!r}")
        fv = float(v)
        if math.isnan(fv):
            raise ValueError(f"{name}[{i}] is NaN")
        if math.isinf(fv):
            raise ValueError(f"{name}[{i}] is inf")
        result.append(fv)
    return result


def validate_xy(
    x: object | None, y: object
) -> tuple[list[float], list[float]]:
    """Validate and normalize x/y data for line plots."""
    y_vals = validate_numbers(y, "y")
    if x is None:
        x_vals = [float(i) for i in range(len(y_vals))]
    else:
        x_vals = validate_numbers(x, "x")
        if len(x_vals) != len(y_vals):
            raise ValueError(
                f"x and y must have the same length (got {len(x_vals)} and {len(y_vals)})"
            )
    return x_vals, y_vals


def validate_dimensions(width: int, height: int) -> None:
    if width < 10:
        raise ValueError(f"width must be >= 10, got {width}")
    if height < 10:
        raise ValueError(f"height must be >= 10, got {height}")


def validate_charset(charset: str) -> Literal["unicode", "ascii"]:
    if charset not in ("unicode", "ascii"):
        raise ValueError(f"charset must be 'unicode' or 'ascii', got {charset!r}")
    return charset  # type: ignore[return-value]


def validate_render(render: str) -> Literal["print", "string"]:
    if render not in ("print", "string"):
        raise ValueError(f"render must be 'print' or 'string', got {render!r}")
    return render  # type: ignore[return-value]


def validate_bins(bins: int) -> int:
    if not isinstance(bins, int) or bins < 1:
        raise ValueError(f"bins must be a positive integer, got {bins!r}")
    return bins
