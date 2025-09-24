from functools import reduce
import pandas as pd
import ast

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


def find_key(S1: pd.DataFrame, S2: pd.DataFrame, impose_join_key=False):
    """
    Black-box function to find join key(s) between two DataFrames.
    Replace this with your own logic.
    """
    common = sorted(list(set(S1.columns) & set(S2.columns)))

    if not common and impose_join_key:
        raise ValueError("No common key found between tables")
    return common


def construct_row_index_dict(index, row, join_key_columns):
    # don't add index for now
    return dict(sorted(row[join_key_columns].to_dict().items()))

def Head(values, vector=None):
    if not vector:
        return f"H({', '.join(values)})"
    else:
        return f"H({', '.join(values)}, {vector})"

def multiply(coefficient, variable):
    return f"{coefficient}*{variable}"


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


def data_projection(df, keys):
    # Parse string index -> dict
    parsed_index = [ast.literal_eval(idx) for idx in df.index]

    # Sort keys to enforce consistent order
    keys = sorted(keys)

    # Extract only subset of dict keys in sorted order
    group_keys = [{k: d[k] for k in keys} for d in parsed_index]

    # Create new temporary column to group by
    group_key_strs = [str(gk) for gk in group_keys]
    df["_group"] = group_key_strs

    # Custom aggregator that builds H_g(...)
    def custom_agg(values):
        return f'H_g({", ".join(values)})'

    grouped = df.groupby("_group").agg(custom_agg)

    # Drop helper column, fix index back to strings
    grouped.index.name = None

    return grouped
    