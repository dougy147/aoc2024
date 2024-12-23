filepath = "../inputs/23.txt"

ports = {}
with_t = set()

with open(filepath,"r") as f:
    for line in f.readlines():
        line = line.replace("\n","")
        left, right = line.split("-")
        if not left in ports:
            ports[left] = (right,)
        else:
            ports[left] += (right,)
        if left[0] == "t": with_t.add(left)
        # for symmetry
        if not right in ports:
            ports[right] = (left,)
        else:
            ports[right] += (left,)

def cliques_of_three(ports):
    cliques = set()
    for p1 in ports:
        for p2 in ports:
            if p1 == p2: continue
            if not p2 in ports[p1] or not p1 in ports[p2]: continue
            for p in ports:
                if p == p1 or p == p2 : continue
                if p in ports[p1] and p in ports[p2]:
                    triplet = tuple(sorted((p,p1,p2)))
                    if not triplet in cliques:
                        cliques.add(triplet)
    return cliques

res = 0
for x in cliques_of_three(ports):
    if "'t" in str(x): res+=1
print(f"Part 1: {res}")

vertices = []
for p in ports:
    vertices.append(p)


cliques = set()

def find_cliques(vertex, css = None, taken = None):
    if css == None: css = []
    if taken == None: taken = []
    # find all the cliques of a given vertex
    cs = (vertex,)
    for v in vertices:
        if v == vertex or v in taken: continue
        if v in ports[vertex]:
            match = True
            for c in cs:
                if not c in ports[v]:
                    match = False
                    break
            if not match:
                if cs != []:
                    css.append(tuple(sorted(cs)))
                    cliques.add(cs)
                find_cliques(vertex, css, taken)
                continue
            cs+=(v,)
            taken.append(v)
    if cs != () and not cs in css:
        css.append(tuple(sorted(cs)))
    for c in css:
        cliques.add(c)
    return css

max_len = 0
candidates = set()
for v in vertices:
    clique = find_cliques(v)
    clique_length = len(max(clique,key=len))
    if clique_length > max_len:
        max_len = clique_length
        candidates = { max(clique,key=len) }
    elif clique_length == max_len:
        candidates.add(max(clique,key=len))
for c in candidates:
    print("Part 2:",','.join(map(str,c)))
