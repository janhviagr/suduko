import numpy as np
import random

def val(level):
    base = np.random.permutation(np.arange(1, 10)) #create the first random row based off of which we'll create the other rows
    global final_board
    #Sudoku values
    final_board = np.array([
        base,
        np.roll(base, -3),
        np.roll(base, -6),
        np.roll(base, -1),
        np.roll(base, -4),
        np.roll(base, -7),
        np.roll(base, -2),
        np.roll(base, -5),
        np.roll(base, -8)
    ])    #creates the sudoku values .roll(array, shift) does a circular shift so that none of the values are lost/repeated
        #-ve means shift left +ve means right shift
    orignal_board = final_board.copy()
    if level == "Easy":
        remove_count = 45
    elif level == "Medium":
        remove_count = 50
    elif level == "Hard":
        remove_count = 64
    

    play_board=board(final_board,remove_count)

    return orignal_board,play_board

    
def board(final_board, remove_count):
    removed = set()

    while len(removed) < remove_count:
        r = random.randint(0, 8)
        c = random.randint(0, 8)

        if (r, c) not in removed:
            final_board[r, c] = 0
            removed.add((r, c))

    return final_board.tolist()  # Convert to list of lists for easier handling

        
