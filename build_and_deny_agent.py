from latest_board_state import latest_board_state
from highest_sequence import longest_sequence_in_the_whole_board
from apply_move import rotate_quarter_of_board
import random


class BuildAndDenyAgent:
    """
    in this agent, we will decide our next move based on the highest score that we achieve.
    each time we try to make longest sequence of our marbles and also make the opponent's sequence short as possible!
    we subtract the scores and the max score is the best move !

    """

    def __init__(self, name, id):
        self.id = id
        self.time = 0
        self.name = name

    def check_win(self, score_dict):
        for score in score_dict:
            if score_dict[score][self.id] == 5:
                return score[1], score[2], score[3], score[4]
        return False

    def __str__(self):
        return self.name

    def play(self):
        # reminder: clockwise: +1  counterclockwise: -1
        # example: score_dict = { ('player_id','x','y','q', 1): {1: 10, 2: 20} }
        max_impact = -9999
        best_play = None
        score_dict = {}
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
            player1_max_sequence_old = longest_sequence_in_the_whole_board(board, 1)
            player2_max_sequence_old = longest_sequence_in_the_whole_board(board, 2)
            for row in range(6):
                for col in range(6):
                    if board[row][col] == 0:
                        # set a marble on empty spot
                        board[row][col] = self.id
                        for q in range(1, 5):
                            # clockwise rotation:
                            board = rotate_quarter_of_board(board, q, 1)
                            max_sequence_player1 = longest_sequence_in_the_whole_board(
                                board, 1
                            )
                            max_sequence_player2 = longest_sequence_in_the_whole_board(
                                board, 2
                            )
                            score_dict[(self.id, row, col, q, 1)] = {
                                1: max_sequence_player1,
                                2: max_sequence_player2,
                            }
                            # reverse changes (rotate back)
                            board = rotate_quarter_of_board(board, q, -1)
                            # now checking the counterclockwise rotation:
                            board = rotate_quarter_of_board(board, q, -1)

                            max_sequence_player1 = longest_sequence_in_the_whole_board(
                                board, 1
                            )
                            max_sequence_player2 = longest_sequence_in_the_whole_board(
                                board, 2
                            )
                            score_dict[(self.id, row, col, q, -1)] = {
                                1: max_sequence_player1,
                                2: max_sequence_player2,
                            }
                            board = rotate_quarter_of_board(board, q, 1)
            if not (self.check_win(score_dict) == False):
                return self.check_win(score_dict)

            # example: score_dict = { ('player_id','x','y','q', 1): {1: 10, 2: 20} }
            score_diff_1 = score_dict[score][1] - player1_max_sequence_old
            score_diff_2 = score_dict[score][2] - player2_max_sequence_old
            if self.id == 1:
                for score in score_dict:
                    if (score_diff_1 - score_diff_2) > max_impact:
                        max_impact = score_diff_1 - score_diff_2
                        best_play = score
            else:
                for score in score_dict:
                    if (score_diff_2 - score_diff_1) > max_impact:
                        max_impact = score_diff_2 - score_diff_1
                        best_play = score
            return best_play
