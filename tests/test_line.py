import pathlib

import pytest

import sparkplot as sp

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


def _read_fixture(name: str) -> str:
    return (FIXTURES / name).read_text()


class TestLineSnapshot:
    def test_basic_unicode(self) -> None:
        result = sp.line([1, 4, 2, 8, 5, 7], render="string")
        assert result == _read_fixture("line_basic_unicode.txt")

    def test_basic_ascii(self) -> None:
        result = sp.line([1, 4, 2, 8, 5, 7], render="string", charset="ascii")
        assert result == _read_fixture("line_basic_ascii.txt")

    def test_title_unicode(self) -> None:
        result = sp.line(
            [0, 1, 2, 3], [10, 20, 15, 25], title="Requests/sec", render="string"
        )
        assert result == _read_fixture("line_title_unicode.txt")

    def test_title_ascii(self) -> None:
        result = sp.line(
            [0, 1, 2, 3],
            [10, 20, 15, 25],
            title="Requests/sec",
            render="string",
            charset="ascii",
        )
        assert result == _read_fixture("line_title_ascii.txt")

    def test_small_unicode(self) -> None:
        result = sp.line([1, 3, 2], width=20, height=10, render="string")
        assert result == _read_fixture("line_small_unicode.txt")

    def test_small_ascii(self) -> None:
        result = sp.line(
            [1, 3, 2], width=20, height=10, render="string", charset="ascii"
        )
        assert result == _read_fixture("line_small_ascii.txt")


class TestLineEdgeCases:
    def test_single_point_unicode(self) -> None:
        result = sp.line([5], width=20, height=10, render="string")
        assert result == _read_fixture("line_single_point_unicode.txt")

    def test_single_point_ascii(self) -> None:
        result = sp.line([5], width=20, height=10, render="string", charset="ascii")
        assert result == _read_fixture("line_single_point_ascii.txt")

    def test_constant_unicode(self) -> None:
        result = sp.line([5, 5, 5, 5], width=20, height=10, render="string")
        assert result == _read_fixture("line_constant_unicode.txt")

    def test_constant_ascii(self) -> None:
        result = sp.line(
            [5, 5, 5, 5], width=20, height=10, render="string", charset="ascii"
        )
        assert result == _read_fixture("line_constant_ascii.txt")

    def test_minimum_canvas(self) -> None:
        result = sp.line([1, 4, 2, 8], width=10, height=10, render="string")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_large_dataset(self) -> None:
        result = sp.line(list(range(10000)), render="string")
        assert isinstance(result, str)


class TestLinePrint:
    def test_print_mode_returns_none(self, capsys: pytest.CaptureFixture[str]) -> None:
        result = sp.line([1, 2, 3], render="print")
        assert result is None
        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_string_mode_returns_string(self) -> None:
        result = sp.line([1, 2, 3], render="string")
        assert isinstance(result, str)
        assert len(result) > 0


class TestLineValidation:
    def test_empty_data(self) -> None:
        with pytest.raises(ValueError, match="empty data"):
            sp.line([], render="string")

    def test_nan_data(self) -> None:
        with pytest.raises(ValueError, match="NaN"):
            sp.line([1.0, float("nan"), 3.0], render="string")

    def test_width_too_small(self) -> None:
        with pytest.raises(ValueError, match="width"):
            sp.line([1, 2, 3], width=5, render="string")

    def test_xy_length_mismatch(self) -> None:
        with pytest.raises(ValueError, match="same length"):
            sp.line([1, 2], [10, 20, 30], render="string")
