import pandas as pd
from matplotlib import pyplot as plt

import time
from memory_profiler import memory_usage
import algorithms
import levels
from amado import Amado

def metrics(func, game_state, goal_board, *args):
    initial_time = time.time()
    initial_mem = memory_usage(-1, interval=0.01, timeout=1, include_children=True)
    resultado, depth_count = func(game_state, goal_board, *args)
    final_mem = memory_usage(-1, interval=0.01, timeout=1, include_children=True)
    final_time = time.time()
    total_nodes = sum(depth_count.values())    

    print(f"Execution time: {final_time - initial_time:.4f} seconds")
    print(f"Memory used: {max(final_mem) - min(initial_mem):.4f} MiB")
    print(f"Nodes explored by depth: {dict(depth_count)}")
    print(f"Total nodes explored: {total_nodes}\n")
    print("--------------------------------------------------\n")

    return resultado

def main():
    for level in range(1, 11):
        print(f"\n--- Testing algorithms for level {level} ---\n")
        start_board = levels.STARTS.get(level)  
        goal_board = levels.GOALS.get(level) 
    
        row, col = 0, 0  
        game_state = Amado(start_board, row, col) 
        
        test_algorithms = [
            (algorithms.breadth_first_search, [game_state, goal_board]),
            (algorithms.depth_first_search, [game_state, goal_board]),
            (algorithms.depth_limited_search, [game_state, goal_board, 20]), 
            (algorithms.iterative_deepening_search, [game_state, goal_board, 20]),
            (algorithms.greedy_search, [game_state, goal_board]),
            (algorithms.a_star, [game_state, goal_board]),
            (algorithms.a_star, [game_state, goal_board, 1]),  
        ]
        
        for algorithm, args in test_algorithms:
            print(f"Testing {algorithm.__name__}...\n")
            metrics(algorithm, *args)
    
    print("Complete analysis.")

if __name__ == "__main__":
    main()


"""
def create_graphs():
    # Load the results file into a pandas DataFrame
    results_df = pd.read_excel('results.xlsx', sheet_name='Data')

    # Calculate the mean values of the columns you are interested in
    mean_moves = results_df[['DFS_MOVES', 'BFS_MOVES', 'GREEDY_MOVES', 'ASTAR_H2_MOVES']].mean()

    plt.figure()
    # Plot the mean values as a bar graph
    ax1 = mean_moves.plot.bar(figsize=(10, 5))
    ax1.set_xlabel('Algorithms')
    ax1.set_ylabel('Mean Move Count')
    ax1.set_title('Mean Move Count Across All Levels')

    # Update the x-axis labels
    new_labels = ['DFS', 'BFS', 'GREEDY', 'A*']
    ax1.set_xticklabels(new_labels, rotation=0)

    # Calculate the mean values of the columns you are interested in
    mean_time = results_df[['DFS_TIME', 'BFS_TIME', 'GREEDY_TIME', 'ASTAR_H2_TIME']].mean()

    plt.figure()
    # Plot the mean values as a bar graph
    ax2 = mean_time.plot.bar(figsize=(10, 5))
    ax2.set_xlabel('Algorithms')
    ax2.set_ylabel('Execution Time (s)')
    ax2.set_title('Mean Time of Execution Across All Levels')
    ax2.set_xticklabels(new_labels, rotation=0)

    # Calculate the mean values of the columns you are interested in
    mean_visits = results_df[['DFS_VISITS', 'BFS_VISITS', 'GREEDY_VISITS', 'ASTAR_H2_VISITS']].mean()

    plt.figure()
    # Plot the mean values as a bar graph
    ax3 = mean_visits.plot.bar(figsize=(10, 5))
    ax3.set_xlabel('Algorithms')
    ax3.set_ylabel('Node Visits')
    ax3.set_title('Mean Node Visits Across All Levels')
    ax3.set_xticklabels(new_labels, rotation=0)

    mean_mem = results_df[['DFS_MAX_MEM', 'BFS_MAX_MEM', 'GREEDY_MAX_MEM', 'ASTAR_H2_MAX_MEM']].mean()

    plt.figure()
    # Plot the mean values as a bar graph
    ax4 = mean_mem.plot.bar(figsize=(10, 5))
    ax4.set_xlabel('Algorithms')
    ax4.set_ylabel('Nodes Stored in Memory')
    ax4.set_title('Mean Max Memory Usage Across All Levels')
    ax4.set_xticklabels(new_labels, rotation=0)

    mean_times = results_df[['ASTAR_H1_TIME', 'ASTAR_H2_TIME', 'ASTAR_H3_TIME']].mean()

    new_labels2 = ['A* Heuristic 1', 'A* Heuristic 2', 'A* Heuristic 3']
    plt.figure()
    # Plot the mean values as a bar graph
    ax5 = mean_times.plot.bar(figsize=(10, 5))
    ax5.set_xlabel('Algorithms')
    ax5.set_ylabel('Execution Time (s)')
    ax5.set_title('Mean Time of Execution Across All Levels')
    ax5.set_xticklabels(new_labels2, rotation=0)

    mean_moves = results_df[['ASTAR_H1_MOVES', 'ASTAR_H2_MOVES', 'ASTAR_H3_MOVES']].mean()

    plt.figure()
    # Plot the mean values as a bar graph
    ax6 = mean_moves.plot.bar(figsize=(10, 5))
    ax6.set_xlabel('Algorithms')
    ax6.set_ylabel('Mean Move Count')
    ax6.set_title('Mean Move Count Across All Levels')
    ax6.set_xticklabels(new_labels2, rotation=0)

    plt.show()

if __name__ == "__main__":
    #analysis()
    create_graphs()
"""