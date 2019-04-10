import sys
from string import ascii_uppercase

def encrypt(message, shift, rotors, debug=0):
    i = 0
    shifted = ""
    for char in message:
        shifted += ascii_uppercase[ (ascii_uppercase.index(char) + shift + i) % 26 ]
        i += 1
    if debug: print("Shifted: %s" % shifted, file=sys.stderr)
    
    tumbled = ""
    for char in shifted: tumbled += rotors[0][ascii_uppercase.index(char)]
    if debug: print("Tumbled once: %s" % tumbled, file=sys.stderr)
    
    tumbled2 = ""
    for char in tumbled: tumbled2 += rotors[1][ascii_uppercase.index(char)]
    if debug: print("Tumbled twice: %s" % tumbled2, file=sys.stderr)
    
    tumbled3 = ""
    for char in tumbled2: tumbled3 += rotors[2][ascii_uppercase.index(char)]
    if debug: print("Tumbled thrice: %s" % tumbled3, file=sys.stderr)

    return tumbled3

def decrypt(message, shift, rotors, debug=0):
    tumbled3 = ""
    for char in message: tumbled3 += ascii_uppercase[rotors[2].index(char)]
    if debug: print("Untumbled once: %s" % tumbled3, file=sys.stderr)
    
    tumbled2 = ""
    for char in tumbled3: tumbled2 += ascii_uppercase[rotors[1].index(char)]
    if debug: print("Untumbled twice: %s" % tumbled2, file=sys.stderr)
    
    tumbled = ""
    for char in tumbled2: tumbled += ascii_uppercase[rotors[0].index(char)]
    if debug: print("Untumbled thrice: %s" % tumbled, file=sys.stderr)

    unshifted = ""
    for i in range(len(tumbled)-1,-1,-1):
        unshifted = ascii_uppercase[abs((ascii_uppercase.index(tumbled[i]) - shift - i) % 26)] + unshifted
    if debug: print("Unshifted: %s" % unshifted, file=sys.stderr)
    return unshifted

if __name__ == "__main__":
    debug = 0
    operation = input("ENCODE or DECODE: ")
    shift = int(input("Shift: "))
    rotors = []
    for i in range(3): rotors.append(input("Rotor " + i + ": "))
    message = input("Message to encode: ")
    if debug:
        print("Operation: %s\nShift: %s\nAlphabet: %s\nMessage: %s" % (operation, shift, ascii_uppercase, message),file=sys.stderr)
        for rotor in rotors: print("Rotor: %s" % rotor, file=sys.stderr)
    if operation == "ENCODE":
        print(encrypt(message, shift, rotors, debug))
    else:
        print(decrypt(message, shift, rotors, debug))
