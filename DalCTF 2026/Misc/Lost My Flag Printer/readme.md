# Lost My Flag Printer

## Description

Have you ever locked your keys in your car? Log in with user `ebpf` and an empty password.

## Solution Walkthrough

After logging in, I briefly looked for the flag but couldn't find it. Later, I discovered a file named `chal` in the root directory. Running it showed the following hint:

```text
Dang, I left my flag printer in /sys/fs/bpf/prog_map. Now /sys/fs/bpf/flag will remain empty forever...

```

This mentions two pinned objects located in bpffs: `/sys/fs/bpf/prog_map` and `/sys/fs/bpf/flag`.

The challenge states that the flag printer was left in `/sys/fs/bpf/prog_map`, meaning the actual eBPF program that outputs the flag already exists, it just hasn't been executed normally.

Meanwhile, `/sys/fs/bpf/flag` is initially empty, indicating that the flag will only be written into the map after that eBPF program is triggered.

Normally, you could use `bpftool` to inspect or dump BPF maps, but `bpftool` is not available in the challenge environment.

Therefore, I resorted to writing a custom binary to directly manipulate the pinned BPF objects via the `bpf()` syscall. The workflow is roughly as follows:

Load a custom eBPF program -> Call bpf_tail_call() inside it -> Jump to the flag printer in /sys/fs/bpf/prog_map -> The flag printer executes -> The flag is written to /sys/fs/bpf/flag -> Read the flag map to retrieve the flag.

Since I am not very familiar with C, I wrote the script with the help of AI and successfully obtained the flag.

## Flag

```text
dalctf{1_<3_t41l_c4ll5}
```
