filepath = "../inputs/13.txt"

class Machine:
    def __init__(self,A,B,prize):
        self.xA, self.yA = A
        self.xB, self.yB = B
        self.xP, self.yP = prize

machines = []
with open(filepath,"r") as f:
    current = 0
    for line in f.readlines():
        line = line.replace("\n","")
        if line != "":
            if current == 0 or current == 1: # button A B
                split = line.split("+")
                X = int(split[1].split(",")[0])
                Y = int(split[2])
                if current == 0: A=(X,Y)
                else: B=(X,Y)
                current+=1
            elif current == 2: # prize
                current = 0
                split = line.split("=")
                prize=(int(split[1].split(",")[0]),int(split[2]))
        else:
            m = Machine(A,B,prize)
            machines.append(m)
m = Machine(A,B,prize)
machines.append(m)

tokens = 0
for m in machines:
    pX = m.xP
    pY = m.yP

    xA = m.xA
    yA = m.yA
    xB = m.xB
    yB = m.yB

    allowed_push = 100
    for A in range(0,allowed_push + 1):
        for B in range(0,allowed_push + 1):
            x = (A * xA) + (B * xB)
            y = (A * yA) + (B * yB)
            if x == pX and y == pY:
                tokens += ((3 * A) + (1 * B))

print(f"Part 1: {tokens}")

# Part 2
for m in machines:
    m.xP+= 10_000_000_000_000
    m.yP+= 10_000_000_000_000

tokens = 0
for m in machines:
    xP = m.xP
    yP = m.yP

    xA = m.xA
    yA = m.yA
    xB = m.xB
    yB = m.yB

    m = ((yB * xP) - (xB * yP)) / ((yB * xA) - (xB * yA))
    if int(m) == m:
        n = (xP - (xA * m)) / xB
        if int(n) == n:
            tokens+=((3 * m) + (1 * n))
    else:
        continue
print(f"Part 2: {int(tokens)}")
