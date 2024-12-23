filepath = "../inputs/11.txt"

stones = []
with open(filepath,'r') as f:
    for stone in f.readlines()[0].replace("\n","").split(" "):
        stones.append(int(stone))
f.close()

calls = {}
def memo(f):
    global calls
    def m(*x):
        if not str([*x]) in calls: calls[str([*x])] = f(*x)
        return calls[str([*x])]
    return m

def blink(stone):
    if stone == 0:
        return (1,None)
    elif len(str(stone)) % 2 == 0:
        left = int(str(stone)[:int(len(str(stone))/2)])
        right = int(str(stone)[int(len(str(stone))/2):])
        return (left,right)
    else:
        return (stone * 2024,None)

def count(stone,depth):
    left,right = blink(stone)
    if depth == 1:
        if right == None: return 1
        return 2

    c = count(left,depth-1)
    if right != None:
        c+= count(right,depth-1)
    return c

count = memo(count)

part1 = 0
for s in stones:
    part1+=count(s,25)
print(f"Part 1: {part1}")

part2 = 0
for s in stones:
    part2+=count(s,75)
print(f"Part 2: {part2}")
