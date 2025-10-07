from functools import reduce
import pandas as pd
import ast 
from figaro_util import TreeNode
ROOT_INDEX = 1

# three node example #
#####################################################
#####################################################
#####################################################
#####################################################

s1 = TreeNode(1)

s2 = TreeNode(2, parent=s1)

s3 = TreeNode(3, parent=s2)

three_node_tree_v1 = {
    1: s1,
    2: s2,
    3: s3
}

three_node_table_access_v1 = {
    1: pd.DataFrame({"Y1":["a1", "a2"], "X1,2":["b1", "b2"]}),
    2: pd.DataFrame({"X1,2":["b1", "b2", "b2"], "Y2":["10", "20", "30"], "X2,3":["c1", "c1", "c1"]}),
    3: pd.DataFrame({"X2,3":["c1", "c1"], "Y3":["d1", "d2"]})
}


# create root
#####################################################
#####################################################
#####################################################
#####################################################

s1 = TreeNode(1)

s2 = TreeNode(2, parent=s1)

s3 = TreeNode(3, parent=s1)


three_node_tree_v2 = {
    1: s1,
    2: s2,
    3: s3
}

three_node_table_access_v2 = {
    1: pd.DataFrame({"X1,2":["b1", "b2", "b2"], "Y1":["10", "20", "30"], "X1,3":["c1", "c1", "c1"]}),
    2: pd.DataFrame({"Y2":["a1", "a2"], "X1,2":["b1", "b2"]}),
    3: pd.DataFrame({"X1,3":["c1", "c1"], "Y3":["d1", "d2"]})
}

# create root
#####################################################
#####################################################
#####################################################
#####################################################

s1 = TreeNode(1)

s2 = TreeNode(2, parent=s1)

s3 = TreeNode(3, parent=s2)

# add another child explicitly
print(s1.children)
print(s2.children)
print(s3.children)

three_node_tree_v3 = {
    1: s1,
    2: s2,
    3: s3
}

three_node_table_access_v3 = {
    1: pd.DataFrame({"X1,2":["c1", "c1"], "Y1":["d1", "d2"]}),
    2: pd.DataFrame({"X2,3":["b1", "b2", "b2"], "Y2":["10", "20", "30"], "X1,2":["c1", "c1", "c1"]}),
    3: pd.DataFrame({"Y3":["a1", "a2"], "X2,3":["b1", "b2"]}),
}


# create root
#####################################################
#####################################################
#####################################################
#####################################################

s1 = TreeNode(1)

s2 = TreeNode(2, parent=s1)

s3 = TreeNode(3, parent=s2)

s4 = TreeNode(4, parent=s2)


# add another child explicitly
print(s1.children)
print(s2.children)
print(s3.children)
print(s4.children)


four_node_four_rows_tree_v1 = {
    1: s1,
    2: s2,
    3: s3,
    4: s4
}

four_node_four_rows_table_access_v1 = {
    1: pd.DataFrame({"X1,2":["b1", "b2"], "Y1":["a1", "a2"]}),
    2: pd.DataFrame({"X1,2":["b1", "b2", "b2", "b2"], "Y2":["10", "20", "30", "40"], "X2,3":["c1", "c1", "c1", "c2"], "X2,4":["d1", "d1", "d1", "d1"]}),
    3: pd.DataFrame({"Y3":["e1", "e2"], "X2,3":["c1", "c2"]}),
    4: pd.DataFrame({"Y4":["f1"], "X2,4":["d1"]})
}


# create root
#####################################################
#####################################################
#####################################################
#####################################################

s1 = TreeNode(1)

s2 = TreeNode(2, parent=s1)

s3 = TreeNode(3, parent=s2)

s4 = TreeNode(4, parent=s2)


# add another child explicitly
print(s1.children)
print(s2.children)
print(s3.children)
print(s4.children)


four_node_four_rows_tree_v2 = {
    1: s1,
    2: s2,
    3: s3,
    4: s4
}

four_node_four_rows_table_access_v2 = {
    1: pd.DataFrame({"X1,2":["b1", "b2"], "Y1":["a1", "a2"]}),
    2: pd.DataFrame({"X1,2":["b1", "b2", "b2", "b2"], "Y2":["10", "20", "30", "40"], "X2,3":["c1", "c1", "c1", "c2"], "X2,4":["d1", "d1", "d1", "d1"]}),
    3: pd.DataFrame({"Y3":["e1", "e2"], "X2,3":["c1", "c2"]}),
    4: pd.DataFrame({"Y4":["f1"], "X2,4":["d1"]})
}

# create root
#####################################################
#####################################################
#####################################################
#####################################################

s0 = TreeNode(0)

s2 = TreeNode(1, parent=s0)

s3 = TreeNode(2, parent=s1)

s4 = TreeNode(3, parent=s2)

s5 = TreeNode(4, parent=s2)


# add another child explicitly
print(s0.children)
print(s1.children)
print(s2.children)
print(s3.children)
print(s4.children)


five_node_padded_from_four_tree_v1 = {
    0: s0,
    1: s1,
    2: s2,
    3: s3,
    4: s4
}

five_node_padded_from_four_table_access_v1 = {
    0: pd.DataFrame({"X0,1":["t1", "t1"], "Y0":["z1", "z2"]}),
    1: pd.DataFrame({"X1,2":["b1", "b2"], "X0,1":["t1", "t1"], "Y1":["a1", "a2"]}),
    2: pd.DataFrame({"X1,2":["b1", "b2", "b2", "b2"], "Y2":["10", "20", "30", "40"], "X2,3":["c1", "c1", "c1", "c2"], "X2,4":["d1", "d1", "d1", "d1"]}),
    3: pd.DataFrame({"Y3":["e1", "e2"], "X2,3":["c1", "c2"]}),
    4: pd.DataFrame({"Y4":["f1"], "X2,4":["d1"]})
}
