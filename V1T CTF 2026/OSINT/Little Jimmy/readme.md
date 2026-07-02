# Little Jimmy Writeup

## Description

Jimmy @V1tJjimmy is a young V1te developer with an unusual obsession for ducks, clean interfaces, and tiny frontend experiments that probably started as jokes but somehow became real projects.

Between broken components, late-night commits, and suspiciously duck-themed side projects, he leaves behind just enough details for curious people to notice. Most of them look ordinary at first glance.

## Solution Walkthrough

Although I didn't solve the second part of the flag, I decided to write a writeup because it was a great challenge.

1. **Step 1**:

    A quick search on X led me to an account:

    https://x.com/V1tJjimmy

    The first post is clearly the "duck project" mentioned in the challenge. Checking GitHub, I found:

    https://github.com/jimmydev367/V1te-proDuck

    Although it looked clean and empty, a closer inspection revealed that some commits had been overwritten by a force push.

    ```bash
    ┌──(kali㉿kali)-[~/Desktop/ctf/V1T CTF/Little Jimmy]
    └─$ curl -sS \
    "https://api.github.com/users/jimmydev367/events/public?per_page=100" |
    jq '
    .[]
    | {
        type,
        created_at,
        repo: .repo.name,
        payload
        }
    '
    {
    "type": "WatchEvent",
    "created_at": "2026-06-26T14:50:51Z",
    "repo": "jimmydev367/V1te-proDuck",
    "payload": {
        "action": "started"
        }
    }
    {
    "type": "PushEvent",
    "created_at": "2026-06-26T14:40:58Z",
    "repo": "jimmydev367/V1te-proDuck",
    "payload": {
        "repository_id": 1265974080,
        "push_id": 36224030692,
        "ref": "refs/heads/main",
        "head": "e122e6e1dd024c3b8d5d22fe1c8ceeb11b1bf280",
        "before": "7727f21c1c8a30e1197b7c3b20eaa052833b90a1"
        }
    }
    {
    "type": "PushEvent",
    "created_at": "2026-06-26T14:40:34Z",
    "repo": "jimmydev367/V1te-proDuck",
    "payload": {
        "repository_id": 1265974080,
        "push_id": 36224011019,
        "ref": "refs/heads/main",
        "head": "7727f21c1c8a30e1197b7c3b20eaa052833b90a1",
        "before": "3324dfe058063f280ac73b50d936b07c1b85d730"
        }
    }
    {
    "type": "CreateEvent",
    "created_at": "2026-06-26T14:20:44Z",
    "repo": "jimmydev367/V1te-proDuck",
    "payload": {
        "ref": "main",
        "ref_type": "branch",
        "full_ref": "refs/heads/main",
        "master_branch": "main",
        "description": null,
        "pusher_type": "user"
        }
    }
    ```


    From there, we can find the modified content:

    https://api.github.com/repos/jimmydev367/V1te-proDuck/events

    ```text
    {
        "profile_type": "accidental_internal_author_profile",
        "app": "V1te proDuck",
        "a_piece_of_flag": "VzB1ejExcXJeVzB1Ml5FdGJqXkBxcV5HMXNiMmVeVWkyXlRxcnVzMjVsXg==",
        "xor_key": "V1T{",
        "author": {
            "author_name": "Nguyen V1et Hoang"
            "display_name": "Quack Byte",
            "phone": "+1-202-555-0184",
            "email": "quackbyte.hoangnv@gmail.com",
            "facebook": "https://www.facebook.com/user0182883828282919"
        }
    }
    ```

    XOR the flag above to get:

    ```text
    V1t{00ps_V1t3_Duck_App_F0rc3d_Th3_Upstr34m_
    ```

2. **Step 2**:

    https://www.facebook.com/user0182883828282919

    After navigating to this Facebook profile, you can find the ID in the website's source code:

    ![alt text](image.png)

    The principle here is that Facebook automatically creates a post when the bio is changed. We can use Ctrl+F to search for the bio; the post ID associated with the bio follows it. You can then go directly to https://www.facebook.com/user0182883828282919/posts/122202695324435453 to see the post.

    There are comments below:

    ![alt text](image-1.png)

    ![alt text](image-2.png)

    The remaining part of the flag is at the bottom of the second image:

    ```text
    OF4jY1v{OFr{[G8T`EOgPly0L08CbICgT{OkbkO1gP<<
    ```

    For the second half, XOR with 0x01 first, then convert from Base64, and finally convert to ASCII to get:

    ```text
    NG5kX0wzNGszZF9UaDNfQmx1M19BcHBfUzNjcjN0fQ==
    4nd_L34k3d_Th3_Blu3_App_S3cr3t}
    ```

    Nice chall!

## Flag

```text
V1t{00ps_V1t3_Duck_App_F0rc3d_Th3_Upstr34m_4nd_L34k3d_Th3_Blu3_App_S3cr3t}
```
