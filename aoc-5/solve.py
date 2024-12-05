from dataclasses import dataclass
from typing import List, Tuple

EXAMPLE = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""


@dataclass
class Input:
    rules: List[Tuple[int, int]]
    updates: List[List[int]]


def parse_content(content: str) -> Input:
    input = Input(rules=[], updates=[])
    for line in content.splitlines():
        if "|" in line:
            rule = tuple([int(v) for v in line.split("|")])
            input.rules.append(rule)
        if "," in line:
            update = list([int(v) for v in line.split(",")])
            input.updates.append(update)

    return input


def rule_ok(
    update: List[int], position: int, rule: Tuple[int, int], debug=False
) -> bool:
    if update[position] == rule[0]:
        valid = rule[1] not in update[:position]
        if not valid and debug:
            print(
                f"{update=} {position=} {rule=} invalid because {rule[1]} in {update[:position]}"
            )
        return valid
    if update[position] == rule[1]:
        valid = rule[0] in update[:position]
        if not valid and debug:
            print(
                f"{update=} {position=} {rule=} invalid because {rule[0]} not in {update[:position]}"
            )
    return True


def update_ok(update: List[int], applicable_rules: List[Tuple[int, int]]) -> bool:
    for i, _ in enumerate(update):
        for rule in applicable_rules:
            if not rule_ok(update, i, rule):
                return False
    return True


def fix_invalid_update(
    update: List[int], applicable_rules: List[Tuple[int, int]]
) -> List[int]:
    fixed = update.copy()
    while not (update_ok(fixed, applicable_rules)):
        for rule in applicable_rules:
            position_before = fixed.index(rule[0])
            position_after = fixed.index(rule[1])
            if position_before > position_after:
                fixed[position_after] = rule[0]
                fixed[position_before] = rule[1]

    return fixed


def filter_valid_updates(input: Input) -> List[List[int]]:
    valid_updates = []
    for update in input.updates:
        applicable_rules = [
            rule for rule in input.rules if (rule[0] in update and rule[1] in update)
        ]
        if update_ok(update, applicable_rules):
            valid_updates.append(update)
    return valid_updates


def solve_content(content: str) -> int:
    input = parse_content(content)
    valid_updates = filter_valid_updates(input)
    # print(f"{valid_updates=}")
    return sum(v[len(v) // 2] for v in valid_updates)


def solve_content2(content: str) -> int:
    input = parse_content(content)
    fixed_updates = []
    for update in input.updates:
        applicable_rules = [
            rule for rule in input.rules if (rule[0] in update and rule[1] in update)
        ]
        if not update_ok(update, applicable_rules):
            fixed = fix_invalid_update(update, applicable_rules)
            fixed_updates.append(fixed)

    # print(f"{fixed_updates=}")
    return sum(v[len(v) // 2] for v in fixed_updates)


if __name__ == "__main__":
    print(f"{solve_content(EXAMPLE)=}")
    print(f"{solve_content2(EXAMPLE)=}")
    with open("./input.txt") as input_file:
        content = input_file.read()
        print(f"{solve_content(content)=}")
        print(f"{solve_content2(content)=}")
