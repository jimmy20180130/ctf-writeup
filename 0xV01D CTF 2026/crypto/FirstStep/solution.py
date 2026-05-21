ciphertext = '723a147273063915710e01720f711d16721d0116043f'
key = 0x42

def xor_decrypt(ciphertext, key):
    decrypted = ''
    for i in range(0, len(ciphertext), 2):
        byte = int(ciphertext[i:i+2], 16)
        decrypted_byte = byte ^ key
        decrypted += chr(decrypted_byte)
    return decrypted

print(xor_decrypt(ciphertext, key))