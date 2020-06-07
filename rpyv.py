import sys
from cpu import CPU
from memory import Memory, MemoryMap
from vio import SimpleIO

def main():
    mem = Memory(32*1024*1024)
    high = Memory(32*1024*1024)
    m = MemoryMap([
        (0, mem),
        (0xffffffff - len(high) + 1, high),
        (40000000, SimpleIO()),
        ])
    with open(sys.argv[1], 'rb') as f:
        mem.write_bin(0, f.read())
    cpu = CPU(m, debug_trace=False)
    while not cpu.ebreak:
        cpu.step()
    print(cpu.regs)

if __name__ == '__main__':
    main()
