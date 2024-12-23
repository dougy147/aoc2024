# robots position (p=x,y) (x from the left wall, y from the top wall)
# and velocities (v=x',y') (velocity in tiles per second)

# map is toroidal

# Part1:
# After 100 seconds, how many robots in each quadrant
# (ignore those exactly in the middle)
# Multiply numbers from each quadrant

width  = 101 # map cols (x)
height = 103 # map rows (y)

class Robot:
    def __init__(self,p,v):
        self.px = p[0]
        self.py = p[1]
        self.vx = v[0]
        self.vy = v[1]
    def move(self,iterations = 1):
        for i in range(iterations):
            self.px = (self.px + self.vx) % width
            self.py = (self.py + self.vy) % height
    def get_quadrant(self):
        if self.px <= width//2-1: # left side
            if self.py <= height//2-1: # top
                return "q1" # q1 = top left
            if self.py >= height//2+1: # bottom
                return "q2" # q2 = bottom left
        if self.px >= width//2+1: # right side
            if self.py <= height//2-1: # top
                return "q3" # top right
            if self.py >= height//2+1: # bottom
                return "q4" # top left
        return "q5" # middle

filepath = "../inputs/sample-14.txt"
filepath = "../inputs/14.txt"

robots = []
with open(filepath,"r") as f:
    for line in f.readlines():
        line = line.replace("\n","")
        s = line.split("=")
        px = int(s[1].split(",")[0])
        py = int(s[1].split(",")[1].split(" ")[0])
        v = s[2].split(",")
        vx = int(v[0])
        vy = int(v[1])
        p,v = (px,py), (vx,vy)
        r = Robot(p,v)
        robots.append(r)
#print(len(robots))

def solve_part_one():
    q1,q2,q3,q4,q5 = 0,0,0,0,0
    for r in robots:
        r.move(100)
        q = r.get_quadrant()
        match q:
            case "q1": q1+=1
            case "q2": q2+=1
            case "q3": q3+=1
            case "q4": q4+=1
            case "q5": q5+=1
    #print(q1,q2,q3,q4)
    res = q1*q2*q3*q4
    print(f"Part 1: {res}")

# Part 2
def print_map(robots):
    m = [[" " for _ in range(width)] for _ in range(height)]
    for r in robots:
        x,y = r.px,r.py
        m[y][x] = "*"
    for row in m:
        print(''.join(map(str,row)))
    print("-"*101)

#import numpy as np
#from PIL import Image
#
#import numpy
#def save_map(iteration):
#    m = [[0 for _ in range(width)] for _ in range(height)]
#    for r in robots:
#        x,y = r.px,r.py
#        m[y][x] = 255
#    np_array = np.array(m,dtype=np.uint8)
#    image = Image.fromarray(np_array)
#    fname = str(iteration) + '.png'
#    image.save(fname)
#
#for i in range(10000):
#    save_map(i)
#    for r in robots:
#        r.move(1)

def are_neighbours(robot1,robot2):
    dirs = [(0,1),(1,0),(0,-1),(-1,0)]
    x,y = robot1.px,robot1.py
    for d in dirs:
        nx,ny = robot2.px + d[0],robot2.px + d[1]
        if x == nx and y == ny: return True
    return False

def find_tree_foot(robots):
    '''
    if same number of aligned on cols distant of one: candidate
    (symetry of the tree)
    '''
    threshold = 14 # today's date
    m = [[" " for _ in range(width)] for _ in range(height)]
    for r in robots:
        x,y = r.px,r.py
        m[y][x] = "*"
    for r in range(len(m)-1-1):
        if threshold == 0: return True
        line1 = ''.join(map(str,m[r]))
        line2 = ''.join(map(str,m[r+1]))
        index_max1 = max(range(len(line1)), key=line1.__getitem__)
        index_max2 = max(range(len(line2)), key=line2.__getitem__)
        if index_max1 == index_max2:
            threshold -= 1
    return False

def solve_part_two():
    aligned = 0
    for i in range(0,10000):
        if find_tree_foot(robots):
            print(f"Part 2: {i+100}") # Add 100, because robots already moved 100.
            return
        for r in robots:
            r.move(1)

solve_part_one()
solve_part_two()
