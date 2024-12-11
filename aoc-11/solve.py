from typing import Dict, List, Deque, Tuple, Optional
from collections import defaultdict, deque

from tqdm import tqdm

EXAMPLE = """\
125 17
"""

Stones = List[int]


def load_content(content: str) -> Stones:
    return list(map(int, content.rstrip().split(" ")))


def solve(stones: Stones, n_blink: int) -> Tuple[int, Stones]:
    stones_copy = stones.copy()
    for blink in range(n_blink):
        new_stones = []
        for stone in stones_copy:
            if stone == 0:
                new_stones.append(1)
            else:
                stone_str = str(stone)
                stone_digits = len(stone_str)
                if stone_digits % 2 == 0:
                    first_half = stone_str[: stone_digits // 2]
                    second_half = stone_str[stone_digits // 2 :]
                    new_stones.append(int(first_half))
                    new_stones.append(int(second_half))
                else:
                    new_stones.append(stone * 2024)
        stones_copy = new_stones

    return len(stones_copy), stones_copy


def solve_memo(stones: Stones, n_blink: int) -> int:
    memo: Dict[Tuple[int, int], int] = defaultdict(lambda: 0)
    work: Deque[Tuple[Optional[int], int, int]] = deque()
    for stone in stones:
        work.append((None, stone, n_blink))

    while work:
        # print(f"{work=}")
        prev, current, blinks = work[-1]

        if blinks == 0:
            memo[(current, 0)] = 1
            if prev is not None:
                memo[(prev, blinks + 1)] += memo[(current, blinks)]
            work.pop()
            continue

        if (current, blinks) in memo:
            if prev is not None:
                memo[(prev, blinks + 1)] += memo[(current, blinks)]
            work.pop()
            continue

        _, new_stones = solve([current], 1)
        for stone in new_stones:
            work.append((current, stone, blinks - 1))
    total = 0
    for stone in stones:
        total += memo[(stone, n_blink)]
    return total


if __name__ == "__main__":
    print(f"{load_content(EXAMPLE)=}")
    for i in range(6):
        print(f"{solve(load_content(EXAMPLE), i)[0]=}")
        print(f"{solve_memo(load_content(EXAMPLE), i)=}")

    print(f"{solve(load_content(EXAMPLE), 25)[0]=}")
    # print(f"{solve_memo(load_content(EXAMPLE), 25)=}")
    with open("./input.txt") as input_file:
        content = input_file.read()
        print(f"{solve(load_content(content), 25)[0]=}")
        # print(f"{solve_memo(load_content(content), 25)=}")
        print(f"{solve_memo(load_content(content), 75)=}")
