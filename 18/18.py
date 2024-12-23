filepath = "../inputs/18.txt"
w,h=70+1,70+1

falling_bytes = []
with open(filepath,"r") as f:
    for line in f.readlines():
        line=line.replace("\n","")
        x,y = line.split(",")
        x,y = int(x),int(y)
        falling_bytes.append((x,y))
f.close()

def is_in_world(pos):
    x,y = pos
    if 0 > x or x >= h: return False
    if 0 > y or y >= w: return False
    return True

def print_world():
    for r in world:
        print(''.join(map(str,r)))

start = (0,0)
end = (h-1,w-1)
world = [["." for _ in range(w)] for _ in range(h)]

# Part 1
bytes_to_fall = 1024
for b in range(bytes_to_fall):
    x,y = falling_bytes[b]
    world[x][y] = "#"

dirs = [(0,1), (1,0), (0,-1), (-1,0)]

visited = set()
      # score,pos,dir,prevs # prevs are for Part 2
queue = [(0,start,0,[])]
while queue != []:
    q = queue.pop(0)
    score, pos, d, prevs = q
    x,y = pos

    if ((x,y),d) in visited: continue
    visited.add(((x,y),d))

    if pos == end:
        print("Part 1:", score)
        prevs+=[pos]
        break

    for d in dirs:
        nx,ny = x+d[0], y+d[1]
        if not is_in_world((nx,ny)): continue
        if world[nx][ny] == "#": continue
        queue.append((score+1,(nx,ny),d,prevs+[pos]))
    queue = sorted(queue)

# Part 2
def can_exit():
    visited = set()
          # score,pos,dir
    queue = [(0,start,0)]
    while queue != []:
        q = queue.pop(0)
        score, pos, d = q
        x,y = pos

        if ((x,y),d) in visited: continue
        visited.add(((x,y),d))

        if pos == end:
            return True

        for d in dirs:
            nx,ny = x+d[0], y+d[1]
            if not is_in_world((nx,ny)): continue
            if world[nx][ny] == "#": continue
            queue.append((score+1,(nx,ny),d))
        queue = sorted(queue)
    return False

on_path_yet = False
for b in range(bytes_to_fall, len(falling_bytes)-1):
    rem = len(falling_bytes) - b
    world[falling_bytes[b][0]][falling_bytes[b][1]] = "#"
    if not on_path_yet:
        for pos in prevs:
            if pos == falling_bytes[b]: on_path_yet = True
    if not on_path_yet: continue
    if not can_exit():
        print(f"Part 2: {falling_bytes[b]}")
        exit()
