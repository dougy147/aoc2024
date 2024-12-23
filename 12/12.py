filepath = "../inputs/12.txt"
garden = []
rows,cols = 0,0
with open(filepath,"r") as f:
    for line in f.readlines():
        line = line.replace("\n","")
        cols = 0
        l = []
        for c in line:
            l.append(c)
            cols+=1
        garden.append(l)
        rows+=1
f.close()

def is_in_grid(plant):
    x,y = plant
    if x < 0 or y < 0: return False
    if x >= rows or y >= cols: return False
    return True

def grab_section(label, coord, stack = []):
    dirs = [(-1,0),(0,1),(1,0),(0,-1)]
    x,y = coord
    for d in dirs:
        neighbour = (x+d[0],y+d[1])
        if neighbour in stack: continue
        if is_in_grid(neighbour) and garden[x+d[0]][y+d[1]] == label:
            stack.append(neighbour)
        else:
            continue
        stack = grab_section(label,neighbour,stack)
    return stack

plots = {}
for r in range(rows):
    for c in range(cols):
        if not garden[r][c] in plots: plots[garden[r][c]] = [(r,c)]
        else: plots[garden[r][c]].append((r,c))

def count_edges(label,subgroup):
    dirs = [(-1,0),(0,1),(1,0),(0,-1)]
    counter = 0
    for plant in subgroup:
        x,y = plant
        for d in dirs:
            neighbour = (x+d[0],y+d[1])
            if not is_in_grid(neighbour) or not garden[neighbour[0]][neighbour[1]] == label:
                counter+=1
    return counter

g = 0
for label in plots:
    subgroups = []
    for coord in plots[label]:
        if coord in subgroups: continue
        section = grab_section(label,coord,[])
        if section == []: section.append(coord)
        for s in section:
            subgroups.append(s)
        c = count_edges(label,section) * len(section)
        g+=c
print(f"Part 1: {g}")

def count_corners(coord,label):
    x,y = coord
    # count, if is outter corner
    dirs = [((-1,0),(0,1)),
            ((0,1) ,(1,0)),
            ((1,0) ,(0,-1)),
            ((0,-1),(-1,0))]
    is_outter = False
    is_inner = False
    outter_count = 0
    for d in dirs:
        adj1 = x+d[0][0],y+d[0][1]
        adj2 = x+d[1][0],y+d[1][1]
        if not is_in_grid(adj1) and not is_in_grid(adj2):
            is_outter = True
            outter_count+=1
        elif not is_in_grid(adj1):
            if garden[adj2[0]][adj2[1]] != label:
                is_outter = True
                outter_count+=1
        elif not is_in_grid(adj2):
            if garden[adj1[0]][adj1[1]] != label:
                is_outter = True
                outter_count+=1
        elif garden[adj1[0]][adj1[1]] != label and garden[adj2[0]][adj2[1]] != label:
            is_outter = True
            outter_count+=1
    # count, if is inner
    diags = {
            (-1,-1): [(-1,0),(0,-1)],
            (-1,1):  [(-1,0),(0,1)],
            (1,1):   [(0,1),(1,0)],
            (1,-1):  [(1,0),(0,-1)]
            }
    inner_count = 0 # how many vertices for potential inner
    for d in diags:
        n = (x+d[0],y+d[1])
        if not is_in_grid(n): continue
        if garden[n[0]][n[1]] == label: continue
        adj1 = (x+diags[d][0][0],y+diags[d][0][1])
        adj2 = (x+diags[d][1][0],y+diags[d][1][1])
        if garden[adj1[0]][adj1[1]] == label and garden[adj2[0]][adj2[1]] == label:
            is_inner = True
            inner_count+=1
    # print(f"{label} {coord}: inner: {inner_count}, outter: {outter_count}")
    return outter_count + inner_count

def count_fences(not_central,label):
    fence = 0
    maxi_corners = 0
    for plant in not_central:
        c = count_edges(label,[plant])
        if c == 2:
            fence+=1
        if c == 3:
            maxi_corners+=1
            fence+=2
    return fence + maxi_corners

g = 0
for label in plots:
    subgroups = []
    for coord in plots[label]:
        if coord in subgroups: continue
        section = grab_section(label,coord,[])
        if section == []: section.append(coord)
        for s in section:
            subgroups.append(s)
        corners = 0
        for s in section:
            corners += count_corners(s,label)
        g+=corners * len(section)
#         print(section)
#         print(f"{label}: {len(section)} * {corners} = {corners * len(section)}")
        if label == "I" and corners == 20: exit()
print(f"Part 2: {g}")
