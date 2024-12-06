from typing import Set, Tuple, List
import numpy.typing as npt
import numpy as np
import tqdm


EXAMPLE=\
"""\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

Up = (-1, 0)
Down = (1, 0)
Left = (0, -1)
Right = (0, 1)


def turn_right(direction: Tuple[int, int]) -> Tuple[int, int]:
    if direction == Up:
        return Right
    if direction == Right:
        return Down
    if direction == Down:
        return Left
    if direction == Left:
        return Up
    else:
        assert False


PuzzleMap = npt.NDArray[np.character]


def load_content(content: str) -> PuzzleMap:
    lines = content.splitlines()
    rows = len(lines)
    cols = len(lines[0])
    return np.array([c for line in lines for c in line]).reshape((rows,cols))


def solve(m: PuzzleMap) -> int:
    patrol = set()
    r, c = np.where(m == '^')
    r, c = r[0], c[0]
    rows, cols = m.shape
    direction = Up
    while 0 <= r < rows and 0 <= c < cols:
        patrol.add((r, c))
        while 0 <= r + direction[0] < rows and 0 <= c + direction[1] < cols and m[r + direction[0]][c + direction[1]] == '#':
            direction = turn_right(direction)
        r += direction[0]
        c += direction[1]

    return len(patrol)


def is_looping(obstruction: Tuple[int, int], m: PuzzleMap) -> bool:
    m_copy = m.copy()
    m_copy[obstruction[0]][obstruction[1]] = '#'

    patrol: Set[Tuple[int, int, Tuple[int, int]]] = set()
    r, c = np.where(m_copy == '^')
    r, c = r[0], c[0]
    rows, cols = m_copy.shape
    direction = Up
    while 0 <= r < rows and 0 <= c < cols:
        if (r, c, direction) in patrol:
            return True
        patrol.add((r, c, direction))
        while 0 <= r + direction[0] < rows and 0 <= c + direction[1] < cols and m_copy[r + direction[0]][c + direction[1]] == '#':
            direction = turn_right(direction)
        r += direction[0]
        c += direction[1]

    return False


def solve2(m: PuzzleMap) -> int:
    patrol: List[Tuple[int, int]] = []
    r, c = np.where(m == '^')
    r, c = r[0], c[0]
    r_start, c_start = r, c
    rows, cols = m.shape
    direction = Up
    while 0 <= r < rows and 0 <= c < cols:
        patrol.append((r, c))
        while 0 <= r + direction[0] < rows and 0 <= c + direction[1] < cols and m[r + direction[0]][c + direction[1]] == '#':
            direction = turn_right(direction)
        r += direction[0]
        c += direction[1]

    obstructions: Set[Tuple[int, int]] = set()
    for obstruction in tqdm.tqdm(patrol):
        if obstruction == (r_start, c_start):
            continue
        if obstruction in obstructions:
            continue
        if is_looping(obstruction, m):
            obstructions.add(obstruction)

    return len(obstructions)


if __name__ == "__main__":
    puzzle = load_content(EXAMPLE)
    print(f"{solve(puzzle)=}")
    print(f"{solve2(puzzle)=}")
    with open("./input.txt") as input_file:
        big_puzzle = load_content(input_file.read())
        print(f"{solve(big_puzzle)=}")
        print(f"{solve2(big_puzzle)=}")
