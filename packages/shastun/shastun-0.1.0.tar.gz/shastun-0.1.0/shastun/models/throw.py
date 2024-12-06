from functools import cached_property


class Throw:
    def __init__(self, roll: tuple[int, ...]):
        self.roll = roll

    def __repr__(self):
        return f"Throw({self.roll}) | Options: {self.options}"

    @property
    def all_equal(self) -> bool:
        return len(set(self.roll)) == 1

    @property
    def all_different(self) -> bool:
        return len(set(self.roll)) == len(self.roll)

    @property
    def sum(self) -> int:
        return sum(self.roll)

    @cached_property
    def options(self) -> list[tuple[int, ...]]:
        opts: list[tuple[int, ...]] = []
        if self.all_equal:
            opts.append((self.roll[0],))
        elif self.all_different:
            opts.append(self.roll)
        opts.append((self.sum,))
        return opts

    def __eq__(self, other):
        return self.roll == other.roll
