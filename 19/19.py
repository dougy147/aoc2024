filepath = "../inputs/19.txt"

patterns = []
designs  = []

desired_designs = False
with open(filepath,"r") as f:
    for line in f.readlines():
        line = line.replace("\n","")
        if line == "":
            desired_designs = True
            continue
        if not desired_designs:
            pats = line.split(",")
            for p in pats:
                p=p.replace(" ","")
                patterns.append(p)
        else:
            designs.append(line)
f.close()
patterns.sort(key=lambda x: len(x), reverse = True)

calls = {}
def memo(f):
    global calls
    def m(*x):
        if not str([*x]) in calls: calls[str([*x])] = f(*x)
        return calls[str([*x])]
    return m

def possible(design):
    if design == "":
        return True
    matched = False
    for p in patterns:
        if len(p) > len(design): continue
        if design[:len(p)] == p:
            t = possible(design[len(p):])
            if t: matched = True
    if matched: return True
    return False
possible = memo(possible)

p = 0
for d in designs:
    if possible(d): p+=1

print(f"Part 1: {p}")

def possible2(design,count=0):
    if design == "":
        return 1
    for p in patterns:
        if len(p) > len(design): continue
        if design[:len(p)] == p:
            count += possible2(design[len(p):])
    return count
calls = {}
possible2 = memo(possible2)

c = 0
for d in designs:
    c += possible2(d)
print(f"Part 2: {c}")
