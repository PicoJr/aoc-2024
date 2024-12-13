from typing import List, Optional
from dataclasses import dataclass
from itertools import batched
import re

EXAMPLE=\
"""\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

TOKEN_A = 3
TOKEN_B = 1

@dataclass
class ClawMachine:
    a_button_dx: int
    a_button_dy: int
    b_button_dx: int
    b_button_dy: int
    prize_x: int
    prize_y: int


def load_content(content: str) -> List[ClawMachine]:

    button_re = re.compile(r"Button [AB]: X\+(\d+), Y\+(\d+)")
    prize_re = re.compile(r"Prize: X=(\d+), Y=(\d+)")

    content_tweaked = content + "ignored\n"
    
    machines = []
    for lineA, lineB, linePrize, _ in batched(content_tweaked.splitlines(), 4):
        claw_machine = ClawMachine(0,0,0,0,0,0)
        button_A = button_re.match(lineA)
        assert button_A is not None
        claw_machine.a_button_dx = int(button_A.group(1))
        claw_machine.a_button_dy = int(button_A.group(2))
        button_B = button_re.match(lineB)
        assert button_B is not None
        claw_machine.b_button_dx = int(button_B.group(1))
        claw_machine.b_button_dy = int(button_B.group(2))
        prize = prize_re.match(linePrize)
        assert prize is not None
        claw_machine.prize_x = int(prize.group(1))
        claw_machine.prize_y = int(prize.group(2))
        
        machines.append(claw_machine)

    return machines


def solve_machines(machines: List[ClawMachine]) -> int:
    total_tokens = 0
    for machine in machines:
        min_tokens: Optional[int] = None
        for press_a in range(100 + 1):
            for press_b in range(100 + 1):
                position_x = press_a * machine.a_button_dx + press_b * machine.b_button_dx
                position_y = press_a * machine.a_button_dy + press_b * machine.b_button_dy
                if position_x == machine.prize_x and position_y == machine.prize_y:
                    tokens = TOKEN_A * press_a + TOKEN_B * press_b
                    if min_tokens is None:
                        min_tokens = tokens
                    elif min_tokens > tokens:
                        min_tokens = tokens

        if min_tokens is not None:
            total_tokens += min_tokens
    return total_tokens

if __name__ == "__main__":
    # print(f"{load_content(EXAMPLE)=}")
    print(f"{solve_machines(load_content(EXAMPLE))=}")
    with open("./input.txt") as input_file:
        machines = load_content(input_file.read())
        print(f"{solve_machines(machines)=}")
