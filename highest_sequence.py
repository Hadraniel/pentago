# highest_sequence_count = highest_sequence(board)

# returns the highest length of sequence all same value as the specified value !
def longest_sequence(arr, value):
    tmp = 0
    count = 0
    for i in range(len(arr)):
        if arr[i] == value:
            tmp += 1
        else:
            count = max(count, tmp)
            tmp = 0
    if tmp != 0:
        count = max(count, tmp)
    return count


# returns the longest sequence that exists in the current state of the board of the specified player !
def longest_sequence_in_the_whole_board(board, player_id):
    longest_sequence_count = 0
    sequence = None
    # 6 rows
    for row in range(6):
        sequence = board[row]
        longest_sequence_count = max(
            longest_sequence_count, longest_sequence(sequence, player_id)
        )
    # 6 columns:
    for column in range(6):
        sequence = [board[i][column] for i in range(6)]
        longest_sequence_count = max(
            longest_sequence_count, longest_sequence(sequence, player_id)
        )
    # 6 diagonals (2 main diagonals and 4 side diagonals)

    # 1 - side diagonal
    sequence = [board[i][i + 1] for i in range(5)]
    longest_sequence_count = max(
        longest_sequence_count, longest_sequence(sequence, player_id)
    )
    # 2 - main diagonal
    sequence = [board[i][i] for i in range(6)]
    longest_sequence_count = max(
        longest_sequence_count, longest_sequence(sequence, player_id)
    )
    # 3 - side diagoal
    sequence = [board[i + 1][i] for i in range(5)]
    longest_sequence_count = max(
        longest_sequence_count, longest_sequence(sequence, player_id)
    )

    # and now the other three diagonals

    # 4 - side diagonal
    sequence = [board[i][4 - i] for i in range(5)]
    longest_sequence_count = max(
        longest_sequence_count, longest_sequence(sequence, player_id)
    )
    # 5 - main diagonal
    sequence = [board[i][5 - i] for i in range(6)]
    longest_sequence_count = max(
        longest_sequence_count, longest_sequence(sequence, player_id)
    )
    # 6 - side diagonal
    sequence = [board[i + 1][5 - i] for i in range(5)]
    longest_sequence_count = max(
        longest_sequence_count, longest_sequence(sequence, player_id)
    )

    return longest_sequence_count
