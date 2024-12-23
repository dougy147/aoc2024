filepath = "../inputs/15.txt"

world = []

dirs = {
    "^": (-1,0),
    ">": (0,1),
    "v": (1,0),
    "<": (0,-1)
    }

def is_inside(pos,world):
    x,y = pos
    if 1 <= x and x <= len(world) - 2: return True
    if 1 <= y and y <= len(world[0]) - 2: return True
    return False

class Robot:
    def __init__(self,init_pos,moves):
        self.x, self.y = init_pos
        self.moves = moves
        self.index = 0 # move index
        self.finished = False
    def load_next_move(self,step=1):
        #self.index = (self.index + step) % (len(moves)-1)
        self.index = self.index + step
        if self.index >= len(moves): self.finished = True
    def move(self):
        if self.finished: return
        x  = self.x
        y  = self.y
        dx = dirs[self.moves[self.index]][0]
        dy = dirs[self.moves[self.index]][1]
        nx = x + dx
        ny = y + dy
        next_case = world[nx][ny]
        if next_case == "#": pass
        if next_case == ".":
            world[nx][ny], world[x][y] = world[x][y], world[nx][ny]
            self.x = nx
            self.y = ny
        if next_case == "O":
            nnx = nx + dx
            nny = ny + dy
            while is_inside((nnx,nny),world):
                distant_case = world[nnx][nny]
                if distant_case == "#": break
                if distant_case == ".":
                    world[nnx][nny] = "O"
                    world[nx][ny] = "@"
                    world[x][y] = "."
                    self.x = nx
                    self.y = ny
                    break
                nnx = nnx + dx
                nny = nny + dy
        self.load_next_move()

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
            width = len(line)
            row = []
            for i in range(len(line)):
                row.append(line[i])
                if line[i] == "@":
                    robot_start=(height,i)
            world.append(row)
            height+=1
        if not parse_map:
            for m in line: moves.append(m)
f.close()
robot = Robot(robot_start,moves)

def count_boxes_coordinates(world):
    count = 0
    for r in range(height):
        for c in range(width):
            if world[r][c] == "O":
                count += 100 * r + c
    return count

def print_world(world):
    for r in world:
        print(''.join(map(str,r)))
    print("-"*width)

while not robot.finished:
    robot.move()

print(f"Part 1: {count_boxes_coordinates(world)}")
