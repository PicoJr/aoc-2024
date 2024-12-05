from pathlib import Path

def solve_content_1(content: str):
    lines = content.splitlines()
    values = [ tuple(map(int, line.split("   "))) for line in lines]
    left = [v[0] for v in values]
    right = [v[1] for v in values]
    print(f"{len(left)=} vs {len(right)=}")
    left_sorted = sorted(left)
    right_sorted = sorted(right)
    distance = 0
    for l, r in zip(left_sorted, right_sorted):
        distance += abs(l -r)

    print(distance)


def solve_content_2(content: str):
    lines = content.splitlines()
    values = [ tuple(map(int, line.split("   "))) for line in lines]
    left = [v[0] for v in values]
    right = [v[1] for v in values]
    print(f"{len(left)=} vs {len(right)=}")
    left_sorted = sorted(left)
    right_sorted = sorted(right)
    similarity = 0
    for l in left_sorted:
        for r in right_sorted:
            if r == l:
                similarity += l
            if r > l:
                continue
    print(similarity)


def solve_path_1(path: Path):
    with open(path) as input_file:
        data_txt = input_file.read()
        solve_content_1(data_txt)

def solve_path_2(path: Path):
    with open(path) as input_file:
        data_txt = input_file.read()
        solve_content_2(data_txt)

EXAMPLE=\
"""\
3   4
4   3
2   5
1   3
3   9
3   3
"""


def main():
    solve_content_1(EXAMPLE)
    solve_path_1(Path("./data/input.txt"))
    
    solve_content_2(EXAMPLE)
    solve_path_2(Path("./data/input.txt"))
    


if __name__ == "__main__":
    main()
