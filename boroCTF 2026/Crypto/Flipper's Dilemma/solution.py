s = "wzgzVASnS4|eE${J%`>h"

flag = ''.join(chr(ord(c) ^ 0x15) for c in s)

print(flag)