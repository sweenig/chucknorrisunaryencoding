from sys import stderr

def where_is_group_end(c:list|str):
    try: i = c.index(")") # look for a series group ending
    except: i = -1 # no series group ending
    try: j = c.index("]") # look for a parallel group ending
    except: j = -1 # no parallel group ending
    if (i <= j and i != -1) or j == -1: return i # if series exists and is possibly inside a parallel or if parallel doesn't exist
    else: return j # otherwise

def where_is_group_start(circuit_list:list, idx_end:int):
    c = "(" if circuit_list[idx_end] == ")" else "[" # get the type of the closing bracket
    while idx_end >= 0 and circuit_list[idx_end] != c: # without reaching the beginning and as long as we haven't found the opening bracket
        idx_end -= 1 # move to the left
    return idx_end

def series_resistance(resistors,circuit): return sum([resistors[r] for r in circuit])

def parallel_resistance(resistors,circuit): return 1.0/sum([1.0/resistors[r] for r in circuit])

def calculate_resistance(resistors,circuit):
    end = where_is_group_end(circuit) # find the first closing bracket, it's the end of the group we'll start with
    while end != -1: # as long as there are still groups in the circuit
        start = where_is_group_start(circuit, end) # find the start of the group we're working on
        r = series_resistance(resistors, circuit[start+1:end]) if circuit[start] == "(" else parallel_resistance(resistors, circuit[start+1:end]) # calculate series or parallel based on the group brackets
        resistors[str(r)] = r # store the answer in the resistors so we don't have to recalculate
        circuit[start] = str(r) # replace the opening bracked with the resistance value
        for _ in range(end-start): circuit.pop(start+1) # remove resistors and closing bracked from circuit
        end = where_is_group_end(circuit) # figure out the next group ending (which may be none)
    return f"{float(circuit[0]):.1f}" # return with 1 decimal point of precision

# process input
n = int(input())
resistors = {name:float(resistance) for name,resistance in [input().split() for _ in range(n)]}
print(f"Resistors:\n{resistors}",file=stderr)
circuit = input().split()
print(f"Circuit:\n{circuit}",file=stderr)

# do the calculation and output
print(calculate_resistance(resistors,circuit))