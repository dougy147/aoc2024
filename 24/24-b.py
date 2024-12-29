import copy

filepath = "../inputs/24.txt"

inputs = {} # and their initial values
connections = []

zs = [] # outputs
os = [] # others (intermediary)

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
            inputs[k] = v
        else:
            s = line.split(" ")
            gate = s[1]
            inps = (s[0],s[2])
            out  = s[4]
            if "x" in s[4]: xs.append(out)    # never happening
            elif "y" in s[4]: ys.append(out)  # never happening
            elif "z" in s[4]: zs.append(out)
            else: os.append(out)
            connections.append((inps,out,gate))
zs = sorted(zs)
os = sorted(os)

def compute_gate(inp1,inp2,gate,values):
    if gate == "XOR": return values[inp1] ^   values[inp2]
    if gate == "OR" : return values[inp1] |   values[inp2]
    if gate == "AND": return values[inp1] and values[inp2]

def compute(connections,inputs):
    conns = copy.deepcopy(connections)
    values = copy.deepcopy(inputs)
    while conns != []:
        q = conns.pop(0)
        conn = q
        inps, out, gate = conn
        inp1, inp2 = inps
        if not inp1 in values or not inp2 in values:
            conns.append(conn)
            continue
        else:
            values[out] = compute_gate(inp1,inp2,gate,values)
    return values

def find_implied(x,y):
    implied = {x,y}
    implied_conns = set()
    follow = []
    for (a,b), o, g in connections:
        if a == x and b == y or a == y or b == x:
            follow.append(o)
            implied.add(x)
            implied.add(y)
            implied.add(o)
            implied_conns.add(((a,b),o,g))
    while follow != []:
        f = follow.pop()
        for (a,b), o, g in connections:
            if a == f:
                if not b in implied:
                    follow.append(b)
                    implied.add(b)
                    implied_conns.add(((a,b),o,g))
            if b == f:
                if not a in implied:
                    follow.append(a)
                    implied.add(a)
                    implied_conns.add(((a,b),o,g))
    return implied_conns

def print_binary(values):
    binary=""
    for z in reversed(zs):
        if values[z]: binary+="1"
        elif not values[z]: binary+="0"
    print(binary)
    return binary

def in_binary(values):
    binary=""
    for z in reversed(zs):
        if values[z]: binary+="1"
        elif not values[z]: binary+="0"
    return binary

c = 0
for i in range(45):
    if i < 10: leading_zero = "0"
    else: leading_zero = ""
    x_k = "x" + leading_zero + str(i)
    y_k = "y" + leading_zero + str(i)
    curr_inputs = copy.deepcopy(inputs)
    for e in curr_inputs:
        curr_inputs[e] = False

    expected = ["0" for x in range(45+1)]
    expected[45-(i+1)] = "1"
    expected = ''.join(map(str,expected))

    ## 1 + 1
    curr_inputs[x_k] = v
    curr_inputs[y_k] = v

    # test this input
    values = compute(connections, curr_inputs)
    z_k0 = "z" + leading_zero + str(i+0)
    if i < 9: leading_zero = "0"
    else: leading_zero = ""
    z_k1 = "z" + leading_zero + str(i+1)

    if values[z_k0] != 0 or values[z_k1] != 1:   # 1 + 1
        if values[z_k0] != 0:
            print(f"[i={i}] problem with XOR {z_k0}?")
            print(find_implied(x_k,y_k))
            print_binary(values)
            print(expected)
            c+=1
        if values[z_k1] != 1:
            print(f"[i={i}] problem with AND {z_k1}?")
            print(find_implied(x_k,y_k))
            print_binary(values)
            print(expected)

c = 0
for i in range(11,45):
    x_k = "x" + str(i)
    y_k = "y" + str(i)
    curr_inputs = copy.deepcopy(inputs)
    for e in curr_inputs:
        curr_inputs[e] = False

    # 10 + 11
    curr_inputs["x"+str(i)] = False
    curr_inputs["x"+str(i+1)] = True
    curr_inputs["y"+str(i)] = True
    curr_inputs["y"+str(i+1)] = True

    # test this input
    values = compute(connections, curr_inputs)
    z_k0 = "z" + str(i+0)
    z_k1 = "z" + str(i+1)
    z_k2 = "z" + str(i+2)

    if i+2 >= 46: break

    if values[z_k0] != 1 or values[z_k1] != 0 or values[z_k2] != 1:   # 10 + 11
        if values[z_k0] != 1:
            print(f"[i={i}] problem with XOR {z_k0}?")
        if values[z_k1] != 0:
            print(f"[i={i}] problem with AND {z_k1}?")
        if values[z_k2] != 1:
            print(f"problem on {z_k2}")
    #else:
    #    print(f"ok for {i}")
