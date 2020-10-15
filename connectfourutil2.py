import numpy as np

def generate_move(board, player, saved_state):
    """Contains all code required to generate a move,
    given a current game state (board & player)
    Args:
        board (2D np.array):   game board (element is 0, 1 or 2)
        player (int):          your plabyer number (float)
        saved_state (object):  returned value from previous call
     Returns:
        action (int):                   number in [0, 6]
        saved_state (optional, object): will be returned next time
                                        the function is called
     """
    return 0

# print(np.array(b'0'*6))
# print(b'0000000000000100000110011111000111100000000000000')

board = np.array([[b'0'*7]*7])

def get_position_mask_bitmap(board, player):
    position, mask = '', ''
    # Start with right-most column
    for j in range(6, -1, -1):
        # Add 0-bits to sentinel 
        mask += '0'
        position += '0'
        # Start with bottom row
        for i in range(0, 6):
            mask += ['0', '1'][board[i, j] != 0]
            position += ['0', '1'][board[i, j] == player]
    return int(position, 2), int(mask, 2)

# print(board)
# print(board[6, 1])
# for j in range(6, -1, -1):
    # print(j)
# get_position_mask_bitmap(board, 1)