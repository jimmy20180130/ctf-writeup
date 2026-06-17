# Lazing Around

## Description

Get back to work!

## Solution Walkthrough

The `chal` downloaded from the problem, after checking with `file`, was found to be an `ext4 filesystem data`. After mounting, `txt` files like `entry_log` and `exit_log` could be seen inside. None of them contained the flag (where `mnt.zip` is a zip file I created containing all these logs).

We know that the block size of `ext4` is usually `4096 bytes`. Upon checking each log, their size was smaller than one block, and `ext4` allocates space in units of blocks. Therefore, `file slack` might exist between the `EOF` and the end of that block.

So, it was inferred that this problem might involve hiding the flag in the `slack space`. With the assistance of `AI`, a `python` script was written. The steps are roughly as follows: first, obtain the normal content of each log from `mnt.zip`; then, search for the position of that content in the `raw image`; read the data between the `EOF` of that file and the next `block boundary`; after removing trailing `null` bytes, sort and concatenate the non-empty `slack` according to `image offset` to get the `flag`.

## Flag

```text
boroCTF{C0u!D_yo8_cuT_m3_Som4_sL@ck}
```
