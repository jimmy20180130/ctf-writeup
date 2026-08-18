# Shifting...v2?

## 題目描述

The official second version of Shifting...? from THJCC 3rd has been moved to the misc category.

## 解題思路

1. base64 decode           -> `やゖゖをゕ〴〣〣をぷゕゖめへゅゐ〢べゑら〣え〥〩ゔ〧ゃ`
2. to charcode             -> `3084 3096 3096 3092 3095 3034 3023 3023 3092 3077 3095 3096 3081 3078 3085 3090 3022 3079 3091 3089 3023 3048 3025 3029 3094 3027 3083`
3. remove `30`             -> `84 96 96 92 95 34 23 23 92 77 95 96 81 78 85 90 22 79 91 89 23 48 25 29 94 27 83`
4. +24                     -> `108 120 120 116 119 58 47 47 116 101 119 120 105 102 109 114 46 103 115 113 47 72 49 53 118 51 107`
5. to char                 -> `lxxtw://tewxifmr.gsq/H15v3k`
6. rot4                    -> `https://pastebin.com/D15r3g`
7. bruteforce last 2 chars -> `https://pastebin.com/D15r3grG`

## Flag

```text
THJCC{maybe_this_time_is_really_an_easy_shifting_and_transforming?}
```
