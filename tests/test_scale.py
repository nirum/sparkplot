from sketchplot.scale import Scale


class TestScaleApply:
    def test_linear_mapping(self) -> None:
        s = Scale(0.0, 10.0, 0, 100)
        assert s.apply(0.0) == 0
        assert s.apply(10.0) == 100
        assert s.apply(5.0) == 50

    def test_edge_values(self) -> None:
        s = Scale(0.0, 100.0, 0, 50)
        assert s.apply(0.0) == 0
        assert s.apply(100.0) == 50
        assert s.apply(50.0) == 25

    def test_non_zero_pixel_min(self) -> None:
        s = Scale(0.0, 10.0, 10, 20)
        assert s.apply(0.0) == 10
        assert s.apply(10.0) == 20
        assert s.apply(5.0) == 15

    def test_zero_range(self) -> None:
        s = Scale(5.0, 5.0, 0, 20)
        assert s.apply(5.0) == 10  # midpoint

    def test_negative_data_range(self) -> None:
        s = Scale(-10.0, 10.0, 0, 20)
        assert s.apply(-10.0) == 0
        assert s.apply(0.0) == 10
        assert s.apply(10.0) == 20


class TestScaleTicks:
    def test_basic_ticks(self) -> None:
        s = Scale(0.0, 10.0, 0, 100)
        ticks = s.ticks(3)
        assert len(ticks) == 3
        assert ticks[0] == 0.0
        assert ticks[1] == 5.0
        assert ticks[2] == 10.0

    def test_single_tick(self) -> None:
        s = Scale(0.0, 10.0, 0, 100)
        ticks = s.ticks(1)
        assert len(ticks) == 1
        assert ticks[0] == 5.0  # midpoint

    def test_five_ticks(self) -> None:
        s = Scale(0.0, 100.0, 0, 50)
        ticks = s.ticks(5)
        assert len(ticks) == 5
        assert ticks == [0.0, 25.0, 50.0, 75.0, 100.0]

    def test_zero_range_ticks(self) -> None:
        s = Scale(5.0, 5.0, 0, 20)
        ticks = s.ticks(3)
        assert all(t == 5.0 for t in ticks)
