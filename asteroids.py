import sys
import math
import string

def plot_future_positions(w, h, t1, t2, t3, p1, p2, debug=False):
    # indicate correct parsing of inputs
    if debug:
        print(f"Time between t1 and t2: {t2-t1}",file=sys.stderr)
        print(f"Time between t2 and t3: {t3-t2}",file=sys.stderr)
    p3 = [['.' for _ in range(w)] for _ in range(h)]
    if debug:
        for name,pic in [("P1",p1),("P2",p2)]:
            print("\n" + name,file=sys.stderr)
            for row in pic:
                print("".join(row),file=sys.stderr)
    # identify asteroids in both pictures
    asteroids = set()
    for row in p1:
        for char in row:
            if char in string.ascii_uppercase:
                asteroids.add(char)
    # put identified asteroids in reverse order starting with the farthest away
    asteroids = sorted(list(asteroids), reverse=True)
    if debug: print(f"Asteroids: {asteroids}", file=sys.stderr)
    for a in asteroids:
        if debug: print("\n" + a,file=sys.stderr)
        # determine position of current asteroid at t1
        x1 = x2 = y1 = y2 = 0
        for idx_row, row in enumerate(p1):
            if a in row:
                x1 = row.index(a)
                y1 = idx_row
                break
        if debug: print(f"Found coordinates of {a} at t1: ({x1},{y1})",file=sys.stderr)
        # determine position of current asteroid at t2
        for idx_row, row in enumerate(p2):
            if a in row:
                x2 = row.index(a)
                y2 = idx_row
                break
        if debug: print(f"Found coordinates of {a} at t2: ({x2},{y2}), {t2-t1} seconds later",file=sys.stderr)
        # calculate movement/t in x and y directions
        mx = (x2 - x1)/(t2 - t1)
        my = (y2 - y1)/(t2 - t1)
        if debug: print(f"Found vector of {a}: ({mx},{my})/second",file=sys.stderr)
        # calculate future position at t3
        x_vector = math.floor(mx * (t3 - t2))
        y_vector = math.floor(my * (t3 - t2))
        if debug: print(f"{a} will move ({x_vector},{y_vector})",file=sys.stderr)
        x3 = int(x2 + x_vector)
        y3 = int(y2 + y_vector)
        # add asteroid to p3
        if 0 <= x3 < w and 0 <= y3 < h:
            p3[y3][x3] = a
            if debug: print(f"Found coordinates of {a} at t3: ({x3},{y3})",file=sys.stderr)
        else:
            if debug: print(f"Coordinates of {a} at t3: ({x3},{y3}) are out of bounds",file=sys.stderr)
    output = ""
    for row in p3: output += ''.join(row) + "\n"
    return output.strip()

# receive inputs
w, h, t1, t2, t3 = [int(i) for i in input().split()]
p1,p2 = [],[]
for i in range(h):
    first_picture_row, second_picture_row = input().split()
    p1.append(first_picture_row)
    p2.append(second_picture_row)

x = plot_future_positions(w, h, t1, t2, t3, p1, p2)
print(x)