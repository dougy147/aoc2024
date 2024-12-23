filepath = "../inputs/sample-16.txt"
filepath = "../inputs/sample-16-2.txt"
filepath = "../inputs/16.txt"

world = []
height = 0
with open(filepath,"r") as f:
    for line in f.readlines():
        line = line.replace("\n","")
        width = len(line)
        tmp = []
        for c in line :
            if c == "S":
                start_pos = (height,line.index("S"))
                c = "."
            if c == "E":
                end_pos = (height,line.index("E"))
                c = "."
            tmp.append(c)
        world.append(tmp)
        height+=1

#        E      S      W       N
dirs = [(0,1), (1,0), (0,-1), (-1,0)]

#        cost  pos    dir visited_tiles
queue = [(0,start_pos,0, [])] # initialize queue with first roundabout to explore (with a cost of zero, obviously)

scores = {}
while queue != []:
    q = queue.pop(0)
    score,pos,d,tiles = q
    x,y = pos
    state = (pos,d)

    for i in range(3):
        # explore in same direction
        if i == 0:
            nd = d
            nx, ny = x+dirs[d][0], y+dirs[d][1]
            if world[nx][ny] == "#": continue
            cost = score + 1
            ntiles = tiles + [(nx,ny)]
        # explore -90°
        elif i == 1:
            nd = (d-1)%len(dirs)
            nx, ny = x,y
            cost = score + 1000
            ntiles = tiles
        # explore +90°
        elif i == 2:
            nd = (d+1)%len(dirs)
            nx, ny = x,y
            cost = score + 1000
            ntiles = tiles

        npos = (nx,ny)
        state2 = (npos,nd)

        if not state2 in scores or scores[state2][0] > cost:
            scores[state2] = (cost, set(ntiles))
            nq = (cost, (nx,ny), nd, ntiles)
            queue.append(nq)
        elif scores[state2][0] == cost:
            scores[state2] = (cost, scores[state2][1] | set(ntiles))
            nq = (cost, (nx,ny), nd, ntiles)
            queue.append(nq)

    queue = sorted(queue)

## Part 1
shortest = 99999999
path = set()
for i in range(len(dirs)):
    score, tiles = scores[(end_pos,i)]
    if score < shortest:
        shortest = score
        path = set(tiles)
    elif score == shortest:
        path |= set(tiles)
print("Part 1:", shortest)
print("Part 2:", len(tiles) + 1) # don't forget to count "END"
