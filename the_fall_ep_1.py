from sys import stderr

rooms = {
    0:{},
    1:{"LEFT":(0,1),"RIGHT":(0,1),"TOP":(0,1)},
    2:{"LEFT":(1,0),"RIGHT":(-1,0)},
    3:{"TOP":(0,1)},
    4:{"RIGHT":(0,1),"TOP":(-1,0)},
    5:{"TOP":(1,0),"LEFT":(0,1)},
    6:{"LEFT":(1,0),"RIGHT":(-1,0)},
    7:{"TOP":(0,1),"RIGHT":(0,1)},
    8:{"LEFT":(0,1),"RIGHT":(0,1)},
    9:{"LEFT":(0,1),"TOP":(0,1)},
    10:{"TOP":(-1,0)},
    11:{"TOP":(1,0)},
    12:{"RIGHT":(0,1)},
    13:{"LEFT":(0,1)}
}

def calculate_next_room(xi,yi,pos):
    xi = int(xi)
    yi = int(yi)
    room_type = int(tunnel[yi][xi])
    print(f"Indy is in room ({xi},{yi}) entering from the {pos}, which is a type {room_type} room",file=stderr)
    xj = xi + rooms[room_type][pos][0]
    yj = yi + rooms[room_type][pos][1]
    return (xj, yj)

# process input
w, h = [int(i) for i in input().split()]
print(f"Tunnel is {w} wide and {h} deep",file=stderr)
tunnel = [input().split() for _ in range(h)]
print(f"Tunnel map:",file=stderr)
for level in tunnel: print(level,file=stderr)
ex = int(input())
print(f"Indy must exit at x={ex}",file=stderr)

# game loop
while True:
    next_room = calculate_next_room(*input().split())
    print(" ".join(map(str,next_room)))