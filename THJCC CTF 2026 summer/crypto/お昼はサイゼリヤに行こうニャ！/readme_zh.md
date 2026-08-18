# お昼はサイゼリヤに行こうニャ！

## 題目描述

「あのメモ？　巻いて吸っちゃったニャ。これじゃお昼も行けないニャ」 残ったのは当時のスクリプトと、大家さんが作っておいたテーブルだけ。

![alt text](image.png)

## 解題思路

`gen_table.py` 產的是標準 rainbow table，密碼是 `yaniko` 六個字母、長度 14（6^14 ≈ 2^36），雜湊是自製的 40-bit ARX `yani40(msg, K)`，reduction function `reduce_at(h, i)` 吃步數 `i`，鏈長 24576、鏈頭固定是 `idx_to_pw(c)`、共 `6^14 // 24576 = 3188646` 條，表裡只存鏈尾密碼前 8 個字母壓成的 21-bit 值

```python
def build_table(K, path="nyan.tbl"):
    acc = n = 0
    buf = bytearray()
    for c in range(NUM_CHAINS):
        acc |= pw_to_val(walk(idx_to_pw(c), CHAIN_LEN, K)) << n
        n += ENDBITS
        while n >= 8:
            buf.append(acc & 0xFF)
            acc >>= 8
            n -= 8
```

種子同時決定表和 shadow，得先湊回來。住戶是《尼古喵喵》的角色，年紀是公開設定，菸子 21、藥子 20、酒子 24，性子的頻道截圖寫 10.8 万 = 108000。鏈頭固定，所以填對的話第 0 條鏈走滿 24576 步的鏈尾就等於 `nyan.tbl` 開頭那 21 個 bit，這就是房東說的「那張表自己會告訴你」，懶得查設定的話三個年紀直接 1..99 暴搜，用同一個自檢撈也行

剩下是課本上的 rainbow table lookup，唯一要注意的是表尾只存 8 個字母（1679616 種）卻有 3188646 條鏈，平均一個值撞到 1.9 條，回頭重走驗證的量比查詢本身還大，兩段都得批次跑

Exploit:

1. `K = (21, 20, 24, 108000)`，走第 0 條鏈的鏈尾比對 `nyan.tbl` 前 21 個 bit 自檢
2. 對每個 shadow 雜湊 `H`，把 24576 個 `j` 當成 lane 一起往前走，lane `j` 從 `reduce_at(H, j)` 出發走第 `j+1..24575` 步，走到第 `i` 步時活著的 lane 剛好是 `j < i` 這段前綴
3. 每條 lane 的鏈尾值去表裡撈出命中的鏈，得到候選 `(鏈 c, j)`，依 `j` 排序後從鏈頭一起重走，走到第 `j` 步就驗 `yani40(pw) == H`，中的就是密語
4. `key = sha256("|".join(五個密語))`，`flag.enc` 前 16 bytes 是 HMAC tag，其餘用 `sha256(key + b"YANI-CTR" + counter)` 當 keystream XOR 回來就是 flag

## Flag

```text
THJCC{46Z-WQv_vFc}
```
