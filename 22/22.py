filepath = "../inputs/22.txt"

secrets = ()
with open(filepath,"r") as f:
    for line in f.readlines():
        line = line.replace("\n","")
        secrets += (int(line),)

def mix(n,secret):
    return n ^ secret

def prune(secret):
    return secret % (16 ** 6)

def process(secret):
    # step 1
    x = secret * 64
    secret = mix(x,secret)
    secret = prune(secret)
    # step 2
    x = secret // 32
    secret = mix(x,secret)
    secret = prune(secret)
    # step 3
    x = secret * 2048
    secret = mix(x,secret)
    secret = prune(secret)
    return secret

iterate = 2000
res = 0
for s in secrets:
    for i in range(iterate):
        s = process(s)
    res+=s
print(f"Part 1: {res}")

iterate = 2000
seqs = {}
for i in range(len(secrets)):
    init = secrets[i]
    s = secrets[i]
    changes=()
    my_seqs = set()
    for i in range(iterate):
        ns = process(s)
        lns = int(str(ns)[len(str(ns))-1])
        ls = int(str(s)[len(str(s))-1])
        changes+=(lns - ls,)
        if len(changes) >= 4:
            seq = changes[-4:]
            if not seq in my_seqs:
                my_seqs.add(seq)
                if not seq in seqs:
                    seqs[seq] = (lns,)
                else:
                    seqs[seq]+=(lns,)

        s = ns

best_deals = 0
for s in seqs:
    if sum(seqs[s]) > best_deals:
        best_deals = sum(seqs[s])
print(f"Part 2: {best_deals}")
