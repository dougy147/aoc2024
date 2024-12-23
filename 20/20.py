filepath = "../inputs/20.txt"

laby = []
h = 0
with open(filepath,"r") as f:
    for line in f.readlines():
        line = line.replace("\n","")
        w = len(line)
        row = ["" for _ in range(w)]
        for c in range(w):
            x = line[c]
            if x == "S":
                start = (h,c)
                x == "."
            if x == "E":
                end = (h,c)
                x == "."
            row[c] = x
        laby.append(row)
        h+=1

dirs = [(0,1), (1,0), (0,-1), (-1,0)]

visited = set()
prevs = {}
      # score,pos,dir,prevs # storing the prevs for part2 (with their distance inside)
queue = [(0,start,0)]
while queue != []:
    q = queue.pop(0)
    score, pos, d = q
    x,y = pos

    if (pos,d) in visited: continue
    visited.add((pos,d))

    if pos == end:
        shortest_path = score
        prevs[pos] = score
        break

    for d in dirs:
        nx,ny = x+d[0], y+d[1]
        if laby[nx][ny] == "#": continue
        if not pos in prevs:
            prevs[pos] = score
        queue.append((score+1,(nx,ny),d))
    queue = sorted(queue)

def is_in_laby(cell):
    x,y = cell
    if 0 > x or x >= h: return False
    if 0 > y or y >= w: return False
    return True

def solve_part_one():
    cheats = 0
    for pos in prevs:
        x,y = pos
        i = prevs[pos]
        for d in dirs:
            nx,ny = x+2*d[0], y+2*d[1]
            npos = (nx,ny)
            if not is_in_laby(npos): continue
            if laby[nx][ny] == "#": continue
            gain = prevs[npos]
            if gain < i: continue
            if gain - i <= 2: continue
            if gain - i - 2 >= 100: # 2 is the size of the cheat
                cheats+=1
    print(f"Part 1: {cheats}")
solve_part_one()

# Part 2
def taxicab_distance(pos1,pos2):
    x1,y1 = pos1
    x2,y2 = pos2
    return abs(x1-x2) + abs(y1-y2)

cheated = {}
cheats = set()
for pos1 in prevs:
    x1,y1 = pos1
    i = prevs[pos1]
    for d in dirs:
        xc = x1 + d[0] # looking for cheat entry
        yc = y1 + d[1]
        cheat_entry = (xc,yc)
        if not is_in_laby(cheat_entry): continue
        if not laby[xc][yc] == "#": continue
        if cheat_entry in prevs: continue
        for r in range(x1-20,x1+20+1):
            if r < 0+1 or r >= h-1: continue
            for c in range(y1-20,y1+20+1):
                if c < 0+1 or c >= w-1: continue
                pos2 = (r,c)
                x2,y2 = pos2
                taxicab = taxicab_distance(pos1,pos2)
                if not taxicab <= 20: continue
                if laby[x2][y2] == "#": continue
                gain = prevs[pos2]
                if gain < i: continue
                if gain - i <= taxicab: continue # prob here part 2
                if gain - i - taxicab >= 100:
                    #cheats+=1
                    cheats.add((pos1,pos2))
print(f"Part 2: {len(cheats)}")
