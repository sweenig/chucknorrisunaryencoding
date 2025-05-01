import sys

def cell(m,r,c):
    if m[r][c] == ".": return "1"
    if m[r][c] == "x": return "x"
    else: return str(int(m[r][c]) + 1)

def process_map(map):
    directions = [(-1, -1), (-1, 0), (-1, 1),  # above row
                  ( 0, -1),          (0,  1),    # same row
                  ( 1, -1), ( 1, 0), (1,  1)]    # below row
    for r, row in enumerate(map):
        for c, col in enumerate(row):
            if col == "x":  # mine found, mark all cells around it
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < h and 0 <= nc < w:  # check bounds
                        map[nr][nc] = cell(map, nr, nc)
    return map

# process inputs
w = int(input())
h = int(input())
map = []
for i in range(h): map.append(list(input()))

# display inputs
for row in map: print(''.join(row),file=sys.stderr)
print(f"w: {w}, h: {h}",file=sys.stderr)

# output result
for row in process_map(map): print(''.join(row).replace("x","."))