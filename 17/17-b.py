filepath = "../inputs/17.txt"

registers = []
reg = True
with open(filepath,"r") as f:
    for line in f.readlines():
        line = line.replace("\n","")
        if line == "":
            reg = False
            continue
        if reg:
            registers.append(int(line.split(":")[1]))
        else:
            vals = line.split(":")[1]
            program = list(map(int,vals.split(",")))

class Computer:
    def __init__(self,registers,program):
        self.A, self.B, self.C = registers[0],registers[1],registers[2]
        self.program = program
        self.pointer = 0
        self.halt = False
        self.load_instruction()
        self.output = []
        self.program_str = ''.join(map(str,self.program))
        self.quine_iteration = 0
    def combo(self, o):
        if 0 <= o and o <= 3: return o
        match o:
            case 4: return self.A
            case 5: return self.B
            case 6: return self.C
        assert 7 != o  # should fail else
    def load_instruction(self):
        if self.pointer >= len(self.program):
            self.halt = True
        else:
            self.opcode = self.program[self.pointer]      # instruction
            self.operand = self.program[self.pointer+1] # instruction input
    def execute(self):
        match self.opcode:
            case 0:
                num = self.A
                den = 2 ** self.combo(self.operand)
                self.A = num // den
            case 1:
                self.B = self.B ^ self.operand
            case 2:
                self.B = self.combo(self.operand) % 8
            case 3:
                if self.A != 0:
                    self.pointer = self.operand
                    self.load_instruction()
                    return
            case 4:
                self.B = self.B ^ self.C
            case 5:
                #print(self.combo(self.operand) % 8,end=',',flush=True)
                self.output.append(self.combo(self.operand) % 8) # always print register B modulo 8
            case 6:
                num = self.A
                den = 2 ** self.combo(self.operand)
                self.B = num // den
            case 7:
                num = self.A
                den = 2 ** self.combo(self.operand)
                self.C = num // den

        self.pointer += 2
        self.load_instruction()
    def run(self):
        while not self.halt:
            self.execute()
    def quine_urself(self):
        global registers
        while not self.halt:
            self.execute()
            if len(self.output) > 0:
                if not self.look_good_in_da_mirror():
                    self.reset()
                    self.A += self.quine_iteration
        else:
            if self.program_str != ''.join(map(str,self.output)):
                self.reset()
                self.A += self.quine_iteration
                self.quine_urself()
    def reset(self):
        self.output = []
        self.output_str = ""
        self.quine_iteration += 1
        self.A, self.B, self.C = registers[0],registers[1],registers[2]
        self.pointer = 0
        self.load_instruction()
        self.halt = False
    def print(self):
        print(','.join(map(str,self.output)))
    def look_good_in_da_mirror(self):
        output_str = ''.join(map(str,self.output))
        if self.program_str[:len(output_str)] != output_str:
            return False
        if self.program_str == output_str:
            self.halt = True
        return True

comp = Computer(registers,program)

## Part 2
# Looking at the program in reverse,
# it seemed to me that A was just
# divided by 8 at each step. :^)

#  Program  : [2, 4, 1, 1, 7, 5, 4, 7, 1, 4, 0, 3, 5, 5, 3, 0]
program_str = ''.join(map(str,comp.program))

cands = []
potential_A = {0,1,2,3,4,5,6,7} # by chance it worked, we need 8 values here
A=0
p8=1 # power of 8, increasing at each step
for i in range(len(comp.program)):
    AS = set()   # potential A's for next iteration
    for a in potential_A:
        for i in range(7+1): # iterations must be 7 here (again chance?)
            cand = a*8**p8 + i
            c = Computer([a,0,0],program)
            c.run()
            simulation_str = ''.join(map(str,c.output))
            if simulation_str == program_str:
                cands.append(a)
            elif simulation_str in program_str:
                AS.add(cand)
    potential_A = AS.copy()

print(f"Part 2: {min(cands)}")
