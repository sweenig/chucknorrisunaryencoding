import sys

map = {
    "sp": " ",
    "bS": "\\",
    "sQ": "'",
    "nl": "\n"
}

# process input
blocks = input().split(" ")
print(blocks,file=sys.stderr, flush=True)

# prepare output
output = ""
for block in blocks:
    if block[-2] in "sbn":
        count = block[:-2]
        char = map[block [-2:]]
        if char == "\n": count = 1
    else:
        count = block[:-1]
        char = block[-1]
    print(f"block: {block} count: {count} char: {char}",file=sys.stderr,flush=True)
    output += char * int(count)

# output the output
print(output)
