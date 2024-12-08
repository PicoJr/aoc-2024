from collections import defaultdict
from typing import Dict, List, Tuple
from itertools import combinations

import numpy as np


EXAMPLE = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""


Position = Tuple[int, int]
Puzzle = Dict[str, List[Position]]


# def is_letter(c: str) -> bool:
#    return (ord('a') <= ord(c) <= ord('z')) or (ord('A') <= ord(c) <= ord('Z'))


def load_puzzle(content: str) -> Tuple[Puzzle, int, int]:
    lines = content.splitlines()
    rows = len(lines)
    cols = len(lines[0])
    map_array = np.array([c for line in lines for c in line]).reshape((rows, cols))

    all = np.unique(map_array)
    letters = [c for c in all if c != "."]
    puzzle: Puzzle = defaultdict(list)
    for letter in letters:
        letter_rows, letter_cols = np.where(map_array == letter)
        for r, c in zip(letter_rows, letter_cols):
            puzzle[letter].append((int(r), int(c)))

    return puzzle, rows, cols


def solve_puzzle(puzzle: Puzzle, rows: int, cols: int) -> int:

    antinodes_positions = set()

    def antinodes(p1: Position, p2: Position) -> List[Position]:
        dr = p2[0] - p1[0]
        dc = p2[1] - p1[1]
        return [(p1[0] - dr, p1[1] - dc), (p2[0] + dr, p2[1] + dc)]

    for _letter, positions in puzzle.items():
        for p1, p2 in combinations(positions, 2):
            for antinode in antinodes(p1, p2):
                antinodes_positions.add(antinode)

    inside_map: List[Position] = [
        p for p in antinodes_positions if ((0 <= p[0] < rows) and (0 <= p[1] < cols))
    ]
    return len(inside_map)


def solve_puzzle2(puzzle: Puzzle, rows: int, cols: int) -> int:

    antinodes_positions = set()

    def inside(p: Position) -> bool:
        return (0 <= p[0] < rows) and (0 <= p[1] < cols)

    def antinodes2(p1: Position, p2: Position) -> List[Position]:
        dr = p2[0] - p1[0]
        dc = p2[1] - p1[1]
        i = 0
        positions = []
        while inside((antinode_position := (p1[0] - i * dr, p1[1] - i * dc))):
            positions.append(antinode_position)
            i += 1
        i = 0
        while inside((antinode_position := (p2[0] + i * dr, p2[1] + i * dc))):
            positions.append(antinode_position)
            i += 1
        return positions

    for _letter, positions in puzzle.items():
        for p1, p2 in combinations(positions, 2):
            for antinode in antinodes2(p1, p2):
                antinodes_positions.add(antinode)

    inside_map: List[Position] = [p for p in antinodes_positions if inside(p)]

    return len(inside_map)


def solve(content: str) -> int:
    return solve_puzzle(*load_puzzle(content))


def solve2(content: str) -> int:
    return solve_puzzle2(*load_puzzle(content))


if __name__ == "__main__":
    print(f"{solve(EXAMPLE)=}")
    print(f"{solve2(EXAMPLE)=}")
    with open("./input.txt") as input_file:
        content = input_file.read()
        print(f"{solve(content)=}")
        print(f"{solve2(content)=}")
