from opcodes import opcodes, opcode_types

class CPU:

    def __init__(self, mem, *, debug_trace=False):
        self.mem = mem
        self.regs = [0]*31
        self.pc = 0
        self.debug_trace = debug_trace
        self.ebreak = False

    def read_reg(self, reg):
        if reg == 0:
            return 0
        return self.regs[reg - 1]

    def write_reg(self, reg, val):
        if reg == 0:
            return
        self.regs[reg - 1] = val

    def step(self):
        #ins = self.mem.read32(self.pc)
        ins = (self.mem.read8(self.pc)
                | self.mem.read8(self.pc+1) << 8
                | self.mem.read8(self.pc+2) << 16
                | self.mem.read8(self.pc+3) << 24)
        opcode = dec_opcode(ins)
        optype = opcode_types[opcode]

        imm = 0
        if optype in imms:
            imm = imms[optype](ins)

        rd = dec_rd(ins)

        rs1 = 0
        if optype in 'RISB':
            rs1 = dec_rs1(ins)

        rs2 = 0
        if optype in 'RSB':
            rs2 = dec_rs2(ins)

        f3 = 0
        f7 = 0
        try:
            if optype == 'R':
                f3 = dec_funct3(ins)
                f7 = dec_funct7(ins)
                opname = opcodes[opcode, f3, f7]
            elif optype in 'ISB':
                f3 = dec_funct3(ins)
                opname = opcodes[opcode, f3]
            elif optype in 'UJ':
                opname = opcodes[opcode]
        except KeyError:
            raise NotImplementedError(f'Unknown opcode {opcode:07b}')
        try:
            func = getattr(self, f'op_{opname}')
        except AttributeError:
            raise NotImplementedError(f'Not implemented {opname}')

        if optype == 'R':
            result = func(self.read_reg(rs1), self.read_reg(rs2))
            self.write_reg(rd, result)
            self.trace(f'{opname} x{rd}, x{rs1}, x{rs2}')
        elif optype == 'I':
            result = func(self.read_reg(rs1), imm)
            self.write_reg(rd, result)
            simm = signed32(imm)
            self.trace(f'{opname} x{rd}, x{rs1}, {simm}')
        elif optype in 'SB':
            func(self.read_reg(rs1), self.read_reg(rs2), imm)
            simm = signed32(imm)
            self.trace(f'{opname} x{rs1}, x{rs2}, {simm}')
        elif optype in 'UJ':
            result = func(imm)
            self.write_reg(rd, result)
            simm = signed32(imm)
            self.trace(f'{opname} x{rd}, {simm}')
        #self.trace(f'[pc={self.pc:x}] {self.regs}')

    def trace(self, s):
        if self.debug_trace:
            print(s)

    def op_LUI(self, imm):
        self.pc += 4
        return imm

    def op_AUIPC(self, imm):
        pc = self.pc
        self.pc += 4
        return (imm + pc) % mask32

    def op_ADDI(self, rs1, imm):
        self.pc += 4
        return (rs1 + imm) & mask32

    def op_ANDI(self, rs1, imm):
        self.pc += 4
        return (rs1 & imm) & mask32

    def op_ADD(self, rs1, rs2):
        self.pc += 4
        return (rs1 + rs2) & mask32

    def op_SUB(self, rs1, rs2):
        self.pc += 4
        return (rs1 - rs2) & mask32

    def op_EBREAK(self, rs1, imm):
        self.pc += 4
        self.ebreak = True

    def op_JAL(self, imm):
        ret = self.pc + 4
        self.pc = (self.pc + imm) & mask32
        return ret & mask32

    def op_JALR(self, rs1, imm):
        ret = self.pc + 4
        self.pc = (rs1 + imm) & (mask32 - 1)
        return ret & mask32

    def op_BGEU(self, rs1, rs2, imm):
        if rs1 >= rs2:
            self.pc = (self.pc + imm) & mask32
        else:
            self.pc += 4

    def op_BEQ(self, rs1, rs2, imm):
        if rs1 == rs2:
            self.pc = (self.pc + imm) & mask32
        else:
            self.pc += 4

    def op_BNE(self, rs1, rs2, imm):
        if rs1 != rs2:
            self.pc = (self.pc + imm) & mask32
        else:
            self.pc += 4

    def op_BGE(self, rs1, rs2, imm):
        if signed32(rs1) >= signed32(rs2):
            self.pc = (self.pc + imm) & mask32
        else:
            self.pc += 4

    def op_BLTU(self, rs1, rs2, imm):
        if rs1 < rs2:
            self.pc = (self.pc + imm) & mask32
        else:
            self.pc += 4

    def op_BLT(self, rs1, rs2, imm):
        if signed32(rs1) < signed32(rs2):
            self.pc = (self.pc + imm) & mask32
        else:
            self.pc += 4

    def op_SB(self, rs1, rs2, imm):
        self.pc += 4
        addr = (rs1 + imm) & mask32
        self.mem.write8(addr, rs2 & 0xFF)

    def op_SW(self, rs1, rs2, imm):
        self.pc += 4
        addr = (rs1 + imm) & mask32
        self.mem.write8(addr, rs2 & 0xFF)
        self.mem.write8(addr+1, (rs2>>8) & 0xFF)
        self.mem.write8(addr+2, (rs2>>16) & 0xFF)
        self.mem.write8(addr+3, (rs2>>24) & 0xFF)

    def op_LB(self, rs1, imm):
        self.pc += 4
        addr = (rs1 + imm) & mask32
        val = self.mem.read8(addr)
        sign = (val >> 7) * 0b11111111111111111111111110000000
        return val | sign

    def op_LBU(self, rs1, imm):
        self.pc += 4
        addr = (rs1 + imm) & mask32
        val = self.mem.read8(addr)
        return val

    def op_LW(self, rs1, imm):
        self.pc += 4
        addr = (rs1 + imm) & mask32
        val = (self.mem.read8(addr)
                | self.mem.read8(addr+1) << 8
                | self.mem.read8(addr+2) << 16
                | self.mem.read8(addr+3) << 24)
        return val

