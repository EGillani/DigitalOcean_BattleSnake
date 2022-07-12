from typing import List
import global_variables as gv
#have a library with our strategy
import strategy
import strategy_open
import copy

"""
This file can be a nice home for your Battlesnake's logic and helper functions.

We have started this for you, and included some logic to remove your Battlesnake's 'neck'
from the list of possible moves!
"""

def get_info() -> dict:
    """
    This controls your Battlesnake appearance and author permissions.
    For customization options, see https://docs.battlesnake.com/references/personalization

    TIP: If you open your Battlesnake URL in browser you should see this data.
    """
    return {
        "apiversion": "1",
        "author": "Sir-Pent",  
        "color": "#202252", 
        "head": "moustache",  
        "tail": "shiny", 
    }


def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_snake = data["you"]      # A dictionary describing your snake's position on the board
    my_head = my_snake["head"]  # A dictionary of coordinates like {"x": 0, "y": 0}
    my_body = my_snake["body"]  # A list of coordinate dictionaries like [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]

    # Uncomment the lines below to see what this data looks like in your output!
    # print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    # print(f"All board data this turn: {data}")
    # print(f"My Battlesnake this turn is: {my_snake}")
    # print(f"My Battlesnakes head this turn is: {my_head}")
    # print(f"My Battlesnakes body this turn is: {my_body}")

    snake_walls = []
    other_snakes_wall = []
    food_and_snakes = []
    all_food = []
    board = []
    length_of_each_snake = []
    #populating an empty board 
    for row in range(gv.BOARD_MAX_X):
        board.append([])
        for column in range(gv.BOARD_MAX_Y):
            board[row].append(1)

    #populating snake parts
    #have list of our other snakes body parts that will act as our walls
    all_snake_body_parts = strategy.other_snakes(data)
    for part in all_snake_body_parts:
        snake_walls.append((part["x"], part["y"]))
        board[part["x"]][part["y"]] = 0
        if part not in data["you"]["body"]:
            other_snakes_wall.append((part["x"], part["y"]))


    #populating all the food
    all_food_data = data["board"]["food"]
    for food in all_food_data:
        all_food.append((food["x"], food["y"]))
        board[food["x"]][food["y"]] = 0

    food_and_snakes = copy.deepcopy(snake_walls)
    for food in all_food_data:
        food_and_snakes.append((food["x"], food["y"]))

    curr_number_of_snakes = len(data["board"]["snakes"])
    snakes = data["board"]["snakes"]
    our_length = data["you"]["length"]
    curr_total_length = 0
    #get length of each snake
    for snake in snakes:
        if snake["name"] != data["you"]["name"]:
            length_of_each_snake.append(snake["length"])

    curr_total_length = len(other_snakes_wall)
    avg_length = (curr_total_length)/curr_number_of_snakes
    ##########3 or less Snakes###############
    if curr_number_of_snakes <= 2:
        if data["you"]["health"] > 90 and our_length < avg_length:
            move = strategy_open.go_to_open(data, board, food_and_snakes, snake_walls, other_snakes_wall)
        if move is not None:
            print(f"MOVE: {move}")
            return {"move": move}
        else: #go for food
            move = strategy.go_for_food_Dij(data,snake_walls, other_snakes_wall, all_food)
        if move is None:
            move = strategy_open.go_to_open(data, board, food_and_snakes, snake_walls, other_snakes_wall)
            if move is not None:
                print(f"MOVE: {move}")
                return {"move": move}
    else:#multiple snakes 
        if data["you"]["health"] > 95 and our_length < 5:
            move = strategy_open.go_to_open(data, board, food_and_snakes, snake_walls, other_snakes_wall)
        if move is not None:
            print(f"MOVE: {move}")
            return {"move": move}
        else: #go for food
            move = strategy.go_for_food_Dij(data,snake_walls, other_snakes_wall, all_food)
        if move is None:
            move = strategy_open.go_to_open(data, board, food_and_snakes, snake_walls, other_snakes_wall)
            if move is not None:
                print(f"MOVE: {move}")
                return {"move": move}
    #######################################


    print(f"MOVE: {move}")
    return {"move": move}




def _avoid_my_neck(my_body: dict, possible_moves: List[str]) -> List[str]:
    """
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    my_head = my_body[0]  # The first body coordinate is always the head
    my_neck = my_body[1]  # The segment of body right after the head is the 'neck'

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.remove("up")

    return possible_moves
