from amado import Amado 

def move(game_state: Amado, row: int, col: int) -> Amado:
    if (game_state.can_move(row, col)):
        color1 = game_state.color(game_state.row, game_state.col)
        color2 = game_state.color(row, col)
        if color1 != color2:
            game_state.board[row][col] = game_state.swap(color1, color2)
        return Amado(game_state.board, game_state.goal_board, game_state.move_counter + 1, row, col)
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

# A generic definition of a tree node holding a state of the problem
class TreeNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.depth = 0

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self
        child_node.depth = self.depth + 1

from collections import deque

def breadth_first_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)   # create the root node in the search tree
    queue = deque([root])   # initialize the queue to store the nodes
    
    while queue:
        node = queue.popleft()   # get first element in the queue
        if goal_state_func(node.state):   # check goal state
            return node
        
        print(node.state.b1, node.state.b2)

        for state in operators_func(node.state):   # go through next states
            # create tree node with the new state
            newNode = TreeNode(state, node) # node é o pai
            
            # link child node to its parent in the tree
            node.add_child(newNode)
            
            # enqueue the child node
            queue.append(newNode)
            
    return None

def depth_first_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)   # create the root node in the search tree
    queue = deque([root])   # initialize the queue to store the nodes
    visitedNodes = set()
    
    while queue:
        node = queue.popleft()  # get first element in the queue
        
        if (node.state.b1, node.state.b2) in visitedNodes:
            continue

        visitedNodes.add((node.state.b1, node.state.b2))
        
        if goal_state_func(node.state):   # check goal state
            return node
        
        for state in operators_func(node.state):   # go through next states
            # create tree node with the new state
            newNode = TreeNode(state, node) # node é o pai
            
            # link child node to its parent in the tree
            node.add_child(newNode)
            
            # enqueue the child node
            queue.appendleft(newNode)
            
    return None

def depth_limited_search(initial_state, goal_state_func, operators_func, depth_limit):
    root = TreeNode(initial_state)   # create the root node in the search tree
    queue = deque([root])   # initialize the queue to store the nodes
    visitedNodes = set()
    
    while queue:
        node = queue.popleft()  # get first element in the queue

        print(node.state.b1, node.state.b2)

        if node.depth > depth_limit:
            break
        
        if (node.state.b1, node.state.b2) in visitedNodes:
            continue

        visitedNodes.add((node.state.b1, node.state.b2))
        
        if goal_state_func(node.state):   # check goal state
            return node
        
        for state in operators_func(node.state):   # go through next states
            # create tree node with the new state
            newNode = TreeNode(state, node) # node é o pai
            
            # link child node to its parent in the tree
            node.add_child(newNode)
            
            # enqueue the child node
            queue.appendleft(newNode)
            
    return None

def iterative_deepening_search(initial_state, goal_state_func, operators_func, depth_limit):
    for i in range(depth_limit):
        result = depth_limited_search(initial_state, goal_state_func, operators_func, i)
        if result:
            return result
    return None