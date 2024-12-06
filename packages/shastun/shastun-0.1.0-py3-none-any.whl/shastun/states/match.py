from ..actors import Player
from ..models import Board, Dice


class Match:
    def __init__(self, size: int, dice: Dice, players: list[Player]):
        self.size = size
        self.dice = dice
        self.finished = False
        self.winner: Player | None = None
        self.players = players
        self.boards = [Board(size) for _ in range(len(players))]
        self.rolls = [[] for _ in range(len(players))]
        self.last_roll: tuple[int, ...] | None = None
        self.player = players[0]

    @property
    def player_index(self) -> int:
        return self.players.index(self.player)

    @property
    def board(self) -> Board:
        return self.boards[self.player_index]

    @property
    def score(self):
        return [len(r) for r in self.rolls]

    def score_for(self, player: Player):
        return self.score[self.players.index(player)]

    def board_for(self, player: Player) -> Board:
        return self.boards[self.players.index(player)]

    def roll(self):
        self.last_roll = self.dice.roll()
        self.rolls[self.player_index].append(self.last_roll)
        return self.last_roll

    def next_player(self):
        index = self.player_index
        self.player = self.players[(index + 1) % len(self.players)]
        return self.player

    def finish(self, winner: Player):
        self.winner = winner
        self.winner.wins += 1
        self.finished = True

    def move(self, items: tuple[int, ...]):
        self.board.remove(items)
        if len(self.board) == 0:
            self.finish(self.player)

    def __repr__(self):
        tab = " " * 2
        result = "Match(\n"
        result += tab
        result += "Players [\n"
        for player in self.players:
            result += tab * 2
            result += f"{player}\n"
        result += tab
        result += "]\n"
        result += tab
        result += "Boards [\n"
        for board in self.boards:
            result += tab * 2
            result += f"{board}\n"
        result += tab
        result += "]\n"
        result += tab
        result += "Rolls [\n"
        for rolls in self.rolls:
            result += tab * 2
            result += f"{rolls}\n"
        result += tab
        result += "]\n"
        result += ")"
        return result
