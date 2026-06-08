# Lost My Flag Printer

## 題目描述

Have you ever locked your keys in your car? Log in with user `ebpf` and an empty password.

## 解題思路

登入後先簡單找了一下 flag，但都沒有找到，後來發現根目錄底下有一個名為 `chal` 的檔案，執行後看到提示：

```text
Dang, I left my flag printer in /sys/fs/bpf/prog_map. Now /sys/fs/bpf/flag will remain empty forever...
```

這裡提到兩個位於 bpffs 裡的 pinned object，分別為 `/sys/fs/bpf/prog_map` 和 `/sys/fs/bpf/flag`

題目說 flag printer 被留在 `/sys/fs/bpf/prog_map`，代表真正會輸出 flag 的 eBPF program 已經存在，只是沒有被正常執行

而 `/sys/fs/bpf/flag` 一開始是空的，表示 flag 要等到那個 eBPF program 被觸發後才會寫進 map

原本可以用 `bpftool` 觀察或 dump BPF map，不過題目環境裡面沒有 `bpftool`

因此改成自己寫一個 binary，直接透過 `bpf()` syscall 操作 pinned BPF object，流程大概如下

自己載入一個 eBPF program -> 在裡面呼叫 bpf_tail_call() -> 跳到 /sys/fs/bpf/prog_map 裡的 flag printer -> flag printer 被執行 -> flag 被寫入 /sys/fs/bpf/flag -> 讀取 flag map 拿到 flag

因為我沒有很熟悉 C 語言，所以在 AI 輔助下寫出了腳本，並得到 flag

## Flag

```text
dalctf{1_<3_t41l_c4ll5}
```
