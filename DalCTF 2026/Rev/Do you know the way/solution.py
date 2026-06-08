import re
import subprocess

BIN = "./checker_unpacked"

asm = subprocess.check_output(
    ["objdump", "-d", "-M", "intel", BIN],
    text=True
)

def rol8(x, n):
    x &= 0xff
    n &= 7
    return ((x << n) | (x >> (8 - n))) & 0xff

def ror8(x, n):
    x &= 0xff
    n &= 7
    return ((x >> n) | (x << (8 - n))) & 0xff

def imm(x):
    return int(x, 16) & 0xffffffff

def check(block, c):
    eax = edx = esi = edi = 0

    for line in block:
        ins = line.split("\t")[-1].strip()

        if "movzx" in ins and "BYTE PTR [rax]" in ins:
            if ins.startswith("movzx  eax"):
                eax = c
            elif ins.startswith("movzx  edx"):
                edx = c

        elif ins == "movzx  eax,al":
            eax &= 0xff

        elif ins.startswith("mov    eax,edx"):
            eax = edx

        elif ins.startswith("mov    edi,eax"):
            edi = eax

        elif ins.startswith("mov    esi,0x"):
            esi = imm(ins.split(",")[1])

        elif ins.startswith("mov    edx,0x"):
            edx = imm(ins.split(",")[1])

        elif ins.startswith("add    eax,eax"):
            eax = (eax + eax) & 0xffffffff

        elif ins.startswith("add    eax,edx"):
            eax = (eax + edx) & 0xffffffff

        elif ins.startswith("add    eax,0x"):
            eax = (eax + imm(ins.split(",")[1])) & 0xffffffff

        elif ins.startswith("sub    eax,edx"):
            eax = (eax - edx) & 0xffffffff

        elif ins.startswith("sub    eax,0x"):
            eax = (eax - imm(ins.split(",")[1])) & 0xffffffff

        elif ins.startswith("xor    eax,0x"):
            eax = (eax ^ imm(ins.split(",")[1])) & 0xffffffff

        elif ins.startswith("shl    eax,0x"):
            eax = (eax << imm(ins.split(",")[1])) & 0xffffffff

        elif ins.startswith("not    eax"):
            eax = (~eax) & 0xffffffff

        elif "<rol8>" in ins:
            eax = rol8(edi, esi)

        elif "<ror8>" in ins:
            eax = ror8(edi, esi)

        elif ins == "cmp    al,dl":
            return (eax & 0xff) == (edx & 0xff)

    return False

flag = ""

for i in range(44):
    m = re.search(
        rf"^[0-9a-f]+ <f_{i}>:\n(.*?)(?=\n[0-9a-f]+ <)",
        asm,
        re.S | re.M
    )

    block = m.group(1).splitlines()

    for c in range(0x20, 0x7f):
        if check(block, c):
            flag += chr(c)
            break

print(flag)