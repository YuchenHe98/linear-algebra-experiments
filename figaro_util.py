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


def get_all_indices_on_subtree(tree_node):

    res = set()
    if tree_node:
        res.add(tree_node.value)
        for child in tree_node.children:
            res = res.union(get_all_indices_on_subtree(child))
            
    return res


def join_all(tree_node, table_access):

    if not tree_node:
        return pd.DataFrame()
        
    current_index = tree_node.value
    result_table = table_access[current_index]
    
    for child in tree_node.children:
        child_table = join_all(child, table_access)
        common_key = find_key(result_table, child_table)
        result_table = pd.merge(result_table, child_table, on=common_key, how="inner")
            
    return result_table

    
def join_table_with_all_nodes_on_subtree(tree_node, table_access, key_value_map, blocked_nodes=set(), skipped_node=None):

    if not tree_node or tree_node in blocked_nodes:
        return pd.DataFrame()
        
    current_index = tree_node.value

    if tree_node != skipped_node:
        base_table = table_access[current_index]
    else:
        base_table = pd.DataFrame([key_value_map])

    # build mask dynamically
    mask = pd.Series(True, index=base_table.index)
    for col, val in key_value_map.items():
        if col in base_table:
            mask &= (base_table[col] == val)

    result_table = base_table[mask].reset_index(drop=True)
    
    for child in tree_node.children:
        if child in blocked_nodes:
            continue
            
        child_table = join_table_with_all_nodes_on_subtree(child, table_access, key_value_map, blocked_nodes, skipped_node)
        common_key = find_key(result_table, child_table)
        result_table = pd.merge(result_table, child_table, on=common_key, how="inner")
            
    return result_table


def find_key(S1: pd.DataFrame, S2: pd.DataFrame):
    """
    Black-box function to find join key(s) between two DataFrames.
    Replace this with your own logic.
    """
    common = list(set(S1.columns) & set(S2.columns))
    if not common:
        raise ValueError("No common key found between tables")
    return common

                        
def down_result(index, table_access, tree_access, key_value_map):
    current_node = tree_access[index]
    return join_table_with_all_nodes_on_subtree(current_node, table_access, key_value_map)
    
    
def up_result(index, table_access, tree_access, key_value_map):
    root_index = 1
    root = tree_access[root_index]
    current_node = tree_access[index]

    return join_table_with_all_nodes_on_subtree(root, table_access, key_value_map, blocked_nodes={current_node})
    
    
def else_result(index, table_access, tree_access, key_value_map):
    root_index = 1
    root = tree_access[root_index]
    current_node = tree_access[index]

    return join_table_with_all_nodes_on_subtree(root, table_access, key_value_map, blocked_nodes={}, skipped_node=current_node)


def all_result(index, table_access, tree_access):
    current_node = tree_access[index]
    return join_all(current_node, table_access)


def fill_in_data(Data, row_index, column, value):
    """
    Add a value to a DataFrame at (row_index, column).
    Creates the row if it does not exist, filling other columns with 0.
    """
    if row_index not in Data.index:
        Data.loc[row_index] = ["0"] * len(Data.columns)
    Data.loc[row_index, column] = value


