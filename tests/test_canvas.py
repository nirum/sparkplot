from sparkplot.canvas import Canvas


class TestCanvasInit:
    def test_dimensions(self) -> None:
        c = Canvas(10, 5)
        assert c.width == 10
        assert c.height == 5

    def test_filled_with_spaces(self) -> None:
        c = Canvas(3, 2)
        for y in range(2):
            for x in range(3):
                assert c.get(x, y) == " "


class TestCanvasSetGet:
    def test_set_and_get(self) -> None:
        c = Canvas(5, 5)
        c.set(2, 3, "X")
        assert c.get(2, 3) == "X"

    def test_set_out_of_bounds_is_noop(self) -> None:
        c = Canvas(5, 5)
        c.set(-1, 0, "X")
        c.set(0, -1, "X")
        c.set(5, 0, "X")
        c.set(0, 5, "X")
        # No exception, no change

    def test_get_out_of_bounds_returns_space(self) -> None:
        c = Canvas(5, 5)
        assert c.get(-1, 0) == " "
        assert c.get(0, -1) == " "
        assert c.get(5, 0) == " "
        assert c.get(0, 5) == " "

    def test_overwrite(self) -> None:
        c = Canvas(5, 5)
        c.set(1, 1, "A")
        c.set(1, 1, "B")
        assert c.get(1, 1) == "B"


class TestCanvasToString:
    def test_empty_canvas(self) -> None:
        c = Canvas(3, 2)
        result = c.to_string()
        assert result == "   \n   "

    def test_origin_bottom_left(self) -> None:
        c = Canvas(3, 3)
        c.set(0, 0, "B")  # bottom-left
        c.set(2, 2, "T")  # top-right
        lines = c.to_string().split("\n")
        assert lines[0][2] == "T"  # top row, rightmost
        assert lines[2][0] == "B"  # bottom row, leftmost

    def test_single_cell(self) -> None:
        c = Canvas(1, 1)
        c.set(0, 0, "#")
        assert c.to_string() == "#"
