import sys

def to_roman(num):
    result = ""
    digits = {v:k for k, v in numerals.items()}
    # Sort digits in descending order to ensure proper Roman numeral construction
    for value in sorted(digits.keys(), reverse=True):
        while num >= value:
            result += digits[value]
            num -= value
    return result

def from_roman(roman):
    result = 0
    i = 0
    while i < len(roman):
        # Check for two-character numerals first
        if i + 1 < len(roman) and roman[i:i+2] in numerals:
            result += numerals[roman[i:i+2]]
            i += 2
        else:
            result += numerals[roman[i]]
            i += 1
    return result

numerals = {
    "I":1,
    "V":5,
    "X":10,
    "L":50,
    "C":100,
    "D":500,
    "M":1000,
    "IV":4,
    "IX":9,
    "XL":40,
    "XC":90,
    "CD":400,
    "CM":900
}

# process input
n = int(input())
numbers = [int(input()) for i in range(n)]
print(numbers,file=sys.stderr)

# form ranks
arabic_numbers = [str(from_roman(roman)) for roman in sorted([to_roman(num) for num in numbers])]
print(" ".join(arabic_numbers))
