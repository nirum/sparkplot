from dataclasses import dataclass


@dataclass(frozen=True)
class CharSet:
    horizontal: str
    vertical: str
    corner_bl: str  # bottom-left corner (axis origin)
    tick_y: str  # y-axis tick mark (right-pointing)
    tick_x: str  # x-axis tick mark (downward-pointing)
    curve_up_right: str  # going up to the right
    curve_down_right: str  # going down to the right
    curve_up_left: str  # going up to the left (unused in v1 but symmetric)
    curve_down_left: str  # going down to the left (unused in v1 but symmetric)
    block_full: str
    block_half: str  # half-block for finer histogram resolution
    diagonal_up: str  # for steep segments
    diagonal_down: str  # for steep segments


UNICODE = CharSet(
    horizontal="─",
    vertical="│",
    corner_bl="└",
    tick_y="┤",
    tick_x="┬",
    curve_up_right="╭",
    curve_down_right="╰",
    curve_up_left="╮",
    curve_down_left="╯",
    block_full="█",
    block_half="▄",
    diagonal_up="/",
    diagonal_down="\\",
)

ASCII = CharSet(
    horizontal="-",
    vertical="|",
    corner_bl="+",
    tick_y="+",
    tick_x="+",
    curve_up_right="/",
    curve_down_right="\\",
    curve_up_left="\\",
    curve_down_left="/",
    block_full="#",
    block_half="#",
    diagonal_up="/",
    diagonal_down="\\",
)
