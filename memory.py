class Memory:

    def __init__(self, size):
        self.mem = bytearray(size)
        self.bin_size = 0

    def read8(self, addr):
        val = self.mem[addr]
        #if addr > self.bin_size:
        #    print(f'Read {val:02x} at {addr}')
        return val

    def write8(self, addr, val):
        self.mem[addr] = val

    def write_bin(self, addr, data):
        self.mem[addr: addr+len(data)] = data
        self.bin_size = addr + len(data)

    def __len__(self):
        return len(self.mem)


class MemoryMap:

    def __init__(self, mems):
        self.mems = mems

    def resolve_addr(self, addr):
        for start, m in self.mems:
            if start <= addr < start + len(m):
                return m, start
        raise IndexError(f'Access to unmapped memory {addr:x}')

    def read8(self, addr):
        mem, start = self.resolve_addr(addr)
        val = mem.read8(addr - start)
        #print(f'Read {val:x} at {addr}')
        return val

    def write8(self, addr, val):
        #print(f'Write {val:x} at {addr}')
        mem, start = self.resolve_addr(addr)
        mem.write8(addr - start, val)


