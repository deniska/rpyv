import memory

def test_ram():
    mem = memory.Memory(1024)
    mem.write8(5, 100)
    assert mem.read8(5) == 100
