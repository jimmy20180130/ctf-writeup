# Severance Overtime Memory Parasite

## 題目描述

Lumon's off-books data wing left behind one unstable memory capture from a quarantined workstation. Reconstruct the incident and recover what the intruder failed to scrub.

## 解題思路

可以看到  `lumon_overtime` 他有 `MDR_REC_A` 和 `MDR_REC_B` 和 `MDR_REC_C`

先胡搞瞎搞一番，以為 `MDR_REC_A` 和 `MDR_REC_B` 和 `MDR_REC_C` 是一組資料還是啥的，搞半天都沒弄出什麼東西。

後來發現把 `MDR_REC_A` base64 decode 再對 `0x37` XOR，最後 zlib decompress 以後就可以得到一串 JSON 字串

```json
{"mx":"MIND-FLAYER-OTC","proc":"ot_kernel_helper.exe","queue":"macrodata_refiner","wl":"kelp-and-lanterns"}
```

接著看到 `MDR_REC_B`，排列組合一下，最後成功以 `MIND-FLAYER-OTC:kelp-and-lanterns` 當 key，並且以 RC4 來解密，會得到一串 session (`OTC_SESSION=otc://macrodata/7f9e3a1dcb8a4f2b`)

最後看到 `MDR_REC_C`，透過用重複的 SHA-1 雜湊值做 XOR，key 也一樣是 `kelp-and-lanterns:MIND-FLAYER-OTC`

```bash
curl -X POST http://167.99.51.176:5000/api/v1/overtime/redeem \
  -H 'Content-Type: application/json' \
  -d '{"session":"otc://macrodata/7f9e3a1dcb8a4f2b"}'
```

POST 完以後就可以拿到 flag 了

```json
{
    "flag": "bitctf{{0v3r71m3_m3m0ry_p4r45173}}",
    "message": "Overtime clearance granted"
}
```

## Flag

```text
bitctf{{0v3r71m3_m3m0ry_p4r45173}}
```
