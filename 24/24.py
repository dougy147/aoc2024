filepath = "../inputs/24.txt"

wires = {} # and their initial values
connections = []
zs = []

parsing_wires = True
with open(filepath,"r") as f:
    for line in f.readlines():
        line = line.replace("\n","")
        if line == "":
            parsing_wires = False
            continue
        if parsing_wires:
            k,v = line.split(":")
            if int(v) == 1: v = True
            elif int(v) == 0: v = False
            else: raise "Error"
            wires[k] = v
        else:
            s = line.split(" ")
            gate = s[1]
            triplet = (s[0],s[2],s[4])
            if "z" in s[4]:
                zs.append(s[4])
            connections.append((triplet,gate))
zs = sorted(zs)

def compute(inp1,inp2,gate):
    if gate == "XOR": return wires[inp1] ^   wires[inp2]
    if gate == "OR" : return wires[inp1] |   wires[inp2]
    if gate == "AND": return wires[inp1] and wires[inp2]

# Part 1
while connections != []:
    q = connections.pop(0)
    conn = q
    triplet, gate = conn
    inp1, inp2, out = triplet
    if not inp1 in wires or not inp2 in wires:
        connections.append(conn)
        continue
    else:
        wires[out] = compute(inp1,inp2,gate)

binary = ""
for z in reversed(zs):
    if wires[z]: binary+="1"
    elif not wires[z]: binary+="0"
    else: raise "Z not computed"
print("Part 1:",int(binary,2))
