import collections
import sys

class SimpleIO:

    def __init__(self):
        self.buf = collections.deque()

    def read8(self, addr):
        if not self.buf:
            self.buf += input('> ').encode('utf-8')
        return buf.popleft()

    def write8(self, addr, val):
        sys.stdout.buffer.write(bytes([val]))

    def __len__(self):
        return 1
