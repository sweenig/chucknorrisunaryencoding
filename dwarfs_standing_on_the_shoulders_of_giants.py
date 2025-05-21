from sys import stderr

def find_longest_chain(relationships):
    adj_list = {}
    for parent, child in relationships:
        if parent not in adj_list: adj_list[parent] = [] # make sure there's an entry for the parent
        if child not in adj_list: adj_list[child] = [] # make sure there's an entry for the child
        adj_list[parent].append(child) # add child to parent's list
    
    for k,v in adj_list.items(): print(k, v, file=stderr) # print adjacency list for debugging
    
    def dfs(node): # recursion function to find path length
        if not adj_list[node]: return 1 # leaf node, end of chain
        max_length = 1 # assume no children (so the node itself makes a chain of length 1)
        for child in adj_list[node]: max_length = max(max_length, dfs(child)) # which is longer, what we've already found or the child?
        return max_length + 1 # child length + 1 for the current node
    
    chain_lengths = {node:dfs(node) for node in adj_list.keys()} # store chain lengths for each node
    print(chain_lengths, file=stderr)
    return max(chain_lengths.values()) # return the longest chain
    
# process input
n = int(input())
relationships = [tuple(map(int, input().split())) for _ in range(n)]
print(relationships,file=stderr)

print(find_longest_chain(relationships))