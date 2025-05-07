import sys, string

v_digits = string.digits + string.ascii_uppercase[:20]  # 0-9, A-T for vigesimal

def split_glyphs(text, width): # creates a list of glyphs from the input text, each glyph is width characters wide
    lines = text.split('\n')
    num_glyphs = len(lines[0]) // width # figure out how many glyphs there are in the text
    glyphs = []
    for i in range(num_glyphs):
        glyph = [] # holds the glyph lines
        for line in lines:
            glyph.append(line[i*width:(i+1)*width]) # extract the glyph from the lines of the input text
        glyphs.append('\n'.join(glyph)) # join the lines of each glyph into a single string and add it to the returned list. Each element of this list is a glyph
    return glyphs

def glyph_to_vigesimal(glyphs,l,h):
    # print(f"Converting glyphs to vigesimal:\n{glyphs}",file=sys.stderr)
    chunks = []
    for i in range(0, len(glyphs.splitlines()), h):
        chunks.append('\n'.join(glyphs.splitlines()[i:i + h])) # split into chunks of height h, each chunk is a glyph
    # print(f"{len(chunks)} glyphs found",file=sys.stderr)
    vigesimal_digits = ""
    for glyph in chunks: # for each of the provided glyphs
        vigesimal_digit = split_glyphs(numerals, l).index(glyph) # find the index of the glyph in the glyph dictionary
        vigesimal_digits += str(v_digits[vigesimal_digit]) # add the vigesimal digit to the list
        # print(f"vigesimal digit: {vigesimal_digit} ({v_digits[vigesimal_digit]})\nSo far: {vigesimal_digits}",file=sys.stderr)
    return vigesimal_digits

def vigesimal_to_decimal(vigesimal_str: str | int) -> int:
    digits = (string.digits + string.ascii_uppercase)[:20]  # 0-9, A-J for vigesimal
    decimal = 0
    if isinstance(vigesimal_str, int): vigesimal_str = str(vigesimal_str) # if it's an integer, make it a string
    is_negative = vigesimal_str.startswith("-") # in case the value passed is negative (not happening here, but could in other use cases)
    vigesimal_str = vigesimal_str[1:] if is_negative else vigesimal_str # strip off the negative sign
    for digit in vigesimal_str.upper(): # loop through each digit
        if digit not in digits: raise ValueError(f"Invalid vigesimal digit: {digit}")
        decimal = decimal * 20 + digits.index(digit) # move existing digits left by one power of 20 and add the value of the current digit
    return -decimal if is_negative else decimal # return negative is input was negative

def decimal_to_vigesimal(decimal_num: int) -> str:
    if decimal_num == 0: return "0" # case not handled by while loop below
    vigesimal = ""
    num = abs(decimal_num) # strip off the negative sign
    while num: # until there's no more to get
        num, remainder = divmod(num, 20) # remove the remainder from the num and make num the quotient
        vigesimal = v_digits[remainder] + vigesimal # add the remainder's character to the output string
    return "-" + vigesimal if decimal_num < 0 else vigesimal

def vigesimal_to_glyph(digit):
    result = ""
    for line in range(h): # loop through the lines of the glyph dictionary
        glyph_part = numerals.splitlines()[line][digit*l:(digit*l)+l] # from the glyph dictionary, grab the part of the glyph that corresponds to the digit
        result += glyph_part + "\n" # add the part of the glyph to the result string, with a newline at the end
    result = result.rstrip('\n')
    return result

# process input glyph dictionary
(l, h) = map(int,input().split()) # l = width of glyph in characters, h = height of glyph in lines
print(f"Individual glyph width: {l} characters, height: {h} lines.",file=sys.stderr)
numerals = '\n'.join(input() for _ in range(h)) # create a string containing the raw glyphs (used for extracting glyphs)

# process input operands and operation
h1 = int(input()) # the number of lines comprising the glyphs of the first operand
glyphs_a = "\n".join(input() for _ in range(h1)) # get the string representation of the glyphs for the first operand
h2 = int(input()) # the number of lines comprising the glyphs of the second operand
glyphs_b = "\n".join(input() for _ in range(h2)) # get the string representation of the glyphs for the second operand
operation = input() # the operation to perform, one of +, -, *, /

# convert from glyph to vigesimal
vigesimal_a = glyph_to_vigesimal(glyphs_a, l, h)
vigesimal_b = glyph_to_vigesimal(glyphs_b, l, h)

# convert from vigesimal to glyph
decimal_a = vigesimal_to_decimal(vigesimal_a)
decimal_b = vigesimal_to_decimal(vigesimal_b)

# do the maths
if   operation == '+': decimal_result = decimal_a  + decimal_b
elif operation == '-': decimal_result = decimal_a  - decimal_b
elif operation == '*': decimal_result = decimal_a  * decimal_b
elif operation == '/': decimal_result = decimal_a // decimal_b

# convert result from decimal to vigesimal
vigesimal_result = decimal_to_vigesimal(decimal_result) # convert the result to vigesimal
print(f"Desired operation: {decimal_a} ({vigesimal_a}) {operation} {decimal_b} ({vigesimal_b}) = {decimal_result} ({vigesimal_result})",file=sys.stderr)

digits = [v_digits.index(digit) for digit in vigesimal_result] # convert the vigesimal string [0-9,A-T] to a list of base-20 digits, which are the indices of the glpyhs in the glyph dictionary
answer = '\n'.join(vigesimal_to_glyph(digit) for digit in digits) # extract the glyphs for each digit in the answer and combine them into a single string
print(answer)