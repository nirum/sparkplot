import math

import pytest

from sketchplot.validate import (
    validate_bins,
    validate_charset,
    validate_dimensions,
    validate_numbers,
    validate_render,
    validate_xy,
)


class TestValidateNumbers:
    def test_valid_ints(self) -> None:
        assert validate_numbers([1, 2, 3]) == [1.0, 2.0, 3.0]

    def test_valid_floats(self) -> None:
        assert validate_numbers([1.5, 2.5]) == [1.5, 2.5]

    def test_mixed(self) -> None:
        assert validate_numbers([1, 2.5, 3]) == [1.0, 2.5, 3.0]

    def test_empty(self) -> None:
        with pytest.raises(ValueError, match="empty data"):
            validate_numbers([])

    def test_nan(self) -> None:
        with pytest.raises(ValueError, match="NaN"):
            validate_numbers([1.0, float("nan")])

    def test_inf(self) -> None:
        with pytest.raises(ValueError, match="inf"):
            validate_numbers([1.0, float("inf")])

    def test_negative_inf(self) -> None:
        with pytest.raises(ValueError, match="inf"):
            validate_numbers([float("-inf")])

    def test_non_number(self) -> None:
        with pytest.raises(ValueError, match="not a number"):
            validate_numbers([1, "two", 3])

    def test_not_iterable(self) -> None:
        with pytest.raises(ValueError, match="iterable"):
            validate_numbers(42)


class TestValidateXY:
    def test_y_only(self) -> None:
        x, y = validate_xy(None, [10, 20, 30])
        assert x == [0.0, 1.0, 2.0]
        assert y == [10.0, 20.0, 30.0]

    def test_x_and_y(self) -> None:
        x, y = validate_xy([1, 2, 3], [10, 20, 30])
        assert x == [1.0, 2.0, 3.0]
        assert y == [10.0, 20.0, 30.0]

    def test_length_mismatch(self) -> None:
        with pytest.raises(ValueError, match="same length"):
            validate_xy([1, 2], [10, 20, 30])


class TestValidateDimensions:
    def test_valid(self) -> None:
        validate_dimensions(60, 20)  # no exception

    def test_width_too_small(self) -> None:
        with pytest.raises(ValueError, match="width must be >= 10"):
            validate_dimensions(9, 20)

    def test_height_too_small(self) -> None:
        with pytest.raises(ValueError, match="height must be >= 10"):
            validate_dimensions(60, 9)


class TestValidateCharset:
    def test_unicode(self) -> None:
        assert validate_charset("unicode") == "unicode"

    def test_ascii(self) -> None:
        assert validate_charset("ascii") == "ascii"

    def test_invalid(self) -> None:
        with pytest.raises(ValueError, match="charset"):
            validate_charset("utf-8")


class TestValidateRender:
    def test_print(self) -> None:
        assert validate_render("print") == "print"

    def test_string(self) -> None:
        assert validate_render("string") == "string"

    def test_invalid(self) -> None:
        with pytest.raises(ValueError, match="render"):
            validate_render("html")


class TestValidateBins:
    def test_valid(self) -> None:
        assert validate_bins(10) == 10

    def test_zero(self) -> None:
        with pytest.raises(ValueError, match="positive integer"):
            validate_bins(0)

    def test_negative(self) -> None:
        with pytest.raises(ValueError, match="positive integer"):
            validate_bins(-1)

    def test_float(self) -> None:
        with pytest.raises(ValueError, match="positive integer"):
            validate_bins(3.5)  # type: ignore[arg-type]
