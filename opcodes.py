opcode_table = [
        (0b0110111, 'LUI', 'U', None, None),
        (0b0010111, 'AUIPC', 'U', None, None),
        (0b1101111, 'JAL', 'J', None, None),
        (0b1100111, 'JALR', 'I', 0b000, None),
        (0b1100011, 'BEQ', 'B', 0b000, None),
        (0b1100011, 'BNE', 'B', 0b001, None),
        (0b1100011, 'BLT', 'B', 0b100, None),
        (0b1100011, 'BGE', 'B', 0b101, None),
        (0b1100011, 'BLTU', 'B', 0b110, None),
        (0b1100011, 'BGEU', 'B', 0b111, None),
        (0b0000011, 'LB', 'I', 0b000, None),
        (0b0000011, 'LH', 'I', 0b001, None),
        (0b0000011, 'LW', 'I', 0b010, None),
        (0b0000011, 'LBU', 'I', 0b100, None),
        (0b0000011, 'LHU', 'I', 0b101, None),
        (0b0100011, 'SB', 'S', 0b000, None),
        (0b0100011, 'SH', 'S', 0b001, None),
        (0b0100011, 'SW', 'S', 0b010, None),
        (0b0010011, 'ADDI', 'I', 0b000, None),
        (0b0010011, 'SLTI', 'I', 0b010, None),
        (0b0010011, 'SLTIU', 'I', 0b011, None),
        (0b0010011, 'XORI', 'I', 0b100, None),
        (0b0010011, 'ORI', 'I', 0b110, None),
        (0b0010011, 'ANDI', 'I', 0b111, None),
        (0b0010011, 'SLLI', 'I', 0b001, 0b0000000),
        (0b0010011, 'SRLI', 'I', 0b101, 0b0000000),
        (0b0010011, 'SRAI', 'I', 0b101, 0b0100000),
        (0b0110011, 'ADD', 'R', 0b000, 0b0000000),
        (0b0110011, 'SUB', 'R', 0b000, 0b0100000),
        (0b0110011, 'SLL', 'R', 0b001, 0b0000000),
        (0b0110011, 'SLT', 'R', 0b010, 0b0000000),
        (0b0110011, 'SLTU', 'R', 0b011, 0b0000000),
        (0b0110011, 'XOR', 'R', 0b100, 0b0000000),
        (0b0110011, 'SRL', 'R', 0b101, 0b0000000),
        (0b0110011, 'SRA', 'R', 0b101, 0b0100000),
        (0b0110011, 'OR', 'R', 0b110, 0b0000000),
        (0b0110011, 'AND', 'R', 0b111, 0b0000000),
        (0b0001111, 'FENCE', 'I', 0b000, None),
        (0b1110011, 'ECALL', 'I', 0b000, None),
        (0b1110011, 'EBREAK', 'I', 0b000, None),
        ]

opcode_types = {}
opcodes = {}
for opcode, name, type, f3, f7 in opcode_table:
    opcode_types[opcode] = type
    if type == 'R':
        opcodes[opcode, f3, f7] = name
    elif type in 'ISB':
        opcodes[opcode, f3] = name
    elif type in 'UJ':
        opcodes[opcode] = name
    else:
        raise ValueError(f'Unknown opcode type {type}')
