from __future__ import annotations

from shared import read_text_file
from typing import List


class Instruction:
    def __init__(self, string: str):
        self.string = string
        self.action = string.split(" ")[0]
        xmin = int(string.split("x=")[1].split("..")[0])
        xmax = int(string.split("x=")[1].split("..")[1].split(",")[0])
        ymin = int(string.split("y=")[1].split("..")[0])
        ymax = int(string.split("y=")[1].split("..")[1].split(",")[0])
        zmin = int(string.split("z=")[1].split("..")[0])
        zmax = int(string.split("z=")[1].split("..")[1].split(",")[0])
        self.cuboid = Cuboid(range(xmin, xmax+1), range(ymin, ymax+1), range(zmin, zmax+1))

    def __repr__(self):
        return f"Instruction({self.action}: {self.cuboid})"


class Cuboid:
    def __init__(self, xrange: range, yrange: range, zrange: range):
        self.xrange = xrange
        self.yrange = yrange
        self.zrange = zrange

    def volume(self) -> int:
        return len(self.xrange) * len(self.yrange) * len(self.zrange)

    def overlap_volume(self, other: Cuboid) -> int:
        overlap = self.overlap_region(other)
        return overlap.volume()

    def overlap_region(self, other: Cuboid) -> Cuboid:
        if len(self.xrange) * len(self.yrange) * len(self.zrange) \
                * len(other.xrange) * len(other.yrange) * len(other.zrange) == 0:
            return Cuboid(range(0), range(0), range(0))
        xrange = range(max(self.xrange[0], other.xrange[0]), min(self.xrange[-1], other.xrange[-1]) + 1)
        yrange = range(max(self.yrange[0], other.yrange[0]), min(self.yrange[-1], other.yrange[-1]) + 1)
        zrange = range(max(self.zrange[0], other.zrange[0]), min(self.zrange[-1], other.zrange[-1]) + 1)
        return Cuboid(xrange, yrange, zrange)

    def nonoverlapping_volume(self, others: List[Cuboid]) -> int:
        """Find the volume of this cuboid that *doesn't* overlap with any other cuboids."""
        volume = self.volume()
        overlap_regions = [self.overlap_region(x) for x in others]
        # filter out regions with no overlap -- performance is much worse if we include these
        overlap_regions = [x for x in overlap_regions if x.volume() > 0]
        for i, x in enumerate(overlap_regions):
            volume -= x.nonoverlapping_volume(overlap_regions[i+1:])
        return volume

    def in_limited_range(self):
        return min(*self.xrange, *self.yrange, *self.zrange) >= -50 \
                and max(*self.xrange, *self.yrange, *self.zrange) <= 50

    def __repr__(self):
        return f"Cuboid(x={self.xrange}, y={self.yrange}, z={self.zrange})"


def count_cubes(instructions: List[Instruction], limit_range: bool = False):
    # only turn on volumes that won't be touched by later instructions -- this way we don't
    # turn on volumes that will be turned off later, and we only turn volumes on once
    volume = 0
    if limit_range:
        instructions = [x for x in instructions if x.cuboid.in_limited_range()]
    for i, inst in enumerate(instructions):
        if inst.action == "on":
            later_cuboids = [x.cuboid for x in instructions[i+1:]]
            volume += inst.cuboid.nonoverlapping_volume(later_cuboids)
    return volume


def parse_data(path: str) -> List[Instruction]:
    data = read_text_file(path)
    return [Instruction(x) for x in data]


if __name__ == "__main__":
    data = parse_data("data/22.txt")

    ### Part 1
    out = count_cubes(data, limit_range=True)
    print(f"Solution 22a: {out}")

    ### Part 2
    print(f"Solution 22b: {count_cubes(data)}")
