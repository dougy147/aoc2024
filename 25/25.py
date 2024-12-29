filepath = "../inputs/25.txt"

locks = []
keys = []
new_key = True
key = False
current_key = []
with open(filepath,"r") as f:
    for line in f.readlines():
        line = line.replace("\n","")
        if line == "":
            new_key = True
            if key: keys.append(current_key)
            else: locks.append(current_key)
            current_key = []
            continue
        if new_key and "#" in line: key = False
        if new_key and "." in line: key = True
        if new_key:
            new_key = False
            tmp = []
            for l in line:
                tmp.append(l)
            current_key.append(tmp)
        else:
            tmp = []
            for l in line:
                tmp.append(l)
            current_key.append(tmp)
if key: keys.append(current_key)
else: locks.append(current_key)

def key_to_heights(key):
    key_heights = [0 for _ in range(len(key[0]))]
    for r in range(len(key)-1): # -1 because don't count last line
        for c in range(len(key[r])):
            if key[r][c] == "#":
                key_heights[c]+=1
    return key_heights

def lock_to_heights(lock):
    lock_heights = [0 for _ in range(len(lock[0]))]
    for r in range(1,len(lock)): # -1 because don't count last line
        for c in range(len(lock[r])):
            if lock[r][c] == "#":
                lock_heights[c]+=1
    return lock_heights

locks_h = []
keys_h = []
for l in locks:
    locks_h.append(lock_to_heights(l))
for k in keys:
    keys_h.append(key_to_heights(k))

def fit(lock,key):
    # on heights
    if len(lock) != len(key):
        print("Not same col length key and lock!")
        exit()
    for i in range(len(lock)):
        if lock[i] + key[i] > 5: return False
    return True

c=0
for l in locks_h:
    for k in keys_h:
        if fit(l,k): c+=1
print(c)
