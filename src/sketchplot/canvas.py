class Canvas:
    """2D grid of characters. Origin at bottom-left, y-axis pointing up."""

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self._grid: list[list[str]] = [[" "] * width for _ in range(height)]

    def set(self, x: int, y: int, char: str) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            self._grid[y][x] = char

    def get(self, x: int, y: int) -> str:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self._grid[y][x]
        return " "

    def to_string(self) -> str:
        # Flip rows so y=0 (bottom) is last in output
        lines = ["".join(row) for row in reversed(self._grid)]
        return "\n".join(lines)
