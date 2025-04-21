import sys
import random
import math
import copy
import time
index = 0
#Board will update from the file
board = [['O'] * 7 for _ in range(6)]
move_list = []
class Node:
    def __init__(self, parent=None, move=None, player='Y',ind=0):
        self.parent = parent
        self.move = move
        self.player = player
        self.children = [None for _ in range(7)]
        self.wins = 0
        self.visits = 0
        self.ind = ind

    # Best move based on win/visits ration   
    def best_move_UR(self):
        best_move = 0
        max_val = -100000
        min_val = 100000
        for i in range(7):
            if self.children[i] == None:
                continue
            
            if self.player == 'Y':
                if self.children[i].wins/self.children[i].visits > max_val:
                    max_val = self.children[i].wins/self.children[i].visits
                    best_move = i
            else:
                if self.children[i].wins/self.children[i].visits < min_val:
                    min_val = self.children[i].wins/self.children[i].visits
                    best_move = i
        return best_move


def read_board(filename):
    global board
    """Reads the board state from a file."""
    with open(filename, 'r') as file:
        algorithm = file.readline().strip()
        player = file.readline().strip()
        board = [list(file.readline().strip()) for _ in range(6)]
    return algorithm, player

def get_legal_moves():
    global board
    """Returns a list of legal moves (columns that are not full)."""
    return [col for col in range(7) if board[0][col] == 'O']

def make_move( move, player):
    global board
    global move_list
    """Drops a piece in the specified column."""
    for row in reversed(range(6)):
        if board[row][move] == 'O':
            board[row][move] = player
            break
    move_list.append(move)
    return 
def undo_move():
    global board
    global move_list
    move = move_list[-1] # last move

    for row in (range(6)):
        if board[row][move] != 'O':
            board[row][move] = 'O'
            break
    move_list.pop()
    return 


def check_winner():
        """Checks if there is a winner. Returns 1 if 'Y' wins, -1 if 'R' wins, 0 if draw, None if game should continue."""
        global board
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Vertical, horizontal, diagonal
        for row in range(6):
            for col in range(7):
                if board[row][col] == 'O':
                    continue
                player = board[row][col]
                for dr, dc in directions:
                    count = 0
                    for i in range(4):
                        r, c = row + dr * i, col + dc * i
                        if 0 <= r < 6 and 0 <= c < 7 and board[r][c] == player:
                            count += 1
                        else:
                            break
                    if count == 4:
                        return 1 if player == 'Y' else -1
        
        if all(board[0][col] != 'O' for col in range(7)):
            return 0  # Draw
        
        return None  # Game not over 
def print_board(board):
    
    for i in range(len(board)):
        print(board[i])
    print("")

def backpropagate(node, result,loglevel):
    """Backpropagates the result up the tree, updating wins and visits."""
    while node is not None:
        node.visits =  node.visits + 1
        node.wins+=result
        if(loglevel == 2):
            print("Updated Values: ")
            print("wi: ",node.wins)
            print("ni: ",node.visits)
        node = node.parent
        if node is not None: 
            undo_move()

    
