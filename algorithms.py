from amado import Amado 
from collections import deque
from copy import deepcopy

# Goal Test

def goal_test(game_state: Amado) -> bool:
    return game_state.board == game_state.goal_board

# Operators

def move(game_state: Amado, row: int, col: int) -> Amado:
    current_state = deepcopy(game_state)
    if (current_state.can_move(row, col)):
        color1 = current_state.color(current_state.row, current_state.col)
        color2 = current_state.color(row, col)
        if color1 != color2:
            current_state.board[row][col] = current_state.swap(color1, color2)
        return Amado(current_state.board, current_state.goal_board, current_state.move_counter + 1, row, col)
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

def breadth_first_search(initial_state):
    root = TreeNode(initial_state)   # create the root node in the search tree
    queue = deque([root])   # initialize the queue to store the nodes
    visited_nodes = set()
    
    while queue:
        node = queue.popleft()   # get first element in the queue

        if node.game_state in visited_nodes:
            continue

        print(node.game_state, "DEPTH = ", node.depth)

        visited_nodes.add(node.game_state)

        if goal_test(node.game_state):   # check goal state
            print("------\nWINNER\n------")
            print_solution(node)           
            return node

        for state in child_game_states(node.game_state):   # go through next states
            # create tree node with the new state
            new_node = TreeNode(state, node) # node é o pai
            
            # link child node to its parent in the tree
            node.add_child(new_node)
            
            # enqueue the child node
            queue.append(new_node)
            
    return None

def depth_first_search(initial_state):
    root = TreeNode(initial_state)   # create the root node in the search tree
    queue = deque([root])   # initialize the queue to store the nodes
    visited_nodes = set()
    
    while queue:
        node = queue.popleft()  # get first element in the queue
        
        if (node.game_state) in visited_nodes:
            continue

        visited_nodes.add((node.game_state))
        
        if goal_test(node.game_state):   # check goal state
            print("WINNER!")    
            print(node.game_state.board)
            return node
        
        for state in child_game_states(node.game_state):   # go through next states
            # create tree node with the new state
            newNode = TreeNode(state, node) # node é o pai
            
            # link child node to its parent in the tree
            node.add_child(newNode)
            
            # enqueue the child node
            queue.appendleft(newNode)
            
    return None

def depth_limited_search(initial_state, depth_limit):
    root = TreeNode(initial_state)   # create the root node in the search tree
    queue = deque([root])   # initialize the queue to store the nodes
    visited_nodes = set()
    
    while queue:
        node = queue.popleft()  # get first element in the queue

        if node.depth > depth_limit or node.game_state in visited_nodes:
            continue

        print(node.game_state, "DEPTH = ", node.depth)

        visited_nodes.add(node.game_state)
        
        if goal_test(node.game_state):   # check goal state
            print("------\nWINNER\n------")
            print_solution(node)
            return node
        
        for state in child_game_states(node.game_state):   # go through next states
            # create tree node with the new state
            new_node = TreeNode(state, node) # node é o pai
            
            # link child node to its parent in the tree
            node.add_child(new_node)
            
            # enqueue the child node
            queue.appendleft(new_node)
            
    return None

def iterative_deepening_search(initial_state, depth_limit):
    for i in range(depth_limit):
        result = depth_limited_search(initial_state, i)
        if result:
            return result
    return None

def print_solution(node):
    if node.parent:    
        print_solution(node.parent)
    print(node.game_state)
    return
