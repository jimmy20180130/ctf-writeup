# Babel's Vault

## 題目描述

My friend sent me a random codebase with a Library of Babel implementation. Apparently the author is well known to hide secrets in his code, but I don't see any here.

## 解題思路

1. **第一步**：

    先看題目給的`babel.py`：

    `page_from_seed()` 會把seed加上一個很大的offset，然後轉成base55文字。

    ```python
    def page_from_seed(seed: int):
        seed += OFFSET
        chars = []
        for _ in range(940):
            seed, remainder = divmod(seed, 55)
            chars.append(ALPHABET[remainder])
        return "".join(chars)
    ```

    `image_from_seed()` 會把seed減去另一個很大的offset，然後轉成15x15的RGB圖片。

    ```python
    def image_from_seed(seed: int):
        seed -= OFFSET_IMAGE
        pixels = []
        for _ in range(225):
            seed, r = divmod(seed, 256)
            seed, g = divmod(seed, 256)
            seed, b = divmod(seed, 256)
            pixels.append((r, g, b))
        return pixels
    ```

    所以我們可以利用這兩個功能來找flag。

2. **第二步**：

    在 `page_from_seed()` 裡，會固定產生940個字元的page，並且 `AUTHORSNOTE.txt` 的內容剛好也是940個字元。

    這代表作者筆記應該不是普通文字，而是一個由 `page_from_seed()` 生成出來的page。

    因此我們可以逆向推導：

    ```text
    作者筆記 -> base55整數 -> 原本的seed
    ```

    `page_from_seed()` 的轉換方式是little-endian base55：

    ```python
    seed, remainder = divmod(seed, 55)
    chars.append(ALPHABET[remainder])
    ```

    所以反向計算時，第 i 個字元代表第 i 位數：

    ```text
    ALPHABET.index(ch) * 55^i
    ```

    python寫法：

    ```python
    def text_to_seed_value(s):
        n = 0
        mul = 1

        for ch in s:
            n += alphabet.index(ch) * mul
            mul *= 55

        return n
    ```

    因為 `page_from_seed(seed)` 一開始會先加上offset，所以在算出seed後，要記得把offset減掉：

    ```python
    seed = text_to_seed_value(text) - offset
    ```

3. **第三步**：

    算出seed後，把seed給 `image_from_seed()`，把數字轉成RGB pixels：

    ```python
    seed, r = divmod(seed, 256)
    seed, g = divmod(seed, 256)
    seed, b = divmod(seed, 256)
    pixels.append((r, g, b))
    ```

    得到的pixels中，很多都是 `(0, 0, 0)`，而有效的 pixels 都長得像：

    ```text
    (0, 0, 7)
    (0, 1, 6)
    (0, 3, 5)
    ...
    ```

    這些RGB值不像真正的顏色，比較像是三位數index，例如(0, 0, 7)代表第7位：

    ```text
    (0, 0, 7) -> 007
    (0, 1, 6) -> 016
    (0, 3, 5) -> 035
    ```

    因此可以把每個非零pixel轉成位置：

    ```python
    pos = 100 * r + 10 * g + b
    ```

    然後用這些位置回去讀 `AUTHORSNOTE.txt` 的字元。

4. **第四步**：

    有了這些index值，就可以寫一段程式來取index對應的字元：

    ```python
    positions = []

    for r, g, b in pixels:
        if (r, g, b) != (0, 0, 0):
            pos = 100 * r + 10 * g + b
            positions.append(pos)

    hidden = "".join(text[pos] for pos in positions)
    ```

    執行腳本後就可以得到：

    ```text
    boroCTFoneSeedCipherInInfinity
    ```

    補上{}就可以拿到flag。

## Flag

```text
boroCTF{oneSeedCipherInInfinity}
```
