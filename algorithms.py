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