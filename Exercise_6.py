# PART 1: Traverse a tree depth-first, in-order (recursively and iteratively)

"""
Create TreeNode class which represents a single node in the binary tree.
param:  value: A string, like "A" or "+".
        left: A reference to the left child (another TreeNode or None).
        right: A reference to the right child (another TreeNode or None).
__init__: The class has no behavior, only state -> it's only a data container.
"""
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None # meaning the node starts with no children
        self.right = None # meaning the node starts with no children

# Printing the value of the node being visited during traversal.
def visit(node: TreeNode):
    if node:
        print(f"Visiting {node.value}")

# Function for traversing the given node and its children recursively -> Visits nodes in the order: left → current → right
def traverse_recursively_in_order(node: TreeNode):
    """
    Recursive variant: it implicitly "remembers" the current node and state

    Step-by-Step:
        - If the current node is None, stop recursion.
        - Recursively call the function on the left child.
        - Visit the current node (e.g., print its value).
        - Recursively call the function on the right child.
    """
    if node:
        traverse_recursively_in_order(node.left)  # Visit the left subtree
        visit(node)  # Visit the current node
        traverse_recursively_in_order(node.right)  # Visit the right subtree


# Function for traverse the node and its children iteratively -> Simulates recursion using a stack to keep track of nodes.
def traverse_iteratively_in_order(node: TreeNode):
    """
    Iterative variant: uses an explicit stack to mimic the behavior of recursion
    --> The stack keeps track of the nodes that need to be processed later, ensuring the same sequence as the recursive approach.

    Stack:
        - A stack is a Last In, First Out (LIFO) data structure.
        - Nodes are added to the stack using append and removed using pop.
        - The stack helps keep track of nodes while exploring a tree, especially when temporarily moving to the left subtree.

    Why "pop" used:
    When implementing an iterative traversal, the stack serves as a substitute for the recursive function
    call stack. pop allows us to backtrack to previously visited nodes.

    Step-by-Step:
        - Start with the root node.
        - Traverse down to the leftmost node, adding nodes to the stack.
        - Once there’s no left child, backtrack (pop from the stack).
        - Visit the node and move to its right child.
    """
    if node:
        stack = [] # to keep track of nodes
        current = node

        while stack or current:
            while current:  # Go as left as possible
                stack.append(current)
                current = current.left

            current = stack.pop()  # Backtrack to the last visited node
            visit(current)  # Visit the current node
            current = current.right  # Move to the right child


# Example tree:
root = TreeNode("+")
root.left = TreeNode("*")
root.left.left = TreeNode("A")
root.left.right = TreeNode("-")
root.left.right.left = TreeNode("B")
root.left.right.right = TreeNode("C")
root.right = TreeNode("+")
root.right.left = TreeNode("D")
root.right.right = TreeNode("E")

print("Recursive In-Order Traversal:")
traverse_recursively_in_order(root)

print("\nIterative In-Order Traversal:")
traverse_iteratively_in_order(root)

# The expected output for both:  A, *, B, -, C, +, D, +, E


# PART 2: Traverse a tree depth-first using OOP, in-order (only recursively!)
# NOTE: The code from the Part 1 is rewritten here into a new class in order to see two different approaches
class TreeNodeOOP:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    # Method for IN-ORDER traversal
    def traverse_in_order(self, visitor):
        if self.left:
            self.left.traverse_in_order(visitor)  # Traverse left subtree
        visitor(self)                             # Visit current node
        if self.right:
            self.right.traverse_in_order(visitor) # Traverse right subtree

    # Method for PRE-ORDER traversal
    def traverse_pre_order(self, visitor):
        visitor(self)                             # Visit current node first
        if self.left:
            self.left.traverse_pre_order(visitor) # Traverse left subtree
        if self.right:
            self.right.traverse_pre_order(visitor) # Traverse right subtree

    # Method for POST-ORDER traversal
    def traverse_post_order(self, visitor):
        if self.left:
            self.left.traverse_post_order(visitor) # Traverse left subtree
        if self.right:
            self.right.traverse_post_order(visitor) # Traverse right subtree
        visitor(self)

# Function visit is exactly the same

# Examples tree using OOP approach:
# Example tree construction for Part 2
root_oop = TreeNodeOOP("+")
root_oop.left = TreeNodeOOP("*")
root_oop.left.left = TreeNodeOOP("A")
root_oop.left.right = TreeNodeOOP("-")
root_oop.left.right.left = TreeNodeOOP("B")
root_oop.left.right.right = TreeNodeOOP("C")
root_oop.right = TreeNodeOOP("+")
root_oop.right.left = TreeNodeOOP("D")
root_oop.right.right = TreeNodeOOP("E")

print("In-Order Traversal:")
root_oop.traverse_in_order(visit) # expected output: A, *, B, -, C, +, D, +, E

print("\nPre-Order Traversal:")
root_oop.traverse_pre_order(visit) # expected output: +, *, A, -, B, C, +, D, E

print("\nPost-Order Traversal:")
root_oop.traverse_post_order(visit) # expected output: A, B, C, -, *, D, E, +, +


# New example tree
new_root = TreeNodeOOP("M")
new_root.left = TreeNodeOOP("L")
new_root.right = TreeNodeOOP("N")
new_root.left.left = TreeNodeOOP("J")
new_root.left.right = TreeNodeOOP("K")
new_root.right.right = TreeNodeOOP("P")
new_root.left.right.left = TreeNodeOOP("A")
new_root.left.right.right = TreeNodeOOP("B")

print("\nIn-Order Traversal:")
new_root.traverse_in_order(visit)

print("\nPre-Order Traversal:")
new_root.traverse_pre_order(visit)

print("\nPost-Order Traversal:")
new_root.traverse_post_order(visit)