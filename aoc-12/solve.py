from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Deque, Dict, List, Optional, Union, Tuple

EXAMPLE_4x4 = """\
AAAA
BBCD
BBCC
EEEC
"""

EXAMPLE_5x5 = """\
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""

EXAMPLE_10x10 = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""


@dataclass
class Puzzle:
    data: List[List[str]]
    rows: int
    cols: int


@dataclass
class PuzzleClusters:
    data: List[List[int]]
    rows: int
    cols: int


def neighbors(
    puzzle: Union[PuzzleClusters, Puzzle],
    row: int,
    col: int,
    down_right: bool = True,
) -> Union[List[Tuple[int, int, int]], List[Tuple[int, int, str]]]:
    n = []

    if down_right:
        directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    else:
        directions = [(1, 0), (0, 1), (0, -1), (-1, 0)]

    for dr, dc in directions:
        if 0 <= row + dr < puzzle.rows and 0 <= col + dc < puzzle.cols:
            n.append((row + dr, col + dc, puzzle.data[row + dr][col + dc]))
    return n


def fancy_str(
    puzzle: Union[PuzzleClusters, Puzzle],
) -> str:
    cluster = isinstance(puzzle, PuzzleClusters)
    lines = []
    for line in puzzle.data:
        if cluster:
            lines.append(",".join([f"{v:02d}" for v in line]))
        else:
            lines.append("".join([str(v) for v in line]))

    return "\n".join([line for line in lines])


def load_puzzle(content: str) -> Puzzle:
    p = Puzzle([], 0, 0)
    for line in content.splitlines():
        p.data.append([c for c in line])
        p.rows += 1
        p.cols = len(line)
    return p


def clusterize(puzzle: Puzzle) -> PuzzleClusters:
    clusters = PuzzleClusters([], puzzle.rows, puzzle.cols)
    for _ in range(puzzle.rows):
        clusters.data.append([-1] * puzzle.cols)

    cluster_number = 0
    work: Deque[Tuple[str, int, int, str, int, int]] = deque(
        [(puzzle.data[0][0], 0, 0, puzzle.data[0][0], 0, 0)]
    )
    current_cluster_plant = puzzle.data[0][0]
    while work:
        cluster_plant, r, c, prev_plant, prev_r, prev_c = work.popleft()

        if cluster_plant == prev_plant and (abs(prev_r - r) + abs(prev_c - c)) > 1:
            # new cluster, same plant
            cluster_number += 1
        elif cluster_plant != prev_plant:
            # new cluster, different plant
            current_cluster_plant = cluster_plant
            cluster_number += 1

        if clusters.data[r][c] < 0:
            clusters.data[r][c] = cluster_number

        for neighbor_p, neighbor_c in zip(
            neighbors(puzzle, r, c), neighbors(clusters, r, c)
        ):
            _rp, _cp, vp = neighbor_p
            rc, cc, vc = neighbor_c

            if vp == current_cluster_plant and int(vc) < 0:
                work.appendleft((str(vp), rc, cc, str(vp), r, c))
            elif vp != current_cluster_plant and int(vc) < 0:
                work.append((str(vp), rc, cc, current_cluster_plant, r, c))

    return clusters


def solve(puzzle: Puzzle) -> int:
    clusters = clusterize(puzzle)
    areas: Dict[Tuple[int, str], int] = defaultdict(lambda: 0)
    perimeters: Dict[Tuple[int, str], int] = defaultdict(lambda: 0)
    for r in range(puzzle.rows):
        for c in range(puzzle.cols):
            areas[(clusters.data[r][c], puzzle.data[r][c])] += 1
            perimeter = 4
            for neighbor in neighbors(clusters, r, c):
                _rc, _cc, nc = neighbor
                if nc == clusters.data[r][c]:
                    perimeter -= 1
            perimeters[(clusters.data[r][c], puzzle.data[r][c])] += perimeter
    total = 0
    for (cluster, plant), area in areas.items():
        perimeter = perimeters[(cluster, plant)]
        print(f"{cluster=} {plant=} {area=} x {perimeter=} = {perimeter * area}")
        total += perimeter * area
    return total


if __name__ == "__main__":
    # print(f"{fancy_str(load_puzzle(EXAMPLE))}")
    # print(f"{fancy_str(clusterize(load_puzzle(EXAMPLE)))}")
    print(f"{solve(load_puzzle(EXAMPLE_4x4))=}")
    print(f"{fancy_str(clusterize(load_puzzle(EXAMPLE_5x5)))}")
    print(f"{solve(load_puzzle(EXAMPLE_5x5))=}")
    print(f"{solve(load_puzzle(EXAMPLE_10x10))=}")
    with open("./input.txt") as input_file:
        content = input_file.read()
        print(f"{solve(load_puzzle(content))}")
