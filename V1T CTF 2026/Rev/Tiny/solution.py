data = open("tini_rev", "rb").read()

words = [int.from_bytes(data[0x1B8 + 2 * i: 0x1BA + 2 * i], "little") for i in range(227)]
cnt   = data[0x37E]                  # 第一列的 segment 數
runs  = words[5: 5 + cnt - 1]        # 第一列的 run length（加密狀態）

s = (sum(runs) - 140) // (cnt - 1)
print(s)                             # 625