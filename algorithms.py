from amado import Amado 
from collections import deque
from copy import deepcopy

# Goal Test

def goal_test(game_state: Amado, goal_board: list) -> bool:
    return game_state.board == goal_board

# Operators

def move(game_state: Amado, row: int, col: int) -> Amado:
    if game_state.can_move(row, col):
        color1 = game_state.color(game_state.row, game_state.col)
        color2 = game_state.color(row, col)
        board = deepcopy(game_state.board)
        if color1 != color2:
            board[row][col] = game_state.swap(color1, color2)
        return Amado(board, row, col)
    else:
        return game_state

def up(game_state: Amado) -> Amado:
    return move(game_state, game_state.row - 1, game_state.col)

def down(game_state: Amado) -> Amado:
    return move(game_state, game_state.row + 1, game_state.col)

def left(game_state: Amado) -> Amado:
    return move(game_state, game_state.row, game_state.col - 1)

def right(game_state: Amado) -> Amado:
    return move(game_state, game_state.row, game_state.col + 1)

# Child Nodes

def child_game_states(game_state: Amado) -> list:
    new_states = []

    move_up = up(game_state)
    move_down = down(game_state)
    move_left = left(game_state)
    move_right = right(game_state)
    
    if move_up != game_state:
        new_states.append(move_up)
    if move_down != game_state:
        new_states.append(move_down)
    if move_left != game_state:
        new_states.append(move_left)
    if move_right != game_state:
        new_states.append(move_right)

    return new_states


class TreeNode:
    def __init__(self, game_state: Amado, parent = None):
        self.game_state = game_state
        self.parent = parent
        self.children = []
        self.depth = 0

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self
        child_node.depth = self.depth + 1

def breadth_first_search(initial_state: Amado, goal_board: list):
    root = TreeNode(initial_state)
    queue = deque([root])
    visited_states = set([initial_state])

    while queue:
        node = queue.popleft()

        if goal_test(node.game_state, goal_board):
            return get_solution(node)

        for state in child_game_states(node.game_state):
            if state not in visited_states:
                new_node = TreeNode(state, node)
                node.add_child(new_node)
                queue.append(new_node)
                visited_states.add(state)
            
    return None

def depth_first_search(initial_state: Amado, goal_board: list):
    root = TreeNode(initial_state)
    queue = deque([root])
    visited_states = set([initial_state])

    while queue:
        node = queue.popleft()
        
        for state in child_game_states(node.game_state):
            if state not in visited_states:
                new_node = TreeNode(state, node)
                node.add_child(new_node)
                queue.appendleft(new_node)
                visited_states.add(state)

                if goal_test(state, goal_board):
                    return get_solution(new_node)

    return None

def depth_limited_search(initial_state: Amado, goal_board: list, depth_limit: int = 50):
    root = TreeNode(initial_state)
    queue = deque([root])
    visited_states = set([initial_state])

    while queue:
        node = queue.popleft()

        if goal_test(node.game_state, goal_board):
            return get_solution(node)

        if node.depth == depth_limit:
            continue
        
        for state in child_game_states(node.game_state):
            if state not in visited_states:
                new_node = TreeNode(state, node)
                node.add_child(new_node)
                queue.appendleft(new_node)
                visited_states.add(state)

    return None

def iterative_deepening_search(initial_state: Amado, goal_board: list, depth_limit: int = 50):
    for i in range(depth_limit + 1):
        result = depth_limited_search(initial_state, goal_board, i)
        if result:
            return result
    return None

def greedy_search(initial_state: Amado, goal_board: list):
    root = TreeNode(initial_state)
    queue = deque([(root, heuristic(initial_state, goal_board))])
    visited_states = set([initial_state])

    while queue:
        node, value = queue.popleft()

        if goal_test(node.game_state, goal_board):
            return get_solution(node)
        
        child_states = [(state, heuristic(state, goal_board)) for state in child_game_states(node.game_state)]

        for (state, evaluation) in child_states:
            if state not in visited_states:
                new_node = TreeNode(state, node)
                node.add_child(new_node)
                queue.append((new_node, evaluation))
                visited_states.add(state)
        
        queue = deque(sorted(queue, key = lambda element: element[1]))
        
    return None

def a_star(initial_state: Amado, goal_board: list, weight: int = 1):
    root = TreeNode(initial_state)
    queue = deque([(root, heuristic(initial_state, goal_board))])
    visited_states = set([initial_state])

    while queue:
        node, value = queue.popleft()

        if goal_test(node.game_state, goal_board):
            return get_solution(node)

        child_states = [(state, weight * heuristic(state, goal_board) + node.depth + 1) for state in child_game_states(node.game_state)]

        for (state, evaluation) in child_states:
            if state not in visited_states:
                new_node = TreeNode(state, node)
                node.add_child(new_node)
                queue.append((new_node, evaluation))
                visited_states.add(state)

        queue = deque(sorted(queue, key = lambda element: element[1]))

    return None

def get_solution(node: TreeNode):
    print("WINNER!")
    solution = deque([node.game_state])
    i = 0
    while node.parent:
        i += 1
        solution.appendleft(node.parent.game_state)
        node = node.parent
    print(i)
    return solution

def dfs(board: list, row: int, col: int):
    queue = deque([(row, col)])
    group_size = 0

    while queue:
        row, col = queue.popleft()
        board[row][col] = False
        group_size += 1

        if row > 0 and board[row - 1][col]:
            queue.appendleft((row - 1, col))

        if row < len(board) - 1 and board[row + 1][col]:
            queue.appendleft((row + 1, col))

        if col > 0 and board[row][col - 1]:
            queue.appendleft((row, col - 1))

        if col < len(board) - 1 and board[row][col + 1]:
            queue.appendleft((row, col + 1))

    return group_size

def heuristic(game_state: Amado, goal_board: list):
    # MINIMIZAR
    different_squares = 0
    distances = []
    new_board = []
    n_squares = 0

    for row in range(game_state.board_size):
        new_row = []
        for col in range(game_state.board_size):
            if game_state.board[row][col] != goal_board[row][col]:
                different_squares += 1
                distance = abs(game_state.row - row) + abs(game_state.col - col)
                distances.append(distance)
                new_row.append(True)
            else:
                new_row.append(False)

            if game_state.board[row][col] != 'n':
                n_squares += 1
        new_board.append(new_row)

    groups = []
    for row in range(len(new_board)):
        for col in range(len(new_board)):
            if new_board[row][col]:
                groups.append(dfs(new_board, row, col))

    max_group = 0
    if groups:
        max_group = max(groups)

    different_squares /= n_squares
    max_group /= n_squares
    n_groups = len(groups) / n_squares / 2

    p1 = min(different_squares, max_group, n_groups)
    p3 = max(different_squares, max_group, n_groups)
    p2 = different_squares + max_group + n_groups - p1 - p3

    return 0.5 * p1 + 0.3 * p2 + 0.2 * p3
