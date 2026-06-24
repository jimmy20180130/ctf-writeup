encoded_flag = [
    0xDA, 0xA1, 0xB5, 0xAD, 0xA4, 0xA8, 0x9B, 0xA0, 0xDF,
    0x88, 0x96, 0xDF, 0x80, 0x30, 0x91, 0x55, 0x68, 0x3A,
    0x7F, 0x7C, 0x1A, 0x58, 0x57, 0x75, 0x42, 0x70, 0x4C,
    0x32, 0x79, 0x28, 0x6B, 0x2E, 0x1A, 0, 0
]


obfuscated_phrase = [
    0x7F, 0x43, 0x5E, 0x25, 0x37, 0x11, 0xEF, 0xF6, 0xD0,
    0xCD, 0xAB, 0xB5
]

# __int64 __fastcall mask_for(char a1)
# {
#   return (unsigned __int8)(17 * a1 + 27);
# }
def mask_for(a1):
    return (17 * a1 + 27) & 0xff # & 0xff 是因為它只會返回 int8

# __int64 __fastcall build_expected_phrase(__int64 result)
# {
#   char v1; // [xsp+Ch] [xbp-14h]
#   unsigned __int64 i; // [xsp+10h] [xbp-10h]
#   __int64 v3; // [xsp+18h] [xbp-8h]

#   v3 = result;
#   for ( i = 0; i < 0xC; ++i )
#   {
#     v1 = obfuscated_phrase[i];
#     result = mask_for(i);
#     *(_BYTE *)(v3 + i) = v1 ^ result;
#   }
#   *(_BYTE *)(v3 + 12) = 0;
#   return result;
# }
def build_expected_phrase():
    result = [0] * 13
    for i in range(12):
        v1 = obfuscated_phrase[i]
        result[i] = (v1 ^ mask_for(i)) & 0xff
    result[12] = 0
    return result

# __int64 __fastcall compute_grid_offset(__int64 a1)
# {
#   __int64 i; // [xsp+8h] [xbp-18h]
#   int v3; // [xsp+14h] [xbp-Ch]

#   v3 = 0;
#   for ( i = 0; *(_BYTE *)(a1 + i); ++i )
#     v3 += *(unsigned __int8 *)(a1 + i) * (i + 3);
#   return (unsigned int)(v3 % 1000 + 200);
# }
def compute_grid_offset(a1):
    v3 = 0
    i = 0
    while a1[i] != 0:
        v3 += a1[i] * (i + 3)
        i += 1
    return v3 % 1000 + 200

expected_phrase = build_expected_phrase()
v4 = compute_grid_offset(expected_phrase)

print("phrase:", bytes(expected_phrase[:-1]).decode())
print("window:", v4)

# __int64 __fastcall print_flag(__int64 a1, char a2)
# {
#   unsigned __int64 i; // [xsp+18h] [xbp-48h]
#   char v4[34]; // [xsp+36h] [xbp-2Ah] BYREF

#   for ( i = 0; i < 0x21; ++i )
#     v4[i] = encoded_flag[i] ^ (5 * i + *(_BYTE *)(a1 + i % 0xC) + a2);
#   v4[33] = 0;
#   puts("Docking accepted. Flag:");
#   return puts(v4);
# }

flag = []
for i in range(0x21):
    key = (5 * i + expected_phrase[i % 12] + v4) & 0xff # AND 0xff 是因為 v4 是 char (int8)
    flag.append(encoded_flag[i] ^ key)

print("flag:", bytes(flag).decode())