import logging
import os
import copy
import global_variables as gv
import strategy
import strategy_open
from flask import Flask
from flask import request

app = Flask(__name__)


@app.get("/")
def handle_info():
    """
    This function is called when you register your Battlesnake on play.battlesnake.com
    See https://docs.battlesnake.com/guides/getting-started#step-4-register-your-battlesnake
    """
    print("INFO")
    return {
        "apiversion": "1",
        "author": "Sir-Pent",
        "color": "#202252",
        "head": "moustache",
        "tail": "shiny"
    }



@app.post("/start")
def handle_start():
    """
    This function is called everytime your Battlesnake enters a game.
    It's purely for informational purposes, you don't have to make any decisions here.
    request.json contains information about the game that's about to be played.
    """
    data = request.get_json()
    
    gv.BOARD_MAX_X = data["board"]["width"]
    gv.BOARD_MAX_Y = data["board"]["height"]

    print(f"{data['game']['id']} START")
    return "ok"


@app.post("/move")
def handle_move():
    """
    This function is called on every turn and is how your Battlesnake decides where to move.
    Valid moves are "up", "down", "left", or "right".
    """
    data = request.get_json()
    
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
    #multiple snakes 
    else:
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

@app.post("/end")
def handle_end():
    """
    This function is called when a game your Battlesnake was in has ended.
    It's purely for informational purposes, you don't have to make any decisions here.
    """
    data = request.get_json()

    print(f"{data['game']['id']} END")
    return "ok"


@app.after_request
def identify_server(response):
    response.headers["Server"] = "BattlesnakeOfficial/starter-snake-python"
    return response


if __name__ == "__main__":
    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    host = "0.0.0.0"
    port = int(os.environ.get("PORT", "8080"))

    print(f"\nRunning Battlesnake server at http://{host}:{port}")
    app.env = 'development'
    app.run(host=host, port=port, debug=True)