import string

def decimal_to_base(n:int, base:int) -> str:
    if base > len(chars): raise Exception(f"Error base is too big (max {len(chars)}).")
    if base == 1: raise Exception(f"For unary encoding use cnencode.")
    chars = (string.digits + string.ascii_uppercase + string.ascii_lowercase + string.punctuation[0]+string.punctuation[2:6])[:base]
    if n == 0: return "0" # case not handled by while loop below
    answer = ""
    num = abs(n) # strip off the negative sign
    while num: # until there's no more to get
        num, remainder = divmod(num, base) # remove the remainder from the num and make num the quotient
        answer = chars[remainder] + answer # add the remainder's character to the output string
    return "-" + answer if n < 0 else answer

def decimal_to_balanced_ternary(n:int | str)->str:
    # Handle zero case separately
    if isinstance(n, str): n = int(n)
    if n == 0: return "0"
    digits = []
    while n:
        remainder = n % 3 # Get remainder when divided by 3
        # In balanced ternary, we use -1 instead of 2
        # If remainder is 2, convert it to -1 and adjust n
        if remainder == 2:
            remainder = -1
            n += 3  # Add 3 to compensate for using -1 instead of 2
        digits.append("T" if remainder == -1 else str(remainder)) # Convert -1 to 'T' for display purposes, otherwise use the digit as is
        n //= 3 # Integer division by 3 to move to next position
    return "".join(digits[::-1])

def balanced_ternary_to_decimal(n:str)->int:
    chars = {"T":-1,"0":0,"1":1}
    return sum([chars[c] * (3 ** i) for i,c in enumerate(n[::-1])])

print(decimal_to_balanced_ternary(input()))
