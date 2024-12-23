filepath = "../inputs/21.txt"
codes = []
with open(filepath,"r") as f:
    for line in f.readlines():
        line=line.replace("\n","")
        codes.append(line)
f.close()

dirs     = [(0,1),(1,0),(0,-1),(-1,0)]
dirs_sym = {(0,1):">",(1,0):"v",(0,-1):"<",(-1,0):"^"}

# ['^^<<A', '^<^<A', '^<<^A', '<^^<A', '<^<^A', '<<^^A']
numk = {"7":(0,0),"8":(0,1),"9":(0,2),
        "4":(1,0),"5":(1,1),"6":(1,2),
        "1":(2,0),"2":(2,1),"3":(2,2),
                  "0":(3,1),"A":(3,2),
        "x":(3,0), }

dirk = {"x":(0,0),
                  "^":(0,1),"A":(0,2),
        "<":(1,0),"v":(1,1),">":(1,2), }

def shortest_paths(keyA,keyB,keypad):
    # Used to build all paths from one
    # key to another on any keypad.
    paths = []
    if keyA == keyB: return paths
    found = False
    queue = [(0,keyA,[keyA])]
    while queue != []:
        q = queue.pop(0)
        distance, pos, path = q
        x,y = pos
        if pos == keyB:
            if not found:
                found = True
                paths.append(path)
                min_distance = distance
            else:
                if distance == min_distance:
                    if not path in paths:
                        paths.append(path)
        for d in dirs:
            nx,ny = x+d[0],y+d[1]
            npos = nx,ny
            if npos in path: continue
            if keypad == "num":
                if not npos in numk.values(): continue
            elif keypad == "dir":
                if not npos in dirk.values(): continue
            nq = (distance+1,npos,path+[npos])
            queue.append(nq)
        queue = sorted(queue)
    return paths
## example use:  "0"   "9"  keypad="num"
#shortest_paths((3,1),(0,2),"num")

def paths_to_instructions(paths,keypad):
    if paths == []: return ["A"]
    instructions = []
    for p in paths:
        good = True
        instr = ""
        for i in range(1,len(p)):
            prev = p[i-1]
            curr = p[i]
            px,py = prev
            cx,cy = curr
            direction = (cx-px,cy-py)
            check = (px+direction[0],py+direction[1])
            if keypad == "num":
                if numk["x"] == check:
                    # then current instruction is false
                    good = False
                    break
            if keypad == "dir":
                if dirk["x"] == check:
                    # then current instruction is false
                    good = False
                    break
            symbol = dirs_sym[direction]
            instr+=symbol
        if good:
            instr+="A"
            instructions.append(instr)
    return instructions


numk_rel = {} # relation between each keys
dirk_rel = {} # relation between each keys

for k1 in numk:
    for k2 in numk:
        if k1 == "x" or k2 == "x": continue
        paths = shortest_paths(numk[k1],numk[k2],"num")
        numk_rel[(k1,k2)] = tuple(paths_to_instructions(paths,"num"))

for k1 in dirk:
     for k2 in dirk:
         if k1 == "x" or k2 == "x": continue
         paths = shortest_paths(dirk[k1],dirk[k2],"dir")
         dirk_rel[(k1,k2)] = tuple(paths_to_instructions(paths,"dir"))

# All instructions (e.g. "^<<A") for any key to another
# for any type of keypad have been stored in two dicts:
#  numeric: "numk_rel"    ,   directional: "dirk_rel"

# Example: numk_rel[("0","9")] = ('^^^>A', '^^>^A', '^>^^A', '>^^^A')
# -----------------------------------------------------#

def code_to_instructions(code,keypad):
    # I nest this one here, because both functions
    # are useless without the other.
    def build_all_strings(instr,string="",ins=None):
        if ins == None: ins = []
        if instr == ():
            ins.append(string)
            return
        for s in instr[0]:
            build_all_strings(instr[1:],string+s,ins)
        return ins

    prev = "A"
    instr = []
    for c in range(len(code)):
        curr = code[c]
        if keypad == "num":
            instr.append(numk_rel[(prev,curr)])
        elif keypad == "dir":
            instr.append(dirk_rel[(prev,curr)])
        prev=curr
    return build_all_strings(tuple(instr))

def split_keep(s):
    # Know better in Python?
    x = s.split("A")
    x = [y + "A" for y in x]
    if s[len(s)-1] == "A": x = x[:-1]
    else: x[len(x)-1] = x[len(x)-1].replace("A","")
    return x

cache = {}
def shortest_seq(instructions,depth,cache={}):
    if depth == 0:
        return len(instructions)
    if (instructions,depth) in cache:
        return cache[(instructions,depth)]
    inst_sublist = split_keep(instructions)
    total = 0
    for sub in inst_sublist:
        # here we translate current instruction
        # for the next farthest robot
        seq = code_to_instructions(sub,"dir")
        m = float("inf")
        for s in seq:
            x = shortest_seq(s,depth-1,cache)
            if x < m:
                m = x
        total+=m # total is the size of the smallest instruction sequence for current instruction
    cache[(instructions,depth)] = total
    return total


part1 = 0
part2 = 0
for code in codes:
    robot1 = code_to_instructions(code,"num")
    m_part1 = float("inf")
    m_part2 = float("inf")
    for inst in robot1:
        x_part1 = shortest_seq(inst,2)
        x_part2 = shortest_seq(inst,25)
        if x_part1 < m_part1: m_part1 = x_part1
        if x_part2 < m_part2: m_part2 = x_part2
    part1+=m_part1*int(code.replace("A",""))
    part2+=m_part2*int(code.replace("A",""))

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
