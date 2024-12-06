class Throw:
    def __init__(self, roll: tuple[int, ...]):
        self.roll = roll
        self.sum = sum(roll)
        self.all_equal = len(set(roll)) == 1
        self.all_different = len(set(roll)) == len(roll)
        self.options = self._calculate_options()

    def __repr__(self):
        return f"Throw({self.roll}) | Options: {self.options}"

    def __eq__(self, other):
        return self.roll == other.roll

    def _calculate_options(self) -> list[tuple[int, ...]]:
        opts: list[tuple[int, ...]] = []
        if self.all_equal:
            opts.append((self.roll[0],))
        elif self.all_different:
            opts.append(self.roll)
        opts.append((self.sum,))
        return opts
