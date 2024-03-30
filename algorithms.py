from amado import Amado 
from collections import deque
from copy import deepcopy
from collections import defaultdict

# Goal Test

def goal_test(game_state: Amado, goal_board: list) -> bool:
    """
    Checks if the current board state matches the goal state.

    Parameters:
        game_state (Amado): The current game state.
        goal_board (list): The goal state of the board.

    Returns:
        bool: True if the current board state matches the goal state, False otherwise.
    """
    return game_state.board == goal_board

# Operators

def move(game_state: Amado, row: int, col: int) -> Amado:
    """
    Performs a move by changing the color of a piece on the board, if possible.

    Parameters:
        game_state (Amado): The current game state.
        row (int): The row of the piece to move.
        col (int): The column of the piece to move.

    Returns:
        Amado: A new game state after the move, or the same state if the move is not possible.
    """
    if game_state.can_move(row, col):
        color1 = game_state.current_color()
        color2 = game_state.color(row, col)
        board = deepcopy(game_state.board)
        if color1 != color2:
            board[row][col] = ({'r', 'y', 'b'} - {color1, color2}).pop()
        return Amado(board, row, col)
    else:
        return game_state

def up(game_state: Amado) -> Amado:
    """
    Moves the selected piece up on the board, if possible.

    Parameters:
        game_state (Amado): The current game state.

    Returns:
        Amado: A new game state after moving the piece up.
    """
    return move(game_state, game_state.row - 1, game_state.col)

def down(game_state: Amado) -> Amado:
    """
    Moves the selected piece down on the board, if possible.

    Parameters:
        game_state (Amado): The current game state.

    Returns:
        Amado: A new game state after moving the piece up.
    """
    return move(game_state, game_state.row + 1, game_state.col)

def left(game_state: Amado) -> Amado:
    """
    Moves the selected piece left on the board, if possible.

    Parameters:
        game_state (Amado): The current game state.

    Returns:
        Amado: A new game state after moving the piece up.
    """
    return move(game_state, game_state.row, game_state.col - 1)

def right(game_state: Amado) -> Amado:
    """
    Moves the selected piece right on the board, if possible.

    Parameters:
        game_state (Amado): The current game state.

    Returns:
        Amado: A new game state after moving the piece up.
    """
    return move(game_state, game_state.row, game_state.col + 1)

# Child Nodes

def child_game_states(game_state: Amado) -> list:
    """
    Generates all possible child states from the current game state.

    Parameters:
        game_state (Amado): The current game state.

    Returns:
        list: A list containing all possible child states.
    """
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
    """
    Represents a node in the search tree for games.
    
    Attributes:
        game_state (Amado): The game state associated with this node.
        parent (TreeNode, optional): The parent node of this node in the search tree.
        children (list): A list of child nodes.
        depth (int): The depth of this node in the search tree.
    """
    def __init__(self, game_state: Amado, parent = None):
        self.game_state = game_state
        self.parent = parent
        self.children = []
        self.depth = 0

    """
    Adds a child node to this node.
    
    Parameters:
        child_node (TreeNode): The child node to be added.
    """
    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self
        child_node.depth = self.depth + 1

    def __hash__(self):
        return hash((self.game_state, self.depth))
    
    def __eq__(self, other):
        if not isinstance(other, TreeNode):
            return False
        return self.depth == other.depth and self.game_state == other.game_state

def breadth_first_search(initial_state: Amado, goal_board: list) -> tuple | None:
    """
    Performs breadth-first search from an initial state to a goal state.

    Parameters:
        initial_state (Amado): The initial game state.
        goal_board (list): The goal state of the board.

    Returns:
        tuple | None: A tuple containing the solution and search statistics, or None if a solution is not found.
    """
    root = TreeNode(initial_state)
    queue = deque([root])
    visited_states = set([initial_state])
    depth_count = defaultdict(int)

    while queue:
        node = queue.popleft()
        current_state = node.game_state
        depth_count[node.depth] += 1

        if goal_test(current_state, goal_board):
            return get_solution(node), depth_count

        for state in child_game_states(current_state):
            if state not in visited_states:
                new_node = TreeNode(state, node)
                node.add_child(new_node)
                queue.append(new_node)
                visited_states.add(state)
            
    return None, depth_count

def depth_first_search(initial_state: Amado, goal_board: list) -> tuple | None:
    """
    Performs depth-first search from an initial state to a goal state.

    Parameters:
        initial_state (Amado): The initial game state.
        goal_board (list): The goal state of the board.

    Returns:
        tuple | None: A tuple containing the solution path (if found) and search statistics, or None if a solution is not found.
    """
    root = TreeNode(initial_state)
    queue = deque([root])
    visited_states = set([initial_state])
    depth_count = defaultdict(int)

    while queue:
        node = queue.popleft()
        depth_count[node.depth] += 1
        
        for state in child_game_states(node.game_state):
            if state not in visited_states:
                new_node = TreeNode(state, node)
                node.add_child(new_node)
                queue.appendleft(new_node)
                visited_states.add(state)

                if goal_test(state, goal_board):
                    return get_solution(new_node), depth_count

    return None, depth_count

def depth_limited_search(initial_state: Amado, goal_board: list, depth_limit: int) -> tuple | None:
    """
    Performs depth-limited search from an initial state to a goal state, up to a specified depth.

    Parameters:
        initial_state (Amado): The initial game state.
        goal_board (list): The goal state of the board.
        depth_limit (int): The maximum depth for the search.

    Returns:
        tuple | None: A tuple containing the solution path (if found) and search statistics, or None if a solution is not found within the depth limit.
    """
    root = TreeNode(initial_state)
    queue = deque([root])
    visited_nodes = set()
    depth_count = defaultdict(int)

    while queue:
        node = queue.popleft()
        depth_count[node.depth] += 1

        if node.depth == depth_limit or node in visited_nodes:
            continue

        for state in child_game_states(node.game_state):
            new_node = TreeNode(state, node)
            node.add_child(new_node)
            queue.appendleft(new_node)

            if goal_test(state, goal_board):
                return get_solution(new_node), depth_count

        visited_nodes.add(node)

    return None, depth_count

