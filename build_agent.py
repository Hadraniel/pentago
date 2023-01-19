from latest_board_state import latest_board_state
from apply_move import rotate_quarter_of_board
from highest_sequence import longest_sequence_in_the_whole_board
import random


class BuildAgent:
    def __init__(self, name, id):
        self.id = id
        self.time = 0
        self.name = name

    def __str__(self):
        return self.name

    def play(self):
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
            # highest_impact_move: x, y, quarter, rotation_direction, sequence_count
            highest_impact_move = [0, 0, 0, None, 0]
            for row in range(6):
                for col in range(6):
                    if board[row][col] == 0:
                        # set a marble on empty spot
                        board[row][col] = self.id
                        for q in range(1, 5):
                            # clockwise rotation:
                            board = rotate_quarter_of_board(board, q, 1)
                            highest_sequence_count = (
                                longest_sequence_in_the_whole_board(board, self.id)
                            )
                            if highest_sequence_count > highest_impact_move[4]:
                                highest_impact_move[0] = row
                                highest_impact_move[1] = col
                                highest_impact_move[2] = q
                                highest_impact_move[3] = 1
                                highest_impact_move[4] = highest_sequence_count

                            # reverse changes (rotate back)
                            board = rotate_quarter_of_board(board, q, -1)

                            # now checking the counterclockwise rotation:
                            board = rotate_quarter_of_board(board, q, -1)
                            highest_sequence_count = (
                                longest_sequence_in_the_whole_board(board, self.id)
                            )

                            if highest_sequence_count > highest_impact_move[4]:
                                highest_impact_move[0] = row
                                highest_impact_move[1] = col
                                highest_impact_move[2] = q
                                highest_impact_move[3] = -1
                                highest_impact_move[4] = highest_sequence_count

                            # revert the changes
                            board = rotate_quarter_of_board(board, q, 1)

                        # remove the marble and check the next empty place for better results !
                        board[row][col] = 0

            return (
                highest_impact_move[0],
                highest_impact_move[1],
                highest_impact_move[2],
                highest_impact_move[3],
            )
