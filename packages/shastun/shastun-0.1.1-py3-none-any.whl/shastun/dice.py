import itertools
import random


class Dice:
    def __init__(self, sides: int, count: int = 1):
        self.count = count
        self.sides = sides
        self.combinations = self._generate_combinations()
        self.uniq_combinations = self._generate_uniq_combinations()

    def roll(self) -> tuple[int, ...]:
        return tuple(random.randint(1, self.sides) for _ in range(self.count))

    def _generate_combinations(self) -> list[tuple[int, ...]]:
        return list(
            itertools.product(*[range(1, self.sides + 1) for _ in range(self.count)])
        )

    def _generate_uniq_combinations(self) -> list[tuple[int, ...]]:
        return sorted(
            [tuple(x) for x in {tuple(sorted(comb)) for comb in self.combinations}]
        )

    def __repr__(self):
        return f"Dice({self.sides}, {self.count})"
