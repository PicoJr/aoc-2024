from enum import Enum, auto
from typing import Generator

import numpy as np
import numpy.typing as npt


class Direction(Enum):
    HorizontalForward = auto()
    VerticalForward = auto()
    DiagonalForward = auto()
    

EXAMPLE=\
"""\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""


def load_content(content: str) -> npt.NDArray[np.character]:
    lines = content.splitlines()
    rows = len(lines)
    cols = len(lines[0])
    chars = [c for line in lines for c in line]

    return np.array(chars).reshape((rows, cols))


def direction_iterator(content: npt.NDArray[np.character], direction: Direction) -> Generator[str, None, None]:
    rows, cols = content.shape
    if direction == Direction.HorizontalForward:
        for row in range(rows):
            for col in range(cols):
                yield str(content[row][col])
            yield '#'  # separator 
    if direction == Direction.VerticalForward:
        for col in range(cols):
            for row in range(rows):
                yield str(content[row][col])
            yield '#'  # separator 
    if direction == Direction.DiagonalForward:
        # start from first row left to right, top to bottom
        for starting_col in range(cols):
            for row in range(rows):
                if starting_col + row < cols and row < rows: 
                    yield str(content[row][starting_col + row])
            yield '#'  # separator 
        
        # start from first row right to left, top to bottom
        for starting_col in reversed(range(cols)):
            for row in range(rows):
                if (cols - 1 - starting_col - row) >= 0 and row < rows: 
                    yield str(content[row][cols - 1 - starting_col - row])
            yield '#'  # separator 

        # start from second row, left to right, top to bottom
        for starting_row in range(1, rows):
            for col in range(cols):
                if starting_row + col < rows and col < cols: 
                    yield str(content[starting_row + col][col])
            yield '#'  # separator 
        
        # start from second row, right to left, top to bottom
        for starting_row in range(1, rows):
            for col in reversed(range(cols)):
                if starting_row + col < rows and (cols - col) >= 0: 
                    yield str(content[starting_row + col][cols - 1 - col])
            yield '#'  # separator 


def solve_content(content: str) -> int:
    chars = load_content(content)
    total = 0
    for direction in [Direction.HorizontalForward, Direction.VerticalForward, Direction.DiagonalForward]:
        direction_text = str("".join(direction_iterator(chars, direction)))
        xmas_count = direction_text.count("XMAS")
        samx_count = direction_text.count("SAMX")
        # print(f"{xmas_count=} {samx_count=}")
        total += xmas_count + samx_count
    return total


def solve_content2(content: str) -> int:
    chars = load_content(content)
    total = 0
    rows, cols = chars.shape

    patterns = [
        np.array([
            ["M", ".", "S"],
            [".", "A", "."],
            ["M", ".", "S"],
        ]),
        np.array([
            ["S", ".", "S"],
            [".", "A", "."],
            ["M", ".", "M"],
        ]),
        np.array([
            ["S", ".", "M"],
            [".", "A", "."],
            ["S", ".", "M"],
        ]),
        np.array([
            ["M", ".", "M"],
            [".", "A", "."],
            ["S", ".", "S"],
        ]),
    ]
    if False:
        patterns.extend([
            np.array([
                [".", "M", "."],
                ["M", "A", "S"],
                [".", "S", "."],
            ]),
            np.array([
                [".", "S", "."],
                ["M", "A", "S"],
                [".", "M", "."],
            ]),
            np.array([
                [".", "S", "."],
                ["S", "A", "M"],
                [".", "M", "."],
            ]),
            np.array([
                [".", "M", "."],
                ["S", "A", "M"],
                [".", "S", "."],
            ]),
        ])
    total = 0
    for pattern in patterns:
        for row in range(1, rows-1):
            for col in range(1, cols-1):
                ok = True
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if pattern[1 + dr][1 + dc] == ".":
                            continue
                        if pattern[1 + dr][1 + dc] != chars[row + dr][col + dc]:
                            ok = False
                            break
                if ok:
                    total += 1
    return total


if __name__ == "__main__":
    print(f"{solve_content(EXAMPLE)=}")
    print(f"{solve_content2(EXAMPLE)=}")
    with open("./input.txt") as input_file:
        txt = input_file.read()
        print(f"{solve_content(txt)=}")
        print(f"{solve_content2(txt)=}")
