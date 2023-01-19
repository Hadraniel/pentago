import numpy as np


def latest_board_state():
    """
    this function simply gets last row of our csv file
    and converts it to a 2d numpy array and then returns it!
    which means that it gives us the latest state of the board!
    note : run board.py before running this one ! csv file gotta be initialized!
    """
    f = open("record.hbd")
    history = f.readlines()
    array = list(map(int, (history[-1].split(","))[:-1]))
    array = np.array(array)
    return np.reshape(array, (-1, 6))
