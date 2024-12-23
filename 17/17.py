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
        print("Part 1:",','.join(map(str,self.output)))
    def look_good_in_da_mirror(self):
        output_str = ''.join(map(str,self.output))
        if self.program_str[:len(output_str)] != output_str:
            return False
        if self.program_str == output_str:
            self.halt = True
        return True

comp = Computer(registers,program)

# Part 1
comp.run()
comp.print()
