from typing import Tuple, List
from itertools import pairwise, product

import tqdm


EXAMPLE = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

Puzzle = List[Tuple[int, List[int]]]


def load_puzzle(content: str) -> Puzzle:
    puzzle: Puzzle = []
    for line in content.splitlines():
        target, values_str = line.split(": ")
        values = list(map(int, values_str.split(" ")))
        puzzle.append((int(target), values))
    return puzzle


def compute(left: int, right: int, operator: str) -> int:
    if operator == "+":
        return left + right
    elif operator == "*":
        return left * right
    elif operator == "|":
        return int(str(left) + str(right))
    else:
        assert False


def solve_puzzle(puzzle: Puzzle, operators: List[str]) -> int:
    targets_ok = []
    for target, values in tqdm.tqdm(puzzle):
        all_operations = product(operators, repeat=(len(values) - 1))
        for operations in all_operations:
            result = None
            for op, (left, right) in zip(operations, pairwise(values)):
                if result is None:
                    result = compute(left, right, op)
                else:
                    result = compute(result, right, op)
            if result == target:
                # print(f"{values=} {operations=} -> {target=}")
                targets_ok.append(target)
                break

    return sum(targets_ok)


def solve(content: str) -> int:
    return solve_puzzle(load_puzzle(content), operators=["+", "*"])


def solve2(content: str) -> int:
    return solve_puzzle(load_puzzle(content), operators=["+", "*", "|"])


if __name__ == "__main__":
    print(f"{solve(EXAMPLE)=}")
    print(f"{solve2(EXAMPLE)=}")
    with open("./input.txt") as input_file:
        puzzle = load_puzzle(input_file.read())
        print(f"{solve_puzzle(puzzle, operators = ['+', '*'])=}")
        print(f"{solve_puzzle(puzzle, operators = ['+', '*', '|'])=}")
