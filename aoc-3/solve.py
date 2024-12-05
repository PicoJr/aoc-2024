
EXAMPLE=r"xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
EXAMPLE2=r"xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

from enum import Enum, auto
import re

class Op(Enum):
    DO = auto()
    DONT = auto()
    MULT = auto()



def solve_content(content: str) -> int:
    mult_re = re.compile(r"mul\((\d\d?\d?),(\d\d?\d?)\)")
    mults = mult_re.findall(content)
    return sum([int(x) * int(y) for x, y in mults])


def solve_content2(content: str) -> int:
    mult_re = re.compile(r"mul\((\d\d?\d?),(\d\d?\d?)\)")
    do_re = re.compile(r"do\(\)")
    dont_re = re.compile(r"don't\(\)")

    doing = True
    index: int = 0
    total: int = 0
    while True:
        next_mult_match = mult_re.search(content[index:])
        next_do_match = do_re.search(content[index:])
        next_dont_match = dont_re.search(content[index:])
        ops = []
        if next_mult_match is not None:
            ops.append((Op.MULT, next_mult_match))
        if next_do_match is not None:
            ops.append((Op.DO, next_do_match))
        if next_dont_match is not None:
            ops.append((Op.DONT, next_dont_match))

        if not ops:
            break

        next_op = min(ops, key=lambda x: x[1].span(0)[0])
        next_op_type, _ = next_op
        if next_op_type == Op.DO:
            assert next_do_match is not None
            doing = True
            index += next_do_match.span(0)[1]
        elif next_op_type == Op.DONT:
            assert next_dont_match is not None
            doing = False
            index += next_dont_match.span(0)[1]
        elif next_op_type == Op.MULT:
            assert next_mult_match is not None
            if doing:
                x = int(next_mult_match.group(1))
                y = int(next_mult_match.group(2))
                total += x * y
            index += next_mult_match.span(0)[1]


    return total
    

if __name__ == "__main__":
    print(f"{solve_content(EXAMPLE)=}")
    with open("./input.txt") as input:
        print(f"{solve_content(input.read())=}")
    print(f"{solve_content2(EXAMPLE2)=}")
    with open("./input.txt") as input:
        print(f"{solve_content2(input.read())=}")
