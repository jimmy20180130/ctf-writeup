#!/usr/bin/env python3
import zlib

CIPHER_FLAG = bytes.fromhex(
    "72901442adade9c53b7cb386eeb8b6765d42dbc58ec6d442"
    "e77057b7d5d2724afc2f4e232df02f9ff050"
)

LEAK1 = [123, 38, 92, 78, 207, 178, 116, 75, 141, 163]
LEAK2 = [4226, 36575, 42265, 42988, 32134, 53660, 36202, 48971, 61905, 20150, 45745]
LEAK3 = [10, 18, 13, 17, 17, 19, 14, 13, 18, 16, 15]
PARTIAL_CRC = 0x32C29A97

M1 = 0x9E3779B1
M2 = 0x045D9F3B


def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def printable(data):
    return all(0x20 <= x <= 0x7e for x in data)


def leak1_value(w1, w2):
    return (((w1 ^ w2) * M1) >> 24) & 0xff


def pos_word(i):
    target_l2 = LEAK2[i]
    target_l3 = LEAK3[i]
    ct = CIPHER_FLAG[i * 4:(i + 1) * 4]

    result = []

    for lo in range(1 << 16):
        hi = target_l2 ^ ((lo * M2) & 0xffff)
        word = (hi << 16) | lo

        if word.bit_count() != target_l3:
            continue

        ks = word.to_bytes(4, "big")[:len(ct)]
        pt = xor_bytes(ct, ks)

        if printable(pt):
            result.append((word, pt))

    return result


def main():
    word_count = len(LEAK2)
    candidates = [pos_word(i) for i in range(word_count)]

    first_word = int.from_bytes(xor_bytes(CIPHER_FLAG[:4], b"V1T{"), "big")

    frontier = [
        (word, b"V1T{", [word])
        for word, pt in candidates[0]
        if word == first_word and pt == b"V1T{"
    ]

    for i in range(word_count - 1):
        new_frontier = []

        for prev_word, recovered, words in frontier:
            for cur_word, cur_pt in candidates[i + 1]:
                if leak1_value(prev_word, cur_word) != LEAK1[i]:
                    continue

                candidate_plain = recovered + cur_pt

                if len(candidate_plain) >= 16:
                    if zlib.crc32(candidate_plain[:16]) != PARTIAL_CRC:
                        continue

                new_frontier.append(
                    (cur_word, candidate_plain, words + [cur_word])
                )

        frontier = new_frontier

    solutions = [
        plain
        for _, plain, _ in frontier
        if plain.startswith(b"V1T{") and plain.endswith(b"}")
    ]

    assert len(solutions) == 1
    print(solutions[0].decode())


if __name__ == "__main__":
    main()