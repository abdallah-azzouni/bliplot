from typing import Sequence
import numpy as np
import shutil


def plot(
    lst: Sequence[int | float],
    width: int | None = None,
    height: int | None = None,
    color: str | None = None,
):
    """_summary_
    Renders a list of numbers as a text-based graph in the terminal.


    Args:
        lst (Sequence[int | float]): The Y values to be plotted. The X values are inferred from the index of the list.
        width (int, optional): The width of the graph in characters. If None, it will use the terminal width.
        height (int, optional): The height of the graph in characters. If None, it will use the terminal height.
        color (str, optional):  The color of the graph. Can be one of "RESET", "GREEN", "CYAN", "YELLOW", "RED", "MAGENTA", "BLUE", "WHITE", or "BLACK". If None, it will default to white.

    Returns:
        _type_: The graph as a string, ready to be printed to the terminal.

    Note:
        Non-finite values (NaN, +Inf, -Inf) in lst are treated as 0.

    """

    term = shutil.get_terminal_size()
    w = width if width is not None else term.columns - 1
    h = height if height is not None else term.lines - 1
    COLORS = {
        "RESET": "\033[0m",
        "GREEN": "\033[32m",
        "CYAN": "\033[36m",
        "YELLOW": "\033[33m",
        "RED": "\033[31m",
        "MAGENTA": "\033[35m",
        "BLUE": "\033[34m",
        "WHITE": "\033[37m",
        "BLACK": "\033[30m",
    }

    color = (
        COLORS.get(color.upper(), COLORS["WHITE"])
        if color is not None
        else COLORS["WHITE"]
    )

    BLOCKS = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
    IBLOCKS = ["▔", "▀", "█"]
    middle_point = "·"

    if len(lst) == 0:
        return ""

    x_scale = np.linspace(0, len(lst) - 1, w)
    x_new = np.interp(x_scale, np.arange(len(lst)), lst)
    x_new = np.nan_to_num(x_new, nan=0.0, posinf=0.0, neginf=0.0)

    has_positive = bool(np.any(x_new > 0))
    has_negative = bool(np.any(x_new < 0))

    if has_negative and has_positive:
        midpoint = (h - 1) // 2
        scale_range = midpoint
    elif has_positive:
        midpoint = h - 1
        scale_range = midpoint
    else:
        midpoint = 0
        scale_range = h - 1

    grid = np.empty((h, w), dtype=object)
    grid.fill(" ")

    max_abs = np.max(np.abs(x_new))
    normalized = (
        midpoint + (x_new / max_abs) * scale_range
        if max_abs != 0
        else np.full_like(x_new, midpoint)
    )

    grid[midpoint, :] = middle_point

    for col in range(w):
        val = normalized[col]
        remainder = val % 1
        if val > midpoint:
            solid_height = int(val - midpoint)
            solid_row = midpoint - solid_height
            grid[solid_row:midpoint, col] = BLOCKS[-1]
            if solid_row > 0:
                grid[solid_row - 1, col] = BLOCKS[
                    int(remainder * len(BLOCKS)) % len(BLOCKS)
                ]
        elif val < midpoint:
            solid_height = int(midpoint - val)
            solid_row = midpoint + solid_height
            grid[midpoint:solid_row, col] = IBLOCKS[-1]
            if solid_row < h:
                grid[solid_row, col] = IBLOCKS[
                    int((1 - remainder) * len(IBLOCKS)) % len(IBLOCKS)
                ]

    return f"{color}{chr(10).join(''.join(row) for row in grid)}{COLORS['RESET']}"
