from ..actors import Player
from ..models import Dice, Throw
from ..states import Match


class Game:
    def __init__(self, board_size: int, dice: Dice, players: list[Player]):
        self.board_size = board_size
        self.dice = dice
        self.players = players
        self.matches: list[Match] = []

    @property
    def match(self) -> Match:
        return self.matches[-1]

    @property
    def player(self) -> Player:
        return self.match.player

    def new_match(self):
        match = Match(self.board_size, self.dice, self.players)
        self.matches.append(match)
        return match

    def roll(self) -> tuple[int, ...]:
        return self.match.roll()

    def throw(self) -> Throw:
        return Throw(self.roll())

    def choices(self, current_throw: Throw):
        return [
            choice
            for choice in current_throw.options
            if all(item in self.match.board for item in choice)
        ]
