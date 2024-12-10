from typing import List, Tuple, Deque
from dataclasses import dataclass
from collections import deque

EXAMPLE=\
"""\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

@dataclass
class TopoMap:
    data: List[List[int]]
    rows: int
    cols: int

Position = Tuple[int, int]

def parse_content(content: str) -> TopoMap:
    topo_map = TopoMap([], 0, 0)
    for line in content.splitlines():
        topo_map.data.append(list(map(int, [c for c in line])))

    topo_map.rows = len(topo_map.data)
    topo_map.cols = len(topo_map.data[0])
    return topo_map

def valid_neighbors(topo_map: TopoMap, row: int, col: int) -> List[Tuple[int, Position]]:
    positions = [
        (row-1, col),
        (row+1, col),
        (row, col-1),
        (row, col+1),
    ]
    valid_positions = [(r, c) for r, c in positions if (0 <= r < topo_map.rows and 0 <= c < topo_map.cols)]
    return [(topo_map.data[r][c], (r, c)) for r, c in valid_positions]

def solve(topo_map: TopoMap) -> int:
    starts: List[Tuple[int, Position]] = []
    for r in range(topo_map.rows):
        for c in range(topo_map.cols):
            if topo_map.data[r][c] == 0:
                starts.append((0, (r, c)))
    # print(f"{starts=}")

    score = 0
    for start in starts:

        todo: Deque[Tuple[int, Position]] = deque([start])
        nines_positions = set()
        while todo:
            new_todo = []
            for (value, (r, c)) in todo:
                neighbors = valid_neighbors(topo_map, r, c)
                for (vn, (rn, cn)) in neighbors:
                    if value == 8 and vn == 9:
                        nines_positions.add((rn, cn))
                    elif vn == (value + 1):
                        new_todo.append((vn, (rn, cn)))
                    # else not reachable
            todo = deque(new_todo)
        # print(f"reached {len(nines_positions)=} 9 from {start=}")
        score += len(nines_positions)

    return score



def solve2(topo_map: TopoMap) -> int:
    starts: List[Tuple[int, Position]] = []
    for r in range(topo_map.rows):
        for c in range(topo_map.cols):
            if topo_map.data[r][c] == 0:
                starts.append((0, (r, c)))
    print(f"{starts=}")

    ratings = 0
    for start in starts:

        todo: Deque[Tuple[int, Position]] = deque([start])
        while todo:
            new_todo = []
            for (value, (r, c)) in todo:
                neighbors = valid_neighbors(topo_map, r, c)
                for (vn, (rn, cn)) in neighbors:
                    if value == 8 and vn == 9:
                        ratings += 1
                    elif vn == (value + 1):
                        new_todo.append((vn, (rn, cn)))
                    # else not reachable
            todo = deque(new_todo)

    return ratings


if __name__ == "__main__":
    print(f"{parse_content(EXAMPLE)=}")
    print(f"{solve(parse_content(EXAMPLE))=}")
    print(f"{solve2(parse_content(EXAMPLE))=}")
    with open("./input.txt") as input_file:
        content = input_file.read()
        print(f"{solve(parse_content(content))=}")
        print(f"{solve2(parse_content(content))=}")
