import numpy as np
import random
from latest_board_state import latest_board_state
from apply_move import apply_move


class AdjacentAgent:
    def __init__(self, name, id):
        self.id = id
        self.time = 0
        self.name = name

    def find_empty_places(self, board):
        empty_places = []
        for i, j in zip(np.where(board == 0)[0], np.where(board == 0)[1]):
            empty_places.append((i, j))
        return empty_places

    def __str__(self):
        return self.name

    def play(self):
        # returns True if the neightbor marble has the same color as the marble
        def adjancent_with_same_id(board, player_id, x, y):
            return (
                board[x + 1][y] == player_id
                and board[x - 1][y] == player_id
                and board[x][y + 1] == player_id
                and board[x][y - 1] == player_id
            )

        # REMOVES the padding
        def return_to_original(all_arr):
            ans = []
            for arr in all_arr:
                ans.append(((arr[0] - 1), (arr[1] - 1)))
            return ans

        board = latest_board_state()
        if self.time == 0:
            empty_places = []
            for i in range(6):
                for j in range(6):
                    if board[i][j] == 0:
                        empty_places.append((i, j))
            x, y = random.choice(empty_places)
            quarter = random.choice([1, 2, 3, 4])
            direction = random.choice([-1, 1])
            self.time += 1
            return x, y, quarter, direction

        else:
            last_filtered_choices = []
            board_with_padding = np.pad(
                board, 1, mode="constant", constant_values=(-1,)
            )
            available_choices = self.find_empty_places(board_with_padding)
            for x, y in available_choices:
                if adjancent_with_same_id(board_with_padding, self.id, x, y):
                    last_filtered_choices.append((x, y))
            last_filtered_choices = return_to_original(last_filtered_choices)
            if last_filtered_choices != []:
                x, y = random.choice(last_filtered_choices)
            else:
                x = random.choice([1, 2, 3, 4, 5])
                y = random.choice([1, 2, 3, 4, 5])
            quarter = random.choice([1, 2, 3, 4])
            direction = random.choice([-1, 1])

            # apply_move(board, self.id, x, y, quarter, direction)
            return (x, y, quarter, direction)
