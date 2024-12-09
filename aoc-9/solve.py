from typing import List
from dataclasses import dataclass

from itertools import pairwise

from llist import dllist


EXAMPLE = """\
2333133121414131402
"""


@dataclass
class Block:
    size: int
    is_file: bool
    id: int


Disk = List[Block]


def parse_content(content: str) -> Disk:
    disk = []
    for i, v in enumerate(content.rstrip()):
        is_file = i % 2 == 0
        disk.append(Block(int(v), is_file, i // 2))
    return disk


def format_debug(disk: Disk) -> str:
    def format_block(block: Block) -> str:
        if block.is_file:
            return str(block.id) * block.size
        else:
            return "." * block.size

    return "".join(format_block(b) for b in disk)


def solve(disk: Disk) -> int:
    new_disk = dllist(disk.copy())
    last_file_block = next(( v for v in reversed(new_disk) if v.is_file))

    while True:
        last_file_block = next(( v for v in reversed(new_disk) if v.is_file))

        holes = 0
        for b in new_disk:
            if b.is_file and b.id == last_file_block.id:
                break
            if not b.is_file:
                holes += b.size
        if holes < 0:
            raise AssertionError
        if holes == 0:
            break

        last_file_block_size = last_file_block.size
        for _ in range(last_file_block_size):
            first_free_block_maybe = next(( v for v in enumerate(new_disk) if not v[1].is_file and v[1].size > 0), None)
            if first_free_block_maybe is None:
                break
            i_first_free_block, first_free_block = first_free_block_maybe
            if first_free_block.size == 1:
                new_disk[i_first_free_block] = Block(1, True, last_file_block.id)
            else:
                new_disk[i_first_free_block].size -= 1
                node = new_disk.nodeat(i_first_free_block)
                new_disk.insertbefore(Block(1, True, last_file_block.id), node)

            # print(f"{format_debug(new_disk)=} {holes=}")
            last_file_block.size -= 1
            holes -= 1
            if holes <= 0:
                break

        if last_file_block.size == 0:
            last_file_block.size = last_file_block_size
            last_file_block.is_file = False

    checksum = 0
    i = 0
    for b in new_disk:
        if b.is_file:
            for j in range(b.size):
                checksum += b.id * (i + j)
        i += b.size

    if len(new_disk) < 100:
        print(f"{format_debug(new_disk)=} {checksum=}")
    return checksum



def solve2(disk: Disk) -> int:
    new_disk = dllist(disk.copy())
    last_file_block = next(( v for v in reversed(new_disk) if v.is_file))

    move_attempt = set()

    while True:
        last_file_block = next(( v for v in reversed(new_disk) if v.is_file and not v.id in move_attempt), None)
        if last_file_block is None:
            break

        # merge holes
        merged = dllist([])
        hole = 0
        for b in new_disk:
            if not b.is_file:
                hole += b.size
            else:
                if hole > 0:
                    merged.append(Block(hole, False, 0))
                    hole = 0
                merged.append(b)
        new_disk = merged
        
        # print(f"attempting to move {last_file_block.id}")
        move_attempt.add(last_file_block.id)

        last_file_block_position = None
        for i, b in enumerate(new_disk):
            if b.is_file and b.id == last_file_block.id:
                last_file_block_position = i

        assert last_file_block_position is not None

        last_file_block_size = last_file_block.size
        first_free_block_maybe = next(( v for v in enumerate(new_disk) if not v[1].is_file and v[1].size >= last_file_block_size), None)
        if first_free_block_maybe is None:
            # print(f"could not find a slot for {last_file_block.id}")
            continue
        i_first_free_block, first_free_block = first_free_block_maybe
        
        if i_first_free_block > last_file_block_position:
            # print(f"refusing to move {last_file_block.id} to the right")
            continue

        if first_free_block.size == 1:
            new_disk[i_first_free_block] = Block(1, True, last_file_block.id)
        else:
            new_disk[i_first_free_block].size -= last_file_block_size
            node = new_disk.nodeat(i_first_free_block)
            new_disk.insertbefore(Block(last_file_block_size, True, last_file_block.id), node)

        # print(f"{format_debug(new_disk)=}")
        last_file_block.size = last_file_block_size
        last_file_block.is_file = False

    checksum = 0
    i = 0
    for b in new_disk:
        if b.is_file:
            for j in range(b.size):
                checksum += b.id * (i + j)
        i += b.size

    if len(new_disk) < 100:
        print(f"{format_debug(new_disk)=} {checksum=}")
    return checksum


if __name__ == "__main__":
    print(f"{solve(parse_content(EXAMPLE))=}")
    print(f"{solve2(parse_content(EXAMPLE))=}")
    with open("./input.txt") as input_file:
        content = input_file.read()
        # print(f"{solve(parse_content(content))}")
        print(f"{solve2(parse_content(content))}")
