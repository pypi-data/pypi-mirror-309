from .player import Player


class User(Player):
    def __init__(self, name: str):
        super().__init__(name)
