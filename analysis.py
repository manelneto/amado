from amado import Amado
from memory_profiler import memory_usage
import algorithms
import levels
import time
import sys

def metrics(f, args):
    func = (f, args, {})
    initial_time = time.time()
    mem_usage, result = memory_usage(func, include_children = True, retval = True)
    solution, depth_count = result
    final_time = time.time()
    total_nodes = sum(depth_count.values())

    print(f"Execution time: {final_time - initial_time:.4f} seconds")
    print(f"Memory used: {max(mem_usage):.4f} MiB")
    print(f"Nodes explored by depth: {dict(depth_count)}")
    print(f"Total nodes explored: {total_nodes}")
    print(f"Solution found: {len(solution)} movements")
    print("\n--------------------------------------------------\n")

def measure_level(level):
    print(f"\n--- Testing algorithms for level {level} ---\n")
    start_board = levels.STARTS.get(level)
    goal_board = levels.GOALS.get(level)

    game_state = Amado(start_board, 0, 0)
    
    test_algorithms = [
        (algorithms.breadth_first_search, (game_state, goal_board, True)),
        (algorithms.depth_first_search, (game_state, goal_board, True)),
        (algorithms.depth_limited_search, (game_state, goal_board, 20, True)), 
        (algorithms.iterative_deepening_search, (game_state, goal_board, 20, True)),
        (algorithms.greedy_search, (game_state, goal_board, 4, True)),
        (algorithms.a_star, (game_state, goal_board, 1, 4, True)),
        (algorithms.a_star, (game_state, goal_board, 1.7, 4, True)),  
    ]
    
    for algorithm, args in test_algorithms:
        print(f"Testing {algorithm.__name__}...\n")
        metrics(algorithm, args)

def measure_levels():
    for level in range(1, 11):
        measure_level(level)

if __name__ == "__main__":
    args = sys.argv
    n = len(args)
    if n > 1:
        measure_level(int(args[1]))
    else:
        measure_levels()
