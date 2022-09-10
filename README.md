# Sir Pent [Battlesnake](http://play.battlesnake.com?utm_source=github&utm_medium=readme&utm_campaign=python_starter&utm_content=homepage)

![Battlesnake Logo](/sirpent.png)

Implements [Battlesnake API](https://docs.battlesnake.com/references/api) in Python. Algorithm used was A* Implementation and brute force. 

## Technologies Used

* [Python3](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/)
## Behavior

On every turn of each game your Battlesnake receives information about the game board and must decide its next move.

Locate the `choose_move` function inside [logic.py](logic.py#L27). Possible moves are "up", "down", "left", or "right" and initially your Battlesnake will choose a move randomly. Your goal as a developer is to read information sent to you about the game (available in the `data` variable) and decide where your Battlesnake should move next. All your Battlesnake logic lives in [logic.py](logic.py), and this is the code you will want to edit.

See the [Battlesnake Game Rules](https://docs.battlesnake.com/references/rules) for more information on playing the game, moving around the board, and improving your algorithm.