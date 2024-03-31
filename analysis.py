from amado import Amado
from memory_profiler import memory_usage
import algorithms
import levels
import time
import sys

def metrics(file, f, args):
    func = (f, args, {})
    initial_time = time.time()
    mem_usage, result = memory_usage(func, include_children = True, retval = True)
    solution, depth_count = result
    final_time = time.time()
    total_nodes = sum(depth_count.values())

    print(f"Execution time: {final_time - initial_time:.4f} seconds", file = file)
    print(f"Memory used: {max(mem_usage):.4f} MiB", file = file)
    print(f"Nodes explored by depth: {dict(depth_count)}", file = file)
    print(f"Total nodes explored: {total_nodes}", file = file)
    print(f"Solution found: {len(solution) - 1} movements", file = file)
    print("\n--------------------------------------------------\n", file = file)

def measure_level(level):
    print(f"\n--- Started measurements for level {level} ---\n")

    start_board = levels.STARTS.get(level)
    goal_board = levels.GOALS.get(level)

    game_state = Amado(start_board, 0, 0)
    
    test_algorithms = [
        (algorithms.breadth_first_search, (game_state, goal_board, True)),
        (algorithms.depth_first_search, (game_state, goal_board, True)),
        (algorithms.depth_limited_search, (game_state, goal_board, 20, True)), 
        (algorithms.iterative_deepening_search, (game_state, goal_board, 20, True)),
        (algorithms.greedy_search, (game_state, goal_board, 4, True)),
        (algorithms.a_star, (game_state, goal_board, 1, 1, True)),
        (algorithms.a_star, (game_state, goal_board, 2, 1, True)),  
    ]

    file = open("level" + str(level) + ".txt", "a")

    for algorithm, args in test_algorithms:
        print(f"Testing {algorithm.__name__}...\n", file = file)
        metrics(file, algorithm, args)

    file.close()

    print(f"\n--- Completed measurements for level {level} ---\n")

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
