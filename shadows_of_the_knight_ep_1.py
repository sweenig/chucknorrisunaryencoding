import sys, math

def log_msg(msg): print(msg, file=sys.stderr, flush=True)

debug = False

# process input
(w, h) = map(int, input().split())
n = int(input())  # maximum number of turns before game over.
(x,y) = map(int, input().split())
if debug: log_msg(f"Building is {w} wide and {h} tall.\nBatman is at: ({x}, {y}) with {n} seconds left")

# save the day
min_x, min_y, max_x, max_y = 0, 0, w-1, h-1
while True:
    direction = input()
    if debug: log_msg(f"Hostages are: {direction}")
    if "U" in direction: max_y = y - 1
    if "D" in direction: min_y = y + 1
    if "L" in direction: max_x = x - 1
    if "R" in direction: min_x = x + 1
    x = min_x + math.ceil((max_x - min_x) / 2)
    y = min_y + math.ceil((max_y - min_y) / 2)
    print(f"{x} {y}")
    if debug:
        n -= 1
        log_msg(f"Batman jumps to: ({x}, {y}) with {n} seconds left")
