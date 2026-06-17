def rot_minus_3(s):
    result = ""

    for ch in s:
        if "a" <= ch <= "z":
            result += chr((ord(ch) - ord("a") - 3) % 26 + ord("a"))
        elif "A" <= ch <= "Z":
            result += chr((ord(ch) - ord("A") - 3) % 26 + ord("A"))
        else:
            result += ch

    return result


cipher = "erurFWI{@iu13qgq0pru3}"
plain = rot_minus_3(cipher)

print(plain)