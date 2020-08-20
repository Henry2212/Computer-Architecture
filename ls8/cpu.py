"""CPU functionality."""

import sys

# Instructions
LDI = 0b10000010 
PRN = 0b01000111    # Print
HLT = 0b00000001    # Halt
MUL = 0b10100010    # Multiply
ADD = 0b10100000    # Addition
PUSH = 0b01000101   # Push in stack
POP = 0b01000110    # Pop from stack

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.pc = 0
        self.running = True

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value
    
    def hlt(self):
        self.running = False
        self.pc += 1
    
    def ldi(self, reg_num, value):
        self.reg[reg_num] = value
        self.pc += 3

    def prn(self, reg_num):
        print(self.reg[reg_num])
        self.pc += 2
    
    def load(self):
        """Load a program into memory."""
        self.address = 0
        
        if len(sys.argv) < 2:
            print("Error: Insufficient arguments. Add a file from example folder into run command as arg[1]")
            sys.exit(0)
        
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.strip()
                    temp = line.split()
        
                    if len(temp) == 0:
                        continue
        
                    if temp[0][0] == '#':
                        continue
        
                    try:
                        self.ram[self.address] = int(temp[0], 2)
        
                    except ValueError:
                        print(f"Invalid number: {temp[0]}")
                        sys.exit(1)
        
                    self.address += 1
        
        except FileNotFoundError:
            print(f"Couldn't open {sys.argv[1]}")
            sys.exit(2)
        
        if self.address == 0:
            print("Program was empty!")

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # load the instructions file
        self.load()
        while self.running:
            instruction_register = self.ram[self.pc]
            reg_a = self.ram[self.pc+1]
            reg_b = self.ram[self.pc+2]

            if instruction_register == HLT:
                self.hlt()
            
            elif instruction_register == LDI:
                self.ldi(reg_a, reg_b)
            
            elif instruction_register == PRN:
                self.prn(reg_a)
            
            elif instruction_register == ADD:
                self.alu("ADD", reg_a, reg_b)
                self.pc += 3
            
            elif instruction_register == MUL:
                self.alu("MUL", reg_a, reg_b)
                self.pc += 3
            
            elif instruction_register == PUSH:
                # decrement stack pointer
                self.reg[7] -= 1

                # get the value from a given register
                # reg_a = self.ram[self.pc+1]
                value = self.reg[reg_a]

                # put it on the stack pointer address
                sp = self.reg[7]
                self.ram[sp] = value

                # increment pc
                self.pc += 2

            elif instruction_register == POP:
                # get the tack pointer
                sp = self.reg[7]
                # get register number to put value in
                # reg_a = self.ram[self.pc+1]

                # use stack pointer to get the value
                value = self.ram[sp]
                # put the value into a given register
                self.reg[reg_a] = value

                # increment stack pointer
                self.reg[7] += 1
                # increment program counter
                self.pc += 2
            
            else:
                print(f"Instruction number {self.pc} not recognized!")
                self.pc += 1