import pathlib
import random

import pytest

import sketchplot as sp

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


def _read_fixture(name: str) -> str:
    return (FIXTURES / name).read_text()


class TestHistSnapshot:
    def test_basic_unicode(self) -> None:
        result = sp.hist(
            [1.2, 1.3, 2.1, 2.4, 2.5, 3.0, 3.1],
            bins=5,
            title="Latency",
            render="string",
        )
        assert result == _read_fixture("hist_basic_unicode.txt")

    def test_basic_ascii(self) -> None:
        result = sp.hist(
            [1.2, 1.3, 2.1, 2.4, 2.5, 3.0, 3.1],
            bins=5,
            title="Latency",
            render="string",
            charset="ascii",
        )
        assert result == _read_fixture("hist_basic_ascii.txt")

    def test_large_unicode(self) -> None:
        random.seed(42)
        data = [random.gauss(50, 15) for _ in range(100)]
        result = sp.hist(data, bins=10, title="Distribution", render="string")
        assert result == _read_fixture("hist_large_unicode.txt")

    def test_large_ascii(self) -> None:
        random.seed(42)
        data = [random.gauss(50, 15) for _ in range(100)]
        result = sp.hist(
            data, bins=10, title="Distribution", render="string", charset="ascii"
        )
        assert result == _read_fixture("hist_large_ascii.txt")

    def test_single_bin_unicode(self) -> None:
        result = sp.hist([1, 2, 3, 4, 5], bins=1, render="string")
        assert result == _read_fixture("hist_single_bin_unicode.txt")

    def test_single_bin_ascii(self) -> None:
        result = sp.hist([1, 2, 3, 4, 5], bins=1, render="string", charset="ascii")
        assert result == _read_fixture("hist_single_bin_ascii.txt")


class TestHistEdgeCases:
    def test_all_same_value(self) -> None:
        result = sp.hist([5, 5, 5, 5], bins=3, render="string")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_one_data_point(self) -> None:
        result = sp.hist([42], bins=1, render="string")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_print_mode(self, capsys: pytest.CaptureFixture[str]) -> None:
        result = sp.hist([1, 2, 3, 4, 5], bins=3, render="print")
        assert result is None
        captured = capsys.readouterr()
        assert len(captured.out) > 0


class TestHistValidation:
    def test_empty_data(self) -> None:
        with pytest.raises(ValueError, match="empty data"):
            sp.hist([], render="string")

    def test_invalid_bins(self) -> None:
        with pytest.raises(ValueError, match="positive integer"):
            sp.hist([1, 2, 3], bins=0, render="string")

    def test_nan_data(self) -> None:
        with pytest.raises(ValueError, match="NaN"):
            sp.hist([1.0, float("nan")], render="string")