def mcts( player, simulations, loglevel,algorithm):
    """Performs both Pure Monte Carlo Tree Search and UCT"""
    global index
    global board
    global move_list

    root = Node( player=player,ind=index)
    index+=1
    for _ in range(simulations):
        node = root
        while True:
            legal_moves = get_legal_moves()
            if not legal_moves:
                result = 0  # Draw
                break
            move = None
            if algorithm == "PMCGS": #random rollout
                move = random.choice(legal_moves)
            elif algorithm.startswith("UCT"): 
                max_reward = -1000000
                min_reward = 1000000
                unexplored_moves = [i for i in legal_moves if node.children[i] is None]
                if len(unexplored_moves) != 0: #not all moves explroed, random rollout
                    move = random.choice(unexplored_moves)
                else:  
                    for i in legal_moves:
                        if node.player =='Y':
                            #UCT Reward
                            reward = node.children[i].wins /node.children[i].visits +  1.4 * math.sqrt(math.log(node.visits) / node.children[i].visits)

                            if reward >= max_reward:
                                move = i
                                max_reward = reward
                        if node.player == 'R':
                             #UCT Reward
                            reward = node.children[i].wins /node.children[i].visits -  1.4 * math.sqrt(math.log(node.visits) / node.children[i].visits)
                            if reward < min_reward:
                                move = i
                                min_reward = reward
                #print(len(unexplored_moves), move)
                
            else:
                print("Invalid Algo")
                return
            if(loglevel==2):
                print("wi ",node.wins)
                print("ni ",node.visits)
                print("Move Selected ",move+1)
            
            make_move(move,node.player)
            #print_board(new_board)
            if node.children[move] is None:
                new_child =  Node( parent=node, move=move, player='Y' if node.player == 'R' else 'R',ind=index)
                if(loglevel==2):
                    print("Node Added")
                index+=1
                node.children[move] = new_child
            else:
                new_child = node.children[move]
            node = new_child  # Move to new node
            winner =  check_winner()
            

            if winner is not None:
                #print_board(board)
                #print(winner)
                if(loglevel==2):
                    print("TERMINAL NODE VALUE:",winner)
                result = winner
                break
        # Backpropagation and update values of wins and visits
        backpropagate(node, result,loglevel)
            

    if(loglevel >=1): # print for both Verbose and Brief
        for col in range(len(root.children)):
            if root.children[col] is not None:
                print(f"Column {col+1}: {root.children[col].wins/root.children[col].visits }")
            else:
                print(f"Column {col+1}: Null")

    #Additional check for UCT-Modification
    if algorithm == "UCT-MODIFIED" :
        legal_moves = get_legal_moves()
        for m in legal_moves:
            make_move(m,'Y' if player == 'R' else 'R')
            if check_winner():
                
                print(f"Player {player} FINAL Move selected: {m + 1}, unless opponet wins")
                undo_move()
                print_board(board)
                
                return m
            undo_move()

    # Select best move
    best_move = root.best_move_UR()
    if(loglevel>=1):
        print(f"FINAL Move selected: {best_move + 1}")
    return best_move

def get_next_move(algo,player,param,loglevel):
    global board
    if(algo == "UR"):
        return random.choice(get_legal_moves())
    return mcts( player,param,loglevel,algo)
    
def play_random_game(loglevel,algo1,algo2,num_sim_1, num_sim_2, game_count):
    """Plays full games game_count times"""

    global board
    global move_list

    p1_win = 0
    p2_win = 0
    draw = 0
    original_board = [row[:] for row in board]
    start_time = time.time() 

    for i in range(game_count):
        board = [row[:] for row in original_board] # For each game        
        player = 'Y'
        while True:
            legal_moves = get_legal_moves()
            if not legal_moves:
                print("Game ended in a draw.")
                draw+=1
                break
            move = get_next_move(algo1 if player == 'Y' else algo2, player,num_sim_1  if player == 'Y' else num_sim_2,loglevel)
                

            make_move( move, player)
            if loglevel >=1 :       
                print(f"Player {player} selects column {move + 1}")
                print_board(board)
            if check_winner():
                print(f"Player {player} wins!")
                print_board(board)
                if player == 'Y':
                    p1_win+=1
                else:
                    p2_win+=1
                break
            player = 'Y' if player == 'R' else 'R'
        print(f"-----{algo1}({num_sim_1})  vs {algo2}({num_sim_2})---")
        print(f"Player 1({algo1}): wins {p1_win} times")
        print(f"Player 2({algo2}): wins {p2_win} times")
        print(f"Draw {draw} times")
    
    end_time = time.time() 
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.6f} seconds")

def main():
    """Main function to execute the script."""
    if len(sys.argv) < 4:
        print("Usage: python PA2.py <filename> <verbosity> <num_simulation>")
        return
    filename, verbosity, num_simulations = sys.argv[1], sys.argv[2], int(sys.argv[3])
    log_level = 0 if verbosity == "None" else 1 if verbosity == "Brief" else 2
    algorithm, player = read_board(filename)
    
    if(len(sys.argv) > 4): # For Complete games in round robin tournament
        num_simulations_1 = num_simulations
        algo1 = sys.argv[4]
        num_simulations_2 = int(sys.argv[5])
        algo2 = sys.argv[6]
        game_count =  int(sys.argv[7]) 
        play_random_game(log_level,algo1,algo2,num_simulations_1,num_simulations_2,game_count)
        return
    if algorithm == "UR":
        move = random.choice(get_legal_moves())
        print(f"Final Move selected: {move + 1}")
    elif algorithm == "PMCGS" or algorithm == "UCT":
        mcts( player, num_simulations, log_level,algorithm)
    else:
        print("Unsupported algorithm.")

if __name__ == "__main__":
    main()

