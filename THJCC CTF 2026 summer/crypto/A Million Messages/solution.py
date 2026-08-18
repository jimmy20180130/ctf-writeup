from types import SimpleNamespace
from attack import Bleichenbacher
from pwn import *

HOST, PORT = "chal.thjcc.org", 12003

io = remote(HOST, PORT)
n = int(io.recvline().split()[1], 16)
e = int(io.recvline().split()[1], 16)
c = bytes.fromhex(io.recvline().split()[1].decode())

class RemoteOracle:
    def Bits(self):
        return (n.bit_length() + 7) // 8 * 8

    def PublicKey(self):
        return SimpleNamespace(n=n, e=e)

    def Oracle(self, ciphertext):
        io.sendline(ciphertext.hex().encode())
        return io.recvline().strip() == b"OK"

log.success(Bleichenbacher(c, RemoteOracle()))
