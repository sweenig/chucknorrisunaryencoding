import sys

def debug(message,indent=0): print(f"{indent*' '}{message}",file=sys.stderr)

def find_nodes(grid):
    nodes = ""
    for row_idx, row in enumerate(grid):
        for col_idx, col in enumerate(row):
            if col == ".":
                debug(f"({row_idx},{col_idx}) is not a node ({col}). Moving on.", 1)
                continue
            nodes += f"{col_idx} {row_idx} "
            debug(f"({row_idx},{col_idx}) is a node. Finding coordinates of next node to the right.",2)
            try:
                next_node = f"{row[col_idx+1:].index('0')+col_idx+1} {row_idx} "
                nodes += next_node
                debug(f"Node to the right found at {next_node.strip()}",3)
            except ValueError:
                nodes += "-1 -1 "
                debug(f"No node to the right found.",3)
            debug(f"... and below.",2)
            try:
                next_row = next(i for i in range(row_idx + 1, len(grid)) if grid[i][col_idx] == '0')
                nodes += f"{col_idx} {next_row}"
                debug(f"Node below found at {col_idx} {next_row}",3)
            except StopIteration:
                nodes += "-1 -1"
                debug(f"No node below found.",3)
            nodes += "\n"
    return nodes.strip()

def process_input():
    width = int(input())  # the number of cells on the X axis
    height = int(input())  # the number of cells on the Y axis
    debug(f"Grid is {width}x{height}")
    grid = [input() for _ in range(height)]
    debug(f"Grid:")
    for x in grid: debug(x)
    return grid

print(find_nodes(process_input()))
