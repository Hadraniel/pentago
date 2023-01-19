import numpy as np
import random
from latest_board_state import latest_board_state


class RandomAgent:
    def __init__(self, name, id):
        self.id = id
        self.rank = 0
        self.name = name

    def __str__(self):
        return self.name

    def find_empty_places(self, board):
        empty_places = []
        for i in range(6):
            for j in range(6):
                if board[i][j] == 0:
                    empty_places.append((i, j))
        return empty_places

    def play(self):
        board = latest_board_state()
        available_choices = self.find_empty_places(board)
        x, y = random.choice(available_choices)
        quarter = random.choice([1, 2, 3, 4])
        direction = random.choice([-1, 1])
        # apply_move(board, self.id, x, y, quarter, direction)
        return x, y, quarter, direction
