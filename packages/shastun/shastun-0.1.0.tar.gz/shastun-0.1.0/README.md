[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
# Shastun Game Core

## Overview
This project is a Python application using Python 3.12.3. 
The primary objective of this project is to provide a reusable core of Shastun Game.

## Requirements
This project requires the following dependencies:
- Python 3.12.3

## Installation
To install the necessary packages, you can use pip:
```bash
pip install shastun
```

## Usage
Describe how to use your project here. For example:

```bash
from shastun import User, Dice, Game

player1 = User("Alice")
player2 = User("Bob")
dice = Dice(sides=6, count=2)

game = Game(board_size=12, dice=dice, players=[player1, player2])

print("Shastun Game")

for i in range(3):
    print("Score |", " | ".join([f"{player.name}: {player.wins}" for player in game.players]))
    match = game.new_match()
    print(f"Match: {i + 1}")
    while match.finished is False:
        print(match.player, "[", match.board, "]", end=None)

        input("Press Enter to roll")

        throw = game.throw()
        print(throw)

        choices = game.choices(throw)

        if len(choices) > 0:
            print("Choose a value from the following options:")
            for index, choice in enumerate(choices, start=1):
                print(f"{index}. {list(choice)}")
            chosen_index = int(input("Enter the number of your chosen value: "))
            selected_choice = choices[chosen_index - 1]
            print("Selected:", list(selected_choice))
            match.move(selected_choice)
            print(game.match.board)
        else:
            print("No valid moves available.")

        print("")
        print(" - " * 20)
        print("")
        match.next_player()

    print("Match finished. Winner:", match.winner.name, "| Rolls:", match.score_for(match.winner))

print("Game finished.")
for player in game.players:
    print(f"{player.name}: {player.wins}")

```

## Contributing
To contribute to this project, you can follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-branch`
5. Submit a pull request.

## License
This project is MIT.

## Contact
If you have any questions or issues, please contact "Besya <gravisbesya@list.ru>".

[//]: # (## Acknowledgments)

[//]: # (- List any resources, tutorials, or contributors you'd like to thank.)