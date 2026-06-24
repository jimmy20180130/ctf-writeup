# The Return Slip

## Problem Description

The login desk is happy to send buyers back where they came from. If the return address is trusted too much, something extra may tag along.

## Solution Walkthrough

In this challenge, when a user tries to access an internal page without being logged in, the system should supposedly redirect them to the login page (`/auth`) and add a `next` parameter.

The `next` here was figured out by intuition. The challenge author said that visiting the `/support` page would redirect to `/auth`, but I personally was not redirected.

The vulnerability in this challenge is that you can change the URL after `next` to any URL, such as `https://google.com`.

After changing it, once the login is completed, you will be redirected to `https://google.com?handoff=bitflag%7Btru5t3d_r3d1r3cts_c4n_c4rry_s3cr3ts%7D`. The string after `handoff` is the flag.

## Flag

```text
bitflag{tru5t3d_r3d1r3cts_c4n_c4rry_s3cr3ts}
```
