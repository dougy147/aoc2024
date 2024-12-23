filepath = "../inputs/10.txt"

topo = []
with open(filepath,'r') as f:
    for line in f.readlines():
        line = line.replace("\n","")
        curhs = []
        for h in line:
            curhs.append(int(h))
        topo.append(curhs)
height = len(topo)
width = len(topo[0])


dirs = {
        'up': (-1,0),
        'right': (0,1),
        'down': (1,0),
        'left': (0,-1),
        }

def val_at(cell):
    return topo[cell[0]][cell[1]]

def is_in_grid(cell):
    x,y = cell
    if 0 > x or x >= height: return False
    if 0 > y or y >= width: return False
    return True

def grab_neighbours(cell):
    ns = []
    for d in dirs:
        n = (cell[0] + dirs[d][0], cell[1] + dirs[d][1])
        if is_in_grid(n): ns.append(n)
    return ns

def reach_nine(cell,start_point,visited,part):
    score = 0
    if val_at(cell) == 9:
        if part == "part1":
            if (cell,start_point) in visited: return 0
            visited.append((cell, start_point))
        return 1
    ns = grab_neighbours(cell)
    for n in ns:
        if (n,cell) in visited: continue
        if val_at(n) != val_at(cell) + 1: continue
        score+=reach_nine(n,start_point,visited,part)
    return score

def solve():
    part_one = 0
    part_two = 0
    for x in range(height):
        for y in range(width):
            if val_at((x,y)) == 0:
                part_one += reach_nine((x,y),(x,y),[],"part1")
                part_two += reach_nine((x,y),(x,y),[],"part2")
    print(f"Part 1: {part_one}")
    print(f"Part 2: {part_two}")
solve()
