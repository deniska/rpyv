import cpu

#32 bit 0b00000000000000000000000000000000

def test_dec_opcode():
    assert cpu.dec_opcode(
            0b00000000000000000000000001000001
            ) == 0b1000001

def test_dec_rd():
    assert cpu.dec_rd(
            0b00000000000000000000100010000000
            ) == 0b10001

def test_funct3():
    assert cpu.dec_funct3(
            0b00000000000000000101000000000000
            ) == 0b101

def test_rs1():
    assert cpu.dec_rs1(
            0b00000000000010001000000000000000
            ) == 0b10001

def test_rs2():
    assert cpu.dec_rs2(
            0b00000001000100000000000000000000
            ) == 0b10001

def test_funct7():
    assert cpu.dec_funct7(
            0b10000010000000000000000000000000
            ) == 0b1000001

def test_imm_I_pos():
    assert cpu.dec_imm_I(
            0b01000000000100000000000000000000
            ) == 0b10000000001

def test_imm_I_neg():
    assert cpu.dec_imm_I(
            0b11000001000100000000000000000000
            ) == 0b11111111111111111111110000010001

def test_imm_S_pos1():
    assert cpu.dec_imm_S(
            0b00000000000000000000100010000000
            ) == 0b10001

def test_imm_S_pos2():
    assert cpu.dec_imm_S(
            0b01000000000000000000000010000000
            ) == 0b10000000001

def test_imm_S_neg():
    assert cpu.dec_imm_S(
            0b10000000000000000000000010000000
            ) == 0b11111111111111111111100000000001

def test_imm_S_bit11_sign():
    assert cpu.dec_imm_S(
            0b10000000000000000000000000000000
            ) == 0b11111111111111111111100000000000

def test_imm_B_bit11():
    assert cpu.dec_imm_B(
            0b00000000000000000000000010000000
            ) == 0b100000000000

def test_imm_B_bit4_1():
    assert cpu.dec_imm_B(
            0b00000000000000000000100100000000
            ) == 0b10010

def test_imm_B_bit10_5():
    assert cpu.dec_imm_B(
            0b01000010000000000000000000000000
            ) == 0b10000100000

def test_imm_B_bit12_sign():
    assert cpu.dec_imm_B(
            0b10000000000000000000000000000000
            ) == 0b11111111111111111111000000000000

def test_imm_U():
    assert cpu.dec_imm_U(
            0b10000000000000000001000000011111
            ) == 0b10000000000000000001000000000000

def test_imm_J_bit19_12():
    assert cpu.dec_imm_J(
            0b00000000000010000001000000000000
            ) == 0b00000000000010000001000000000000

def test_imm_J_bit11():
    assert cpu.dec_imm_J(
            0b00000000000100000000000000000000
            ) == 0b00000000000000000000100000000000

def test_imm_J_bit10_1():
    assert cpu.dec_imm_J(
            0b01000000001000000000000000000000
            ) == 0b00000000000000000000010000000010

def test_imm_J_bit20_sign():
    assert cpu.dec_imm_J(
            0b10000000000000000000000000000000
            ) == 0b11111111111100000000000000000000
