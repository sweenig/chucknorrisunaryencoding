import sys

def calculate(cells, instructions):
    for row, (operation, arg1, arg2) in enumerate(instructions): # loop through the calculations
        if cells[row] is not None: continue # this cell has a value, move on to the next cell
        if "$" in arg1: # it's a reference
            r = int(arg1[1:]) # figure out the reference's row number
            if cells[r] is None: continue # the referenced cell hasn't been calculated. Skip this calculating this cell.
            a = cells[r] # the referenced cell has a value, get it.
        else: a = int(arg1) # not a reference, grab the value
        if "$" in arg2: # it's a reference
            r = int(arg2[1:]) # figure out the reference's row number
            if cells[r] is None: continue # the referenced cell hasn't been calculated. Skip calculating this cell.
            b = cells[r] # the referenced cell has a value, get it
        else: b = int(arg2) if "_" not in arg2 else arg2 # not a reference, grab the value (unless it's not needed)
        # calculate this cell's value and store it in the spreadsheet
        if operation == "VALUE": cells[row] = a
        if operation == "ADD": cells[row] = a + b
        if operation == "SUB": cells[row] = a - b
        if operation == "MULT": cells[row] = a * b
    return cells

# process input
n = int(input())
instructions = [input().split() for _ in range(n)]

# create the empty spreadsheet
cells = [None for _ in range(n)]
print(cells,file=sys.stderr)

# calculate until all cells are populated
while None in cells: cells = calculate(cells,instructions)

for cell in cells: print(cell)
