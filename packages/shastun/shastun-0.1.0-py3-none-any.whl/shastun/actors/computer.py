from .player import Player


class Computer(Player):
    def __init__(self, number: int):
        super().__init__(f"Computer {number}")
