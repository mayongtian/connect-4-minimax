def connect_four_ab(contents : str, turn : str, max_depth : int):
    """
    Copied directly from minimax
    """
    state = vectorize_input(contents)
    player = 1 if turn.lower() == "red" else -1

    best_column, nodes_explored, _ = ab_pruning(state, player, max_depth, 0, float("-inf"), float("inf"))
    return f"{best_column}\n{nodes_explored}"

def ab_pruning(state: list[list[int]], player: int, max_depth: int, depth, alpha=float("-inf"), beta=float("inf")) -> tuple[int, int,int]:
    """
    Implements the Minimax algorithm to determine the best column to play in.

    :param state: The current board state (column-major: list of 7 columns, each of length 6).
    :param player: The current player (1 for red, -1 for yellow).
    :param max_depth: The maximum depth to search.
    :param depth: The current recursion depth.
    :return: A tuple (best_move, nodes_explored, value), where:
        - best_move is the best column (int) to play (or None if terminal).
            - NOTE: most of the time we don't care about the best_move until the final recursion, which is why its mostly not used until the end. Might cause issue for alpha beta
        - nodes_explored is the total number of nodes explored in this subtree.
        - value is the evaluation value for the state.
    """

    nodes_explored = 0
    
    #BASE CASE 1: Check if someone won
    utility = UTILITY(state)
    if utility != 0:
        return (None, nodes_explored, utility)
    #BASE CASE 2: Check if reached max depth
    if depth == max_depth:
        return (None, nodes_explored,EVALUATION(state))
    
    #Generate valid moves
    valid_moves = generate_child_states(state, player)
    #no valid moves
    if not valid_moves:
        return (None, nodes_explored, EVALUATION(state))
    
    # Logic for exploring gamestate
    isMax = (player == 1)
    best_value = -float('inf') if isMax else float('inf')
    best_move = None
    
    for child_state, col in valid_moves:
        # recursion
        _, count_nodes, child_value = ab_pruning(child_state, -player, max_depth, depth + 1, alpha, beta)
        nodes_explored += count_nodes

        # pruning
        if (isMax and alpha >= child_value) or (not isMax and beta <= child_value):
            nodes_explored = 1
        else:
            break
        
        # Logic 
        if isMax and child_value > best_value:
            best_value = child_value
            alpha = max(alpha, best_value)
            best_move = col
        elif not isMax and child_value <best_value:
            best_value = child_value
            beta = min(beta, best_value)
            best_move = col
    
    return best_move, nodes_explored, best_value 

def vectorize_input(state: str) -> list[list[int]]:
    """
    Convert a Connect Four board string into a 2D list of integers.
    We assume:
      - '.' means empty (0)
      - 'r' or 'R' means Red (1)
      - 'y' or 'Y' means Yellow (-1)
    returns: a 2d array where its column-major i.e state[column][row] where:
      - row 0 is where the bottom is, left to right is 0-6 for column 
    """
    # Split the state string by commas to get each row
    rows = state.split(',')
    
    #generates Column-major 2d array: 7 columns x 6 rows
    board_2d = [[0] * 6 for _ in range(7)]
    
    #fill it in 
    num_row = 0
    for row in rows:
        num_column = 0
        for char in row:
            if char.lower() == 'r':
                board_2d[num_column][num_row] = 1
            elif char.lower() == 'y':
                board_2d[num_column][num_row] = -1
            else:
                board_2d[num_column][num_row] = 0
            num_column += 1
        num_row += 1 
    
    return board_2d

def generate_child_states(state:list[list[int]], player: int) -> list[list[list[int]]]:
    """
    Generates all valid moves given a state
    
    param: board state, player move 
    return: tuple (list[states], move)
      - list: a list containing 0-7 board states, if there is no valid moves for that row, it will contain a -1
      - int: column the tile was placed into
    """
    #if there is now valid moves return 
    child_states = []

    #logic for generating child states
    for column in range(7):
        #check if the row is full, if it is continue
        if state[column][5] != 0: 
            continue
        # otherwise, find the lowest empty row, and return a new deep copy 
        for row in range(6):
            if state[column][row] == 0:
                # this should be a deep copy. ??? what does this mean
                # new_state = [column[:] for column in state] 
                new_state = [list(col) for col in state]
                new_state[column][row] = player
                child_states.append((new_state,column))
                break

    return child_states

