filepath = "../inputs/15.txt"

world = []

dirs = {
    "^": (-1,0),
    ">": (0,1),
    "v": (1,0),
    "<": (0,-1)
    }

class Robot:
    def __init__(self,init_pos,moves):
        self.pos = init_pos
        self.moves = moves
        self.index = 0 # move index
        self.finished = False
    def move(self):
        x, y = self.pos
        dx,dy = dirs[self.moves[self.index]]
        nx, ny = x + dx, y + dy
        b = world[nx][ny]
        if b == "#": pass
        elif b == ".":
            world[x][y] = "."
            world[nx][ny] = "@"
            self.pos = (nx,ny)
        else:
            if b.movable(dx,dy):
                b.move(dx,dy)
                world[x][y] = "."
                world[nx][ny] = "@"
                self.pos = (nx,ny)
        self.index+=1
        if self.index >= len(self.moves): self.finished = True

class Box:
    def __init__(self,pos):
        self.x, self.l, self.r = pos # l = left, r = right
    def movable(self, dx, dy):
        x,l,r=self.x,self.l,self.r
        ns = set()
        if dx != 0: # up/down
            ns.add(world[x+dx][l])
            ns.add(world[x+dx][r])
            for n in ns:
                if n == "#": return False
                if type(n) == Box and not n.movable(dx,dy): return False
            return True
        elif dy > 0:
            n = world[x][r+dy]
            if n == "#": return False
            if n == ".": return True
            if n.movable(dx,dy): return True
            return False
        else:
            n = world[x][l+dy]
            if n == "#": return False
            if n == ".": return True
            if n.movable(dx,dy): return True
            return False

    def move(self, dx, dy):
        x,l,r=self.x,self.l,self.r
        if dy != 0: # easiest: moving right or left
            if dy > 0:
                n = world[x][r+dy]
            else:
                n = world[x][l+dy]
            if type(n) == Box:
                n.move(dx,dy)
            if dy > 0:
                world[x][r+dy] = self
                world[x][l] = "."
            else:
                world[x][l+dy] = self
                world[x][r] = "."
            self.l = l+dy
            self.r = r+dy
        else: # hardest, move above/under
            nl = world[x+dx][l] # neighbour up/above left
            nr = world[x+dx][r] # neighbour up/above right
            if nl == nr:
                if type(nl) == Box:
                    nl.move(dx,dy)
            else: # we have either two boxes over our current one, or one box and one "."
                if type(nl) == Box: nl.move(dx,dy)
                if type(nr) == Box: nr.move(dx,dy)
            world[x+dx][l] = self
            world[x+dx][r] = self
            world[x][l], world[x][r] = ".","."
            self.x = x+dx

moves = []
with open(filepath,"r") as f:
    height = 0
    parse_map = True
    for line in f.readlines():
        line = line.replace("\n","")
        if line == "":
            parse_map = False
            continue
        if parse_map:
            row = []
            for i in range(len(line)):
                if line[i] == "#": row.append("#"),row.append("#")
                if line[i] == ".": row.append("."),row.append(".")
                if line[i] == "O": row.append("O"),row.append("O")
                if line[i] == "@": row.append("@"),row.append(".")
            for i in range(len(row)):
                if row[i] == "@":
                    robot_start=(height,i)
                if row[i] == "O":
                    box = Box((height,i,i+1))
                    row[i] = box
                    row[i+1] = box
                    i+=1
            width = len(row)
            world.append(row)
            height+=1
        if not parse_map:
            for m in line: moves.append(m)
f.close()
robot = Robot(robot_start,moves)

def count_boxes_coordinates(world):
    count = 0
    boxes = []
    for r in range(height):
        for c in range(width):
            if type(world[r][c]) == Box and not world[r][c] in boxes:
                boxes.append(world[r][c])
                count += 100 * r + c
    return count

def print_world(world):
    for r in world:
        to_print = []
        boxes = []
        for c in range(len(r)):
            item = r[c]
            if type(item) == Box:
                if item in boxes: continue
                boxes.append(item)
                to_print.append("[")
                to_print.append("]")
            else:
                to_print.append(item)
        print(''.join(map(str,to_print)))
    print("-"*width)

while not robot.finished:
    robot.move()

print(f"Part 2: {count_boxes_coordinates(world)}")