mask32 = 0xFFFFFFFF

def signed32(n):
    if not (n & 0b10000000000000000000000000000000):
        return n
    return n + ~mask32

def dec_opcode(ins):
    return ins & 0b1111111

def dec_rd(ins):
    return (ins >> 7) & 0b11111

def dec_funct3(ins):
    return (ins >> 12) & 0b111

def dec_rs1(ins):
    return (ins >> 15) & 0b11111

def dec_rs2(ins):
    return (ins >> 20) & 0b11111

def dec_funct7(ins):
    return ins >> 25

def dec_imm_I(ins):
    sign = ins >> 31
    return (ins >> 20) | ((((1<<20)-1) * sign) << 12)

def dec_imm_S(ins):
    sign = ins >> 31
    return (((ins >> 7) & 0b11111)
            | (((ins >> 25) & 0b1111111) << 5)
            | (((1<<21)-1) * sign << 11))

def dec_imm_B(ins):
    sign = ins >> 31
    imm11 = (ins >> 7) & 0b1
    imm4_1 = (ins >> 8) & 0b1111
    imm10_5 = (ins >> 25) & 0b111111
    imm12 = ((1<<20)-1) * sign
    return ((imm4_1 << 1)
            | (imm10_5 << 5)
            | (imm11 << 11)
            | (imm12 << 12))

def dec_imm_U(ins):
    return ins & 0b11111111111111111111000000000000

def dec_imm_J(ins):
    sign = ins >> 31
    imm19_12 = (ins >> 12) & 0b11111111
    imm11 = (ins >> 20) & 0b1
    imm10_1 = (ins >> 21) & 0b1111111111
    imm20 = ((1<<12)-1) * sign
    return ((imm10_1 << 1)
            | (imm11 << 11)
            | (imm19_12 << 12)
            | (imm20 << 20))

imms = {
        'I': dec_imm_I,
        'S': dec_imm_S,
        'B': dec_imm_B,
        'U': dec_imm_U,
        'J': dec_imm_J,
        }
