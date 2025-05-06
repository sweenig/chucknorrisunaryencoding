import sys
from pprint import pformat

def store_number_in_tree(tree, telephone):
    if not telephone: return tree # escape condition for recursion
    first_digit = telephone[0] # get the label for the current node in the tree
    if first_digit not in tree: tree[first_digit] = {} # if the node doesn't exist, create it
    tree[first_digit] = store_number_in_tree(tree[first_digit], telephone[1:]) # add the children of this node to this node (recursion)
    return tree # return the tree with the new node(s) added

def count_all_keys(tree):
    if not tree: return 0 # escape condition for recursion
    count = len(tree)  # Count keys at current level
    for digit in tree: count += count_all_keys(tree[digit])  # Add counts from sub-dictionaries
    return count # return the total count for this node and its children

# process input
n = int(input())

# build the node tree
data = {}
for i in range(n):
    number = input()
    print(f"Number: {number}", file=sys.stderr)
    data = store_number_in_tree(data, number)

# output the tree and the count of all keys
print(pformat(data),file=sys.stderr)
print(count_all_keys(data))