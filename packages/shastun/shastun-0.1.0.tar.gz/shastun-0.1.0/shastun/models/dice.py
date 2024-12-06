import itertools
import random
from functools import cached_property


class Dice:
    def __init__(self, sides: int, count: int = 1):
        self.count = count
        self.sides = sides

    def roll(self) -> tuple[int, ...]:
        return tuple(random.randint(1, self.sides) for _ in range(self.count))

    @cached_property
    def combinations(self) -> list[tuple[int, ...]]:
        return list(
            itertools.product(*[range(1, self.sides + 1) for _ in range(self.count)])
        )

    @cached_property
    def uniq_combinations(self) -> list[tuple[int, ...]]:
        return sorted(
            [tuple(x) for x in {tuple(sorted(comb)) for comb in self.combinations}]
        )

    def __repr__(self):
        return f"Dice({self.sides}, {self.count})"
