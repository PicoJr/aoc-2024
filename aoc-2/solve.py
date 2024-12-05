from typing import List

def pairwise(iterable):
    # pairwise('ABCDEFG') → AB BC CD DE EF FG

    iterator = iter(iterable)
    a = next(iterator, None)

    for b in iterator:
        yield a, b
        a = b

EXAMPLE=\
"""\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""


def safe(data: List[int]) -> bool:
    increasing = False
    decreasing = False
    for a, b in pairwise(data):
        if abs(a - b) < 1:
            return False
        if abs(a - b) > 3:
            return False
        if a < b and decreasing:
            return False
        if a > b and increasing:
            return False
        if a < b:
            increasing = True
        if a > b:
            decreasing = True
    return True

def safe2(data: List[int]) -> bool:

    if safe(data):
        return True

    for i_dampened, _ in enumerate(data):
        dampened_data = [d for (i, d) in enumerate(data) if i != i_dampened]
        if safe(dampened_data):
            return True
    return False

def load_content(content: str) -> List[List[int]]:
    return [list(map(int, line.split(" "))) for line in content.splitlines()]

def solve_content(content: str) -> int:
    data = load_content(content)
    return len([ v for v in data if safe(v)])

def solve_content2(content: str) -> int:
    data = load_content(content)
    return len([ v for v in data if safe2(v)])

def main():
    print(f"{solve_content(EXAMPLE)=}")
    print(f"{solve_content2(EXAMPLE)=}")
    with open("./input.txt") as input:
        content = input.read()
        print(f"{solve_content(content)=}")
        print(f"{solve_content2(content)=}")



if __name__ == "__main__":
    main()
