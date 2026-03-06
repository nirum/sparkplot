class Scale:
    """Maps a data range [lo, hi] to an integer pixel range [0, size-1]."""

    def __init__(
        self, data_min: float, data_max: float, pixel_min: int, pixel_max: int
    ) -> None:
        self.data_min = data_min
        self.data_max = data_max
        self.pixel_min = pixel_min
        self.pixel_max = pixel_max

    def apply(self, value: float) -> int:
        if self.data_max == self.data_min:
            return (self.pixel_min + self.pixel_max) // 2
        ratio = (value - self.data_min) / (self.data_max - self.data_min)
        return self.pixel_min + round(ratio * (self.pixel_max - self.pixel_min))

    def ticks(self, n: int) -> list[float]:
        if n <= 1:
            return [(self.data_min + self.data_max) / 2]
        step = (self.data_max - self.data_min) / (n - 1)
        return [self.data_min + i * step for i in range(n)]
