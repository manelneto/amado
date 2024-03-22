from amado import Amado 
from collections import deque
from copy import deepcopy

# Goal Test

def goal_test(game_state: Amado, goal_board) -> bool:
    return game_state.board == goal_board

# Operators

def move(game_state: Amado, row: int, col: int) -> Amado:
    current_state = deepcopy(game_state)
    if (current_state.can_move(row, col)):
        color1 = current_state.color(current_state.row, current_state.col)
        color2 = current_state.color(row, col)
        if color1 != color2:
            current_state.board[row][col] = current_state.swap(color1, color2)
        return Amado(current_state.board, row, col)
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
    def __init__(self, game_state: Amado, parent=None):
        self.game_state = game_state
        self.parent = parent
        self.children = []
        self.depth = 0

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self
        child_node.depth = self.depth + 1

def breadth_first_search(initial_state, goal_board):
    root = TreeNode(initial_state)
    queue = deque([root])
    visited_states = set([initial_state])
    
    while queue:
        node = queue.popleft()

        if goal_test(node.game_state, goal_board):
            print("WINNER!")
            print_solution(node)
            return node

        for state in child_game_states(node.game_state):
            if state not in visited_states:
                new_node = TreeNode(state, node)
                node.add_child(new_node)
                queue.append(new_node)
                visited_states.add(state)
            
    return None

def depth_first_search(initial_state, goal_board):
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
                    print("WINNER!")
                    print_solution(new_node) # TODO excede o limite de profundidade de recursão
                    return new_node

    return None

def depth_limited_search(initial_state, goal_board, depth_limit):
    root = TreeNode(initial_state)
    queue = deque([root])
    visited_states = set([initial_state])
    
    while queue:
        node = queue.popleft()

        if goal_test(node.game_state, goal_board):
            print("WINNER!")
            print_solution(node)
            return node

        if node.depth == depth_limit:
            continue
        
        for state in child_game_states(node.game_state):
            if state not in visited_states:
                new_node = TreeNode(state, node)
                node.add_child(new_node)
                queue.appendleft(new_node)
                
    return None

def iterative_deepening_search(initial_state, goal_board, depth_limit):
    for i in range(depth_limit + 1):
        result = depth_limited_search(initial_state, goal_board, i)
        if result:
            return result
    return None

def print_solution(node):
    if node.parent:    
        print_solution(node.parent)
    print(node.game_state, "DEPTH = ", node.depth)
    return
