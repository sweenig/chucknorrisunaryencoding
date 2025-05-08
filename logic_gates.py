import sys
from pprint import pformat

def gate_output(operation:str,signal1:list,signal2:list)->list:
    """
    Compares two lists of booleans and returns the list of booleans with 
    each element of both lists logically operated on according to the operation
    provided. If the lists are of different sizes, the shorter list is assumed
    to have False for the missing elements.
    operation(str): one of AND,OR,XOR,NAND,NOR,NXOR
    signal1(list): list of booleans
    signal2(list): list of booleans
    """
    class ExtendedList(list):
        """
        Extends the built-in list class with a .get() method for retrieving a 
        value at a given index, but returns the default object if the index is 
        out of range. This mimics a dictionary's .get() method.
        """
        def get(self,index:int,default):
            """
            Fetches the value at index if the index is not out of range. 
            Returns the default object if it is out of range.
            index (int): The index of the value to fetch.
            default (any): The object to return if the index is out of range.
            """
            try: return self[index] # try to retrive the value
            except IndexError: return default # return the default object if the index is out of range
    r = []
    for i in range(max(len(signal1),len(signal2))): # loop through each bit of data in both signals
        a = ExtendedList(signal1).get(i,False) # gracefully fetch the current bit from signal1
        b = ExtendedList(signal2).get(i,False) # gracefully fetch the current bit from signal2
        # perform the logical operation for this one bit
        if operation == "AND": output = a and b
        elif operation == "OR": output = a or b
        elif operation == "XOR": output = (a and not b) or (not a and b)
        elif operation == "NAND": output = not (a and b)
        elif operation == "NOR": output = not (a or b)
        elif operation == "NXOR": output = not ((a and not b) or (not a and b))
        else: raise Exception(f"Operation {operation} not valid.")
        r.append(output) # add this bit's result to the output
    return r

# process input
n = int(input()) # number of signals
m = int(input()) # number of gates
# the input signals use waveform: - = True and _ = False. As we read the signals, convert to a list of booleans
signals = {line.split()[0]: [True if x == "-" else False for x in line.split()[1]] for line in [input() for _ in range(n)]}
# create a dictionary of the output signals
gates = {line.split()[0]:line.split()[1:] for line in [input() for _ in range(m)]}

# output the input
print("Input signals:",file=sys.stderr)
for signal,value in signals.items():
    print(f"{signal}: {''.join(['-' if x else '_' for x in value])}",file=sys.stderr)
print("Requested logic operations:",file=sys.stderr)
for gate,(operation,signal1,signal2) in gates.items():
    print(f"{gate}: {signal1} {operation} {signal2}",file=sys.stderr)

# process each gate
print("Output signals:",file=sys.stderr)
outputs = {}
for gate,(operation, signal1, signal2) in gates.items():
    result = gate_output(operation,signals[signal1],signals[signal2]) # execute the logic
    outputs[gate] = [*gates[gate] + result] # store the resulting list of booleans in the gates dict in case we want it later
    print(f"{gate} {''.join(['-' if x else '_' for x in result])}") # transform to the desired waveform characters

# print(pformat(outputs),file=sys.stderr)