# Freebie

## Description

Human error is the weakest link.

## Solution Walkthrough

This is a dum challenge that has nothing to do with human error.

The challenge begins with a login page. You cannot log in as `admin`, nor can you create an account named `admin`. However, obtaining the flag requires logging in with the username `admin`.

I tried setting the username to `admin `, `admin `, or `ad"+"min`, but none of these worked. Eventually, I suspected a weak secret, but brute-forcing with rockyou yielded no results.

Out of boredom, I tried `?debug=1`, which revealed the source code. It contained a secret key: `sup3r_s3cr3t_ctf_k3y_727`. Using this to forge a cookie with the username `admin` allowed me to obtain the flag.

## Flag

```text
LYKNCTF{2a16cd4d8964453aa9948ec5b2b92db0} (dynamic flag)
```
