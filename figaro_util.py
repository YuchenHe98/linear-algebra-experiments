from functools import reduce
import pandas as pd

class TreeNode:
    def __init__(self, value, parent=None):
        self.value = value               # node's value
        self.parent = parent             # pointer to parent (or None if root)
        self.children = set()            # children stored in a set

        # if parent is provided, add this node to parent's children
        if parent is not None:
            parent.add_child(self)

    def add_child(self, child_node):
        """Add a child to this node."""
        if not isinstance(child_node, TreeNode):
            raise TypeError("child_node must be a TreeNode")
        child_node.parent = self
        self.children.add(child_node)

    def remove_child(self, child_node):
        """Remove a child from this node."""
        if child_node in self.children:
            self.children.remove(child_node)
            child_node.parent = None

    def is_root(self):
        """Check if node is root (no parent)."""
        return self.parent is None

    def is_leaf(self):
        """Check if node is leaf (no children)."""
        return len(self.children) == 0

    def __repr__(self):
        return f"TreeNode(value={self.value})"

    def __hash__(self):
        """Allow TreeNode objects to live in sets (hash by id)."""
        return id(self)

    def __eq__(self, other):
        """Equality is identity-based (same object)."""
        return self is other


def get_all_nodes_on_subtree(tree_node):

    res = set()
    if tree_node:
        res.add(tree_node.value)
        for child in tree_node.children:
            res = res.union(get_all_nodes_on_subtree(child))
            
    return res


def find_key(S1: pd.DataFrame, S2: pd.DataFrame):
    """
    Black-box function to find join key(s) between two DataFrames.
    Replace this with your own logic.
    """
    common = list(set(S1.columns) & set(S2.columns))
    if not common:
        raise ValueError("No common key found between tables")
    return common


def recursive_join(tables):
    """
    Recursively join a list of DataFrames using find_key(S1, S2).
    """
    if len(tables) == 0:
        return pd.DataFrame()   # nothing to join
    if len(tables) == 1:
        return tables[0]
    if len(tables) == 2:
        S1, S2 = tables
        join_cols = find_key(S1, S2)
        return pd.merge(S1, S2, on=join_cols, how="inner")
    else:
        # join first with recursive join of the rest
        S1 = tables[0]
        rest = recursive_join(tables[1:])
        join_cols = find_key(S1, rest)
        return pd.merge(S1, rest, on=join_cols, how="inner")


def join_result(table_access, indices_of_nodes, key_value_map):
    # Example: list of DataFrames
    tables = [table_access[i] for i in indices_of_nodes]
    
    # Join all tables on 'key'    
    joined = recursive_join(tables)
    
    # build mask dynamically
    mask = pd.Series(True, index=joined.index)
    for col, val in key_value_map.items():
        mask &= (joined[col] == val)
    
    filtered = joined[mask].reset_index(drop=True)
    return filtered
    
                        
def down_result(index, table_access, tree_access, key_value_map):
    current_node = tree_access[index]
    nodes_on_subtree = get_all_nodes_on_subtree(current_node)
    
    return join_result(table_access, nodes_on_subtree, key_value_map)
    
    
def up_result(index, table_access, tree_access, key_value_map):
    root_index = 1
    root = tree_access[root_index]
    all_nodes = get_all_nodes_on_subtree(root)
    
    current_node = tree_access[index]
    nodes_on_subtree = get_all_nodes_on_subtree(current_node)    

    upper_nodes = all_nodes - nodes_on_subtree
    
    return join_result(table_access, upper_nodes, key_value_map)

    
def all_result(index, table_access, tree_access, key_value_map):
    root_index = 1
    root = tree_access[root_index]
    all_nodes = get_all_nodes_on_subtree(root)
    all_nodes.remove(index)

    return join_result(table_access, all_nodes, key_value_map)


