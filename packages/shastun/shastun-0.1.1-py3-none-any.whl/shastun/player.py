from dataclasses import dataclass


@dataclass
class Player:
    name: str
    wins: int = 0
