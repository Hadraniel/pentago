import numpy as np
import shutil

from latest_board_state import latest_board_state
from validator import validator
from apply_move import apply_move


class Pentago:
    """
    In this class, we initialize our board and save its records
    into .csv file!
    """

    def __init__(self):
        self.flag = 1
        self.size = 6
        self.winner = 0
        self.done = False

    def add_agents(self, a1, a2):
        self.agent_1 = a1
        self.agent_2 = a2

    def play(self):
        # clean the records from previous plays !
        shutil.copyfile("original.hbd", "record.hbd")
        board = latest_board_state()
        while True:
            self.game_over()
            if self.done:
                break
            if self.flag == 1:
                move = self.agent_1.play()
                # if validator(*move):
                #     apply_move(board, 1, *move)
                # else:
                #     while not (validator(*move)):
                #         move = self.agent_1.play()
                self.flag = 2
                apply_move(board, 1, *move)

            else:
                move = self.agent_2.play()
                # if validator(*move):
                #     apply_move(board, 2, *move)
                # else:
                #     while not (validator(*move)):
                #         move = self.agent_2.play()
                self.flag = 1
                apply_move(board, 2, *move)

            self.game_over()
            if self.done:
                break

    def game_over(self):
        """
        Checks whether the game is over or not.
        It also specifies the winner of the game
        at first we check main diagonals(those with the length of 6)
        and then the side ones(their length is 5) !
        """
        board = latest_board_state()
        flipped_board = np.fliplr(board)
        # checking main diagonals
        if (len(set(np.diag(board)[:-1])) == 1 and np.diag(board)[0] != 0) or (
            len(set(np.diag(board)[1:])) == 1 and np.diag(board)[1] != 0
        ):
            if np.diag(board)[1] == 1:
                self.winner = 1
                self.done = True

            elif np.diag(board)[1] == 2:
                self.winner = 2
                self.done = True
            return
        if (
            len(set(np.diag(flipped_board)[:-1])) == 1
            and np.diag(flipped_board)[0] != 0
        ) or (
            len(set(np.diag(flipped_board)[1:])) == 1 and np.diag(flipped_board)[1] != 0
        ):
            if np.diag(flipped_board)[1] == 1:
                self.winner = 1
                self.done = True
            elif np.diag(flipped_board)[1] == 2:
                self.winner = 2
                self.done = True
            return

        # Cheking Rows and Columns
        for row in board:
            if row[-1] == ",":
                row = row[:-1]
            a = row == [1, 1, 1, 1, 1, 1]
            b = row == [0, 1, 1, 1, 1, 1]
            c = row == [1, 1, 1, 1, 1, 0]
            d = row == [2, 1, 1, 1, 1, 1]
            e = row == [1, 1, 1, 1, 1, 2]
            if a.all() or b.all() or c.all() or d.all() or e.all():
                self.winner = 1
                self.done = True

            a = row == [2, 2, 2, 2, 2, 2]
            b = row == [0, 2, 2, 2, 2, 2]
            c = row == [2, 2, 2, 2, 2, 0]
            d = row == [1, 2, 2, 2, 2, 2]
            e = row == [2, 2, 2, 2, 2, 1]
            if a.all() or b.all() or c.all() or d.all() or e.all():
                self.winner = 2
                self.done = True

        for row in board.T:
            if row[-1] == ",":
                row = row[:-1]
            a = row == [1, 1, 1, 1, 1, 1]
            b = row == [0, 1, 1, 1, 1, 1]
            c = row == [1, 1, 1, 1, 1, 0]
            d = row == [2, 1, 1, 1, 1, 1]
            e = row == [1, 1, 1, 1, 1, 2]
            if a.all() or b.all() or c.all() or d.all() or e.all():
                self.winner = 1
                self.done = True

            a = row == [2, 2, 2, 2, 2, 2]
            b = row == [0, 2, 2, 2, 2, 2]
            c = row == [2, 2, 2, 2, 2, 0]
            d = row == [1, 2, 2, 2, 2, 2]
            e = row == [2, 2, 2, 2, 2, 1]
            if a.all() or b.all() or c.all() or d.all() or e.all():
                self.winner = 2
                self.done = True
        # checking side diagonals
        if (len(set(np.diag(board, 1))) == 1 and np.diag(board, 1)[0] != 0) or (
            len(set(np.diag(board, -1))) == 1 and np.diag(board, -1)[0] != 0
        ):
            if np.diag(board, 1)[0] == 1:
                self.winner = 1
                self.done = True
            elif np.diag(board, 1)[0] == 2:
                self.winner = 2
                self.done = True
            return

        if (
            len(set(np.diag(flipped_board, 1))) == 1
            and np.diag(flipped_board, 1)[0] != 0
        ) or (
            len(set(np.diag(flipped_board, -1))) == 1
            and np.diag(flipped_board, -1)[0] != 0
        ):
            if np.diag(flipped_board, 1)[0] == 1:
                self.winner = 1
                self.done = True
            elif np.diag(flipped_board, 1)[0] == 2:
                self.winner = 2
                self.done = True
            return

        if not 0 in board:
            self.winner = "draw"
            self.done = True
            return


board = Pentago()
