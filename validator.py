from latest_board_state import latest_board_state


def validator(x, y, quarter, direction):
    """
    input consists of 4 parameters: x,y,quarter,direction
    x, y: the coordinates in which the player wants to put his marble in
    quarter: overall we have 4 squares (3*3) in the board:
        quarter 1: [:3][:3]
        quarter 2: [:3][3:]
        quarter 3: [3:][:3]
        quarter 4: [3:][3:]
    direction: can be +1 or -1 (90 degrees rotation: clockwise or counterclockwise)
    this function checks if the given input is correct and also if the place that player
    wants to put his marble in, is empty
    """

    def validate_x_y():
        if x < 0 or x > 5 or y < 0 or y > 5:
            return False
        return True

    def validate_quarter():
        if quarter not in [1, 2, 3, 4]:
            return False
        return True

    def validate_direction():
        if direction not in [-1, 1]:
            return False
        return True

    def validate_empty_place():
        board = latest_board_state()
        if board[x][y] != 0:
            return False
        return True

    return (
        validate_x_y()
        and validate_quarter()
        and validate_direction()
        and validate_empty_place()
    )