def iterative_deepening_search(initial_state: Amado, goal_board: list, depth_limit: int) -> tuple | None:
    """
    Performs iterative deepening search from an initial state to a goal state. This method incrementally increases the depth limit until the goal is found or the depth limit is reached.

    Parameters:
        initial_state (Amado): The initial game state.
        goal_board (list): The goal state of the board.
        depth_limit (int): The maximum depth limit to reach in iterative deepening.

    Returns:
        tuple | None: A tuple containing the solution path (if found) and aggregated search statistics across all depths, or None if a solution is not found within the depth limit.
    """
    depth_count = defaultdict(int)
    for i in range(depth_limit + 1):
        result = depth_limited_search(initial_state, goal_board, i)
        if result:
            return result
    return None

def greedy_search(initial_state: Amado, goal_board: list, heuristic_num : int = 4) -> tuple | None:
    """
    Performs greedy search from an initial state to a goal state, using a heuristic to prioritize nodes.

    Parameters:
        initial_state (Amado): The initial game state.
        goal_board (list): The goal state of the board.
        heuristic_num (int, optional): The number indicating which heuristic to use for prioritizing nodes.

    Returns:
        tuple | None: A tuple containing the solution path (if found) and search statistics, or None if a solution is not found.
    """
    root = TreeNode(initial_state)
    queue = deque([(root, heuristic(initial_state, goal_board, heuristic_num))])
    visited_states = set([initial_state])
    depth_count = defaultdict(int)

    while queue:
        node, value = queue.popleft()
        current_state = node.game_state
        depth_count[node.depth] += 1

        if goal_test(current_state, goal_board):
            return get_solution(node), depth_count
        
        child_states = [(state, heuristic(state, goal_board, heuristic_num)) for state in child_game_states(current_state)]

        for (state, evaluation) in child_states:
            if state not in visited_states:
                new_node = TreeNode(state, node)
                node.add_child(new_node)
                queue.append((new_node, evaluation))
                visited_states.add(state)
        
        queue = deque(sorted(queue, key = lambda element: element[1]))
        
    return None, depth_count

def a_star(initial_state: Amado, goal_board: list, weight: int = 1, heuristic_num : int = 4) -> tuple | None:
    """
    Performs A* search from an initial state to a goal state. Combines the cost to reach the node and a heuristic estimate of the cost to reach the goal.

    Parameters:
        initial_state (Amado): The initial game state.
        goal_board (list): The goal state of the board.
        weight (int, optional): The weight given to the heuristic component of the cost.
        heuristic_num (int, optional): The number indicating which heuristic to use for estimating the cost to reach the goal.

    Returns:
        tuple | None: A tuple containing the solution path (if found) and search statistics, or None if a solution is not found.
    """
    root = TreeNode(initial_state)
    queue = deque([(root, heuristic(initial_state, goal_board, heuristic_num))])
    visited_states = set([initial_state])
    depth_count = defaultdict(int)

    while queue:
        node, value = queue.popleft()
        current_state = node.game_state
        depth_count[node.depth] += 1

        if goal_test(current_state, goal_board):
            return get_solution(node), depth_count

        child_states = [(state, weight * heuristic(state, goal_board, heuristic_num) + node.depth + 1) for state in child_game_states(current_state)]

        for (state, evaluation) in child_states:
            if state not in visited_states:
                new_node = TreeNode(state, node)
                node.add_child(new_node)
                queue.append((new_node, evaluation))
                visited_states.add(state)

        queue = deque(sorted(queue, key = lambda element: element[1]))

    return None, depth_count

def get_solution(node: TreeNode) -> deque:
    solution = deque([node.game_state])
    i = 0
    while node.parent:
        i += 1
        solution.appendleft(node.parent.game_state)
        node = node.parent
    #print(i) # TODO
    return solution

def visit_group(board: list, row: int, col: int) -> int:
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

def heuristic(game_state: Amado, goal_board: list, choice: int) -> int:
    """
    Calculates the heuristic estimate from the current state to the goal state.

    Parameters:
        game_state (Amado): The current game state.
        goal_board (list): The goal state of the board.
        choice (int): The number indicating the heuristic strategy to be used.

    Returns:
        int: The calculated heuristic value.
    """
    different_squares = 0
    new_board = []
    n_squares = 0

    for row in range(game_state.board_size):
        new_row = []
        for col in range(game_state.board_size):
            if game_state.board[row][col] != goal_board[row][col]:
                different_squares += 1
                new_row.append(True)
            else:
                new_row.append(False)

            if game_state.board[row][col] != 'n':
                n_squares += 1
        new_board.append(new_row)

    if choice == 1:
        return different_squares

    groups = []
    for row in range(game_state.board_size):
        for col in range(game_state.board_size):
            if new_board[row][col]:
                groups.append(visit_group(new_board, row, col))

    different_squares /= n_squares
    n_groups = len(groups)

    if choice == 2:
        return n_groups
    
    max_group = 0
    if groups:
        max_group = max(groups)

    if choice == 3:
        return max_group

    if n_squares < 16:
        return 0.9 * different_squares + 0.1 * n_groups
    return 0.99 * different_squares + 0.01 * n_groups
