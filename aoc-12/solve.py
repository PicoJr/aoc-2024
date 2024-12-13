from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Deque, Dict, List, Optional, Set, Union, Tuple

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

EXAMPLE_6x6 = """\
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
"""

EXAMPLE_E = """\
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
"""

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

Direction = Tuple[int, int]
RowCol = Tuple[int, int]
Sides = Tuple[bool, bool, bool, bool]


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


@dataclass
class PuzzleFences:
    data: List[List[int]]
    rows: int
    cols: int


def neighbors(
    puzzle: Union[PuzzleClusters, Puzzle, PuzzleFences],
    row: int,
    col: int,
) -> Union[List[Tuple[int, int, int]], List[Tuple[int, int, str]]]:
    n = []

    directions = [LEFT, UP, RIGHT, DOWN]

    for dr, dc in directions:
        if 0 <= row + dr < puzzle.rows and 0 <= col + dc < puzzle.cols:
            n.append((row + dr, col + dc, puzzle.data[row + dr][col + dc]))
    return n


def neighbors2(
    puzzle: Union[PuzzleClusters, Puzzle, PuzzleFences],
    row: int,
    col: int,
) -> Union[
    List[Optional[Tuple[int, int, int]]],
    List[Optional[Tuple[int, int, str]]],
]:
    n = []

    directions = [LEFT, UP, RIGHT, DOWN]

    for dr, dc in directions:
        if 0 <= row + dr < puzzle.rows and 0 <= col + dc < puzzle.cols:
            n.append((row + dr, col + dc, puzzle.data[row + dr][col + dc]))
        else:
            n.append(None)
    return n


def fancy_str(
    puzzle: Union[PuzzleClusters, Puzzle, PuzzleFences],
) -> str:
    cluster = isinstance(puzzle, PuzzleClusters) or isinstance(puzzle, PuzzleFences)
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


def solve2(puzzle: Puzzle) -> int:
    clusters = clusterize(puzzle)
    areas: Dict[Tuple[int, str], int] = defaultdict(lambda: 0)

    for r in range(puzzle.rows):
        for c in range(puzzle.cols):
            areas[(clusters.data[r][c], puzzle.data[r][c])] += 1

    total = 0
    for (cluster, plant), area in areas.items():
        fences: PuzzleFences = PuzzleFences(
            data=[], rows=puzzle.rows * 2 + 1, cols=puzzle.cols * 2 + 1
        )
        for r in range(fences.rows):
            fences.data.append([-1] * fences.cols)

        for r in range(puzzle.rows):
            for c in range(puzzle.cols):
                if clusters.data[r][c] != cluster:
                    continue
                sides = [False, False, False, False]
                for i_side, neighbor in enumerate(neighbors2(clusters, r, c)):
                    if neighbor is None:
                        sides[i_side] = True
                    else:
                        _rc, _cc, nc = neighbor
                        if nc != clusters.data[r][c]:
                            sides[i_side] = True
                [left, up, right, down] = sides
                cluster_id = clusters.data[r][c]
                if left:
                    fences.data[2 * r][2 * c] = cluster_id
                    fences.data[2 * r + 1][2 * c] = cluster_id
                    fences.data[2 * r + 2][2 * c] = cluster_id
                if up:
                    fences.data[2 * r][2 * c] = cluster_id
                    fences.data[2 * r][2 * c + 1] = cluster_id
                    fences.data[2 * r][2 * c + 2] = cluster_id
                if right:
                    fences.data[2 * r][2 * c + 2] = cluster_id
                    fences.data[2 * r + 1][2 * c + 2] = cluster_id
                    fences.data[2 * r + 2][2 * c + 2] = cluster_id
                if down:
                    fences.data[2 * r + 2][2 * c] = cluster_id
                    fences.data[2 * r + 2][2 * c + 1] = cluster_id
                    fences.data[2 * r + 2][2 * c + 2] = cluster_id

        corners = 0
        antimobius: Dict[RowCol, int] = defaultdict(lambda: 0)
        # print(f"{cluster=} {plant=} {{")
        for r in range(puzzle.rows):
            for c in range(puzzle.cols):
                # top left corner
                r2, c2 = 2 * r, 2 * c
                check_top_left_corner = [(r2, c2), (r2, c2 + 1), (r2 + 1, c2)]
                check_top_right_corner = [(r2, c2 + 2), (r2, c2 + 1), (r2 + 1, c2 + 2)]
                check_bottom_right_corner = [
                    (r2 + 2, c2 + 2),
                    (r2 + 1, c2 + 2),
                    (r2 + 2, c2 + 1),
                ]
                check_bottom_left_corner = [
                    (r2 + 2, c2),
                    (r2 + 2, c2 + 1),
                    (r2 + 1, c2),
                ]
                new_corners = 0
                corners_checks = [
                    check_top_left_corner,
                    check_top_right_corner,
                    check_bottom_right_corner,
                    check_bottom_left_corner,
                ]
                corner_names = ["top_left", "top_right", "bottom_right", "bottom_left"]
                for checks, corner_name in zip(corners_checks, corner_names):
                    if all(
                        [
                            fences.data[r_corner][c_corner] == cluster
                            for (r_corner, c_corner) in checks
                        ]
                    ):
                        antimobius[checks[0]] += 1
                        if antimobius[checks[0]] > 2:
                            print(f"found a mobius...at {checks[0]}")
                        else:
                            new_corners += 1
                        # print(f"\t found corner {corner_name} at {r=} {c=}")
                corners += new_corners

        # print(fancy_str(clusters))
        # print(fancy_str(fences))
        # print(f"=> {corners=} }}")
        total += corners * area

    return total


if __name__ == "__main__":
    # print(f"{fancy_str(load_puzzle(EXAMPLE_5x5))}")
    # print(f"{solve(load_puzzle(EXAMPLE_4x4))=}")
    # print(f"{fancy_str(clusterize(load_puzzle(EXAMPLE_5x5)))}")
    # print(f"{solve(load_puzzle(EXAMPLE_5x5))=}")
    # print(f"{solve(load_puzzle(EXAMPLE_10x10))=}")

    print(f"{solve2(load_puzzle(EXAMPLE_4x4))=} vs 80")
    print(f"{solve2(load_puzzle(EXAMPLE_5x5))=} vs 436")
    print(f"{solve2(load_puzzle(EXAMPLE_6x6))=} vs 368")
    print(f"{solve2(load_puzzle(EXAMPLE_E))=} vs 236")
    print(f"{solve2(load_puzzle(EXAMPLE_10x10))=} vs 1206")
    with open("./input.txt") as input_file:
        content = input_file.read()
        print(f"{solve(load_puzzle(content))} vs 1471452")
        print(f"{solve2(load_puzzle(content))} vs 863366")
