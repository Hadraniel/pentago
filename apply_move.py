import numpy as np
import pandas as pd


def apply_move(board, player_id, x, y, quarter, direction):
    """
    here, we apply the player's moves to the board:
        1- update the record and save it
        2- apply changes to the board

    direction:
        +1: 90 degrees clockwise
        -1: 90 degrees counterclockwise
    player id:
        player 1: 1
        player 2: 2

    and also, just a reminder:
                quarter 1: [:3][:3]
                quarter 2: [:3][3:]
                quarter 3: [3:][:3]
                quarter 4: [3:][3:]

    """

    def get_board_quarter(x, board):
        quarter_dict = {
            1: board[:3, :3],
            2: board[:3, 3:],
            3: board[3:, :3],
            4: board[3:, 3:],
        }
        return quarter_dict[x]

    def set_board_quarter(x, board, rotated_quarter):
        if x == 1:
            board[:3, :3] = rotated_quarter
        elif x == 2:
            board[:3, 3:] = rotated_quarter
        elif x == 3:
            board[3:, :3] = rotated_quarter
        else:
            board[3:, 3:] = rotated_quarter
        return board

    board[x][y] = player_id
    rotated_quarter = get_board_quarter(quarter, board)
    if direction == 1:
        # k = 3 -> clockwise rotation
        rotated_quarter = np.rot90(rotated_quarter, k=3, axes=(0, 1))
    elif direction == -1:
        # k = 1 -> counter clockwise rotation
        rotated_quarter = np.rot90(rotated_quarter, k=1, axes=(0, 1))
    board = set_board_quarter(quarter, board, rotated_quarter)
    serialString = ""
    for row in board:
        for value in row:
            serialString += str(value)
            serialString += ","
        serialString = serialString[:-1]
        serialString += ","
    file = open("record.hbd", "a")
    file.write(serialString + "\n")
    file.close()


# this function rotates a quarter of the board and returns the modified board
def rotate_quarter_of_board(board, q, direction):
    # direction: clockwise +1  counterclockwise -1
    temp_board = board
    quarter_dict = {
        1: temp_board[:3, :3],
        2: temp_board[:3, 3:],
        3: temp_board[3:, :3],
        4: temp_board[3:, 3:],
    }[q]
    if direction == 1:
        rotated_quarter = np.rot90(quarter_dict, k=3, axes=(0, 1))
    else:
        rotated_quarter = np.rot90(quarter_dict, k=1, axes=(0, 1))
    if q == 1:
        temp_board[:3, :3] = rotated_quarter
    elif q == 2:
        temp_board[:3, 3:] = rotated_quarter
    elif q == 3:
        temp_board[3:, :3] = rotated_quarter
    else:
        temp_board[3:, 3:] = rotated_quarter
    return temp_board
