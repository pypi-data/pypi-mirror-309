class Player:
    def __init__(self, name: str, wins: int = 0):
        self.name = name
        self.wins = wins

    def __repr__(self):
        return f'{self.__class__.__name__}(name="{self.name}", wins={self.wins})'
