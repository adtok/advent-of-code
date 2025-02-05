from __future__ import annotations

from dataclasses import dataclass, field
from itertools import count

FILENAME = "example.txt"

SPACE = -1
HEAD = -2
TAIL = -3

id_counter = count()


def next_id():
    return next(id_counter)


@dataclass
class Block:
    file_id: int
    size: int
    next: Block | None = None
    prev: Block | None = field(default=None, repr=False)
    seen: bool = False

    def __repr__(self) -> str:
        if self.file_id == SPACE:
            return f"Space({self.size})"
        elif self.file_id == HEAD:
            return f"HEAD"
        elif self.file_id == TAIL:
            return "TAIL"
        else:
            return f"File({self.file_id}, {self.size})"

    @property
    def is_space(self) -> bool:
        return self.file_id == SPACE

    @property
    def is_file(self) -> bool:
        return self.file_id >= 0

    @property
    def has_both_links(self) -> bool:
        return self.prev is not None and self.next is not None

    def can_accept(self, other: Block) -> bool:
        other_fits = other.size <= self.size
        return (
            self.is_space and not other.is_space and other_fits and self.has_both_links
        )

    def consolidate(self) -> None:
        assert self.is_space, f"{self} only spaces can consolidate"
        p = self.prev
        n = self.next
        if p.is_space or n.is_space:
            print(self, p, n)
            if p.is_space:
                p2 = p.prev
                self.size += p.size
                p2.next = self
                self.prev = p2
            if n.is_space:
                n2 = n.next
                self.size += n.size
                n2.prev = self
                self.next = n2
            print(self)

    def detach(self) -> None:
        assert self.is_file, f"{self} only files can detach"
        assert self.has_both_links, f"{self} can't detach ({self.next=}, {self.prev=})"
        p = self.prev
        n = self.next
        new_space = Block(file_id=SPACE, size=self.size, prev=p, next=n)
        p.next = new_space
        n.prev = new_space
        self.prev = None
        self.next = None
        self.seen = True

    def destroy(self) -> None:
        assert self.has_both_links, f"{self} can't destroy ({self.next=}, {self.prev=})"
        p = self.prev
        n = self.next
        p.next = n
        n.prev = p

    def accept(self, other: Block) -> None:
        assert self.can_accept(other), f"{self} can't accept {other}"
        old_prev = self.prev
        old_prev.next = other
        other.prev = old_prev
        self.prev = other
        other.next = self
        self.size -= other.size
        if self.size == 0:
            self.destroy()

    def print(self) -> None:
        print(self, end="")
        if self.next:
            print(" -> ", end="")
            self.next.print()
        else:
            print()

    def as_string(self) -> str:
        char = "." if self.file_id < 0 else str(self.file_id)
        s = char * self.size
        if self.next:
            s += self.next.as_string()
        return s

    def _print_recursive(self, start: bool = False) -> None:
        print(f"{self}")


def main() -> None:
    part_two()


def part_two() -> None:
    with open(FILENAME, "r") as file:
        disk_map = parse(file.read())

    files = list(map(int, disk_map[::2]))
    spaces = list(map(int, disk_map[1::2])) + [0]

    # print("Start -> ", end="")
    head = Block(file_id=HEAD, size=0)
    tail = head
    for file_id, (size, spaces) in enumerate(zip(files, spaces)):
        file = Block(file_id=file_id, size=size, prev=tail)
        tail.next = file
        tail = file
        if spaces:
            space = Block(file_id=SPACE, size=spaces, prev=tail)
            tail.next = space
            tail = space
    end = Block(file_id=TAIL, size=0, next=None, prev=tail)
    tail.next = end
    tail = end
    # head.print()
    right = tail
    while (right := right.prev) != head:
        if right.is_space or right.seen:
            continue
        # print(head.as_string())
        left = head
        # print(right)
        while (left := left.next) != right:
            # print(f"\t{left}")
            if left.is_space and left.can_accept(right):
                # print("\t\tcan accept")
                curr = right
                right = curr.next
                curr.detach()
                # head.print()
                left.accept(curr)
                break
        # print()
    """
    while (right := right.prev) != head:
        if right.seen:
            continue
        right.seen = True
        curr: Block = right
        # right = right.next
        # if it's not a file, just move on to the next one
        if curr.file_id < 0:
            # print("start", curr, "is not a file")  # debug
            continue
        # print("start", curr, "is a file")  # debug
        left = head
        # print(f"\t", end="")  # debug
        while (left := left.next) != curr.prev:
            # print(f" -> {left}", end="")  # debug
            if left.can_accept(curr):
                right = curr.next
                # print(" can hold the file")  # debug
                if left.next == curr:
                    print("corner case !!!")
                # pop curr from the list
                c_prev = curr.prev
                c_next = curr.next
                c_prev.next = c_next
                c_next.prev = c_prev
                replacement_space = Block(
                    file_id=SPACE, size=curr.size, prev=c_prev, next=c_next
                )
                c_prev.next = replacement_space
                c_next.prev = replacement_space

                # pop left from the list and replace it with new File -> Space
                l_prev = left.prev
                l_next = left.next
                remaining = left.size - curr.size
                new_space = Block(file_id=SPACE, size=remaining, prev=curr, next=l_next)
                curr.prev = l_prev
                curr.next = new_space
                l_prev.next = curr
                l_next.prev = new_space
                # head.print()
                break
        # print()  # debug
        # print(head.as_string())
    # head.print()"""
    # print(head.as_string())
    result = checksum_l(head)
    print(result)
    print(total_nodes(head))
    assert result == 6423258376982, "checksum wrong"


def part_one() -> None:
    with open(FILENAME, "r") as file:
        disk_map = parse(file.read())

    files = list(map(int, disk_map[::2]))
    spaces = list(map(int, disk_map[1::2]))

    total_data = sum(files)
    print(total_data)
    total_space = sum(spaces)
    print(total_space)

    disk = []
    data = []
    for i, (size, spaces) in enumerate(zip(files, spaces + [0])):
        disk += size * [i] + spaces * [None]
        data += size * [i]

    total_pops = sum(datum is not None for datum in disk[-total_space:])
    print(total_pops)
    packed = [*disk][:total_data]

    assert sum(datum is None for datum in packed) == total_pops

    for i in range(total_data):
        if packed[i] is None:
            datum = data.pop()
            packed[i] = datum

    result = checksum(packed)
    print(result)


def parse(line: str):
    return line.strip()


def build(files: list[int], spaces: list[int]):
    pass


def checksum(disk: list[int]) -> int:
    return sum(position * value for position, value in enumerate(disk))


def total_nodes(node: Block) -> int:
    total = 1
    while (node := node.next) != None:
        total += 1
    return total


def checksum_l(node: Block) -> int:
    total = 0
    idx = 0
    while (node := node.next).file_id != TAIL:
        value = 0 if node.file_id < 0 else node.file_id
        for _ in range(node.size):
            total += idx * value
            idx += 1
    return total


if __name__ == "__main__":
    main()
