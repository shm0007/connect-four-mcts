Implementation of Connect Four game using Monte Carlo Game Tree search. Both of the Pure Monte Carlo Game Search and Upper Confidence Bound are implemented

## Usage
The program can be executed from the command line. It can be run to generate the next move from a current board, or simulate multiple games.  
To get next move:  
`ConnectFour.py <file_path> <verbosity> <num_simulation>`  
`ConnectFour.py zero.txt None 100`  


To run complete games:  
`ConnectFour.py <file_path> <verbosity> <num_simulation_algo1> <algo1> <num_simulation_algo2> <algo2> <total_games>`  
`ConnectFour.py zero.txt None 100 UCT 100 PMCGS 10`  