def UTILITY(state):
    #red is winner
    if NUM_IN_A_ROW(4, state, 1) > 0:
        return 10000
    #yellow is winner
    if NUM_IN_A_ROW(4, state, -1) > 0 :
        return -10000
    return 0

def NUM_IN_A_ROW(count: int, state: list[list[int]], player: int):
    """
    Helper function for Utility to find the winner, provided implementation takes too long for ED test cases 
    
    Parameters:
        count (int): The length of the sequence to look for (e.g., 2, 3, or 4).
        state ([[int]]): The board state as a 2D list in column-major order.
        player (int): The player's token (1 for red, -1 for yellow).
        
    Returns:
        int: The total number of occurrences where the player has 'count' in a row.
    """
    num_rows = 6
    num_columns =7
    total_matches = 0

    #check each column
    for col in range(num_columns):
        #max starting position
        for start_row in range(num_rows - count + 1):
            #count number of possibilities
            if all(state[col][start_row + offset] == player for offset in range(count)):
                total_matches+= 1
    
    # check each row
    for start_col in range(num_columns - count + 1):
        for row in range(num_rows):
            if all(state[start_col + offset][row] == player for offset in range(count)):
                total_matches += 1
    
    #  from left to right column, check each row diagonally from bottom-left to top right
    for start_col in range(num_columns - count + 1):
        for start_row in range(num_rows - count + 1):
            # starts (0,0), (1,1) ...., then 
            if all(state[start_col + offset][start_row + offset] == player for offset in range(count)):
                total_matches += 1

     #  from left to right column, check each row diagonally from top left to bottom right
    for start_col in range(num_columns - count + 1):
        for start_row in range(count - 1, num_rows):
            if all(state[start_col + offset][start_row - offset] == player for offset in range(count)):
                total_matches += 1
    
    return total_matches

def EVALUATION(board):
    """
    Actual logic for evaluating the score at each node, kind of gave up on this part, 
    but basically this one considers whether there is a contiguous sequence already
    and not overcount (i.e a 3 in a row should not also count for two 2 in a row)
    Params:
        board (_type_): 2d array

    Returns: value of the evaluation, it is red evaluation - yellow evaluation
        - int: score
    """
    # Initialize score accumulators for red and yellow
    red_score = 0
    yellow_score = 0
    # Directions for (up, down, diagonal up - right, diagonal down- right)
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    
    # Logic for counting
    for col in range(len(board)):
        for row in range(len(board[0])):
            piece = board[col][row]
            #skip if the cell is empty
            if piece == 0:
                continue
            
            # Directions for column and row, dc and dr respectively
            for dc, dr in directions:
                # Only count if this cell is the start of a new sequence in this direction.
                # That is, check if the previous cell in this direction is either off-board or not the same color.
                prev_col = col - dc
                prev_row = row - dr
                if (0 <= prev_col < len(board) and 
                    0 <= prev_row < len(board[0]) and 
                    board[prev_col][prev_row] == piece):
                    continue  # This cell is not the start of the chain
                
                # Count the contiguous pieces in the current direction
                length = 0
                current_col = col
                current_row = row
                while (0 <= current_col < len(board) and 
                       0 <= current_row < len(board[0]) and 
                       board[current_col][current_row] == piece):
                    length += 1
                    current_col += dc
                    current_row += dr
                
                # Logic for determining the points
                if length == 1:
                    score = 1
                elif length == 2:
                    score = 10
                elif length == 3:
                    score = 100
                else:
                    score = 1000
                
                # Accumulate the score for the appropriate player
                if piece == 1:
                    red_score += score
                elif piece == -1:
                    yellow_score += score

    return red_score - yellow_score
    

if __name__ == '__main__':
    # Example function call below, you can add your own to test the connect_four_mm function
    print(connect_four_ab(".ryyrry,.rryry.,..y.r..,..y....,.......,.......", "red", 4))


