from typing import Collection


class Board(list[int]):
    def __init__(self, size: int):
        super().__init__(range(1, size + 1))

    def __sub__(self, other):
        self.remove(other)
        return self

    def __repr__(self):
        return f"Board({len(self)}) [{[i for i in self]}]"

    def remove(self, other):
        if isinstance(other, int):
            super().remove(other)
        elif isinstance(other, Collection):
            for i in other:
                super().remove(i)
        else:
            raise ValueError("Invalid input for removal")
