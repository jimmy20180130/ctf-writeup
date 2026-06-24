# Severance Overtime Memory Parasite

## Description

Lumon's off-books data wing left behind one unstable memory capture from a quarantined workstation. Reconstruct the incident and recover what the intruder failed to scrub.

## Solution Walkthrough

You can see that `lumon_overtime` has `MDR_REC_A`, `MDR_REC_B`, and `MDR_REC_C`.

I messed around with it for a while, thinking `MDR_REC_A`, `MDR_REC_B`, and `MDR_REC_C` were a single set of data or something, but I didn't get anywhere after a long time.

Later, I discovered that by base64 decoding `MDR_REC_A`, XORing it with `0x37`, and finally performing a zlib decompression, I could obtain a JSON string.

```json
{"mx":"MIND-FLAYER-OTC","proc":"ot_kernel_helper.exe","queue":"macrodata_refiner","wl":"kelp-and-lanterns"}
```

Next, looking at `MDR_REC_B`, after some permutations and combinations, I successfully used `MIND-FLAYER-OTC:kelp-and-lanterns` as the key and decrypted it with RC4 to obtain a session (`OTC_SESSION=otc://macrodata/7f9e3a1dcb8a4f2b`).

Finally, looking at `MDR_REC_C`, I used XOR with a repeated SHA-1 hash value; the key is also `kelp-and-lanterns:MIND-FLAYER-OTC`.

```bash
curl -X POST http://167.99.51.176:5000/api/v1/overtime/redeem \
  -H 'Content-Type: application/json' \
  -d '{"session":"otc://macrodata/7f9e3a1dcb8a4f2b"}'
```

After posting, you can get the flag.

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
