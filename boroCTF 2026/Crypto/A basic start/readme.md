# A basic start

## Description

We, the Boro Cyber Division have been spying on the chats of a group of local hackers. We used to be able to decrypt their chats from base64 but they seemed to have changed their encoding. Can you find out what they’re talking about now?

## Solution Walkthrough

1. **Step 1**:

    Decode the "Before new encoding" part using Base64 to get:

    ```text
    User1: Hey, I think the Boro team is onto us!\nUser2: No Way! They're going to send the CTF participants after us!\nUser3: It'll be okay, we'll move to another base encoding!
    ```

2. **Step 2**:

    Decode the "After new encoding" part using Base91 to get:

    ```text
    User1: Okay we're on the new encoding.
    User2: You wonder if anyones ever reading your messages?
    User1: Nope. boroCTF{B@5ics_0f_B@si6s}
    ```

## Flag

```text
boroCTF{B@5ics_0f_B@si6s}
```
