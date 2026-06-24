# Black Mirror Memory Fragments

## Description

A corrupted mobile backup is all that remains of a wiped conversation. Sort the real evidence from the noise, reconstruct what actually happened, and recover the hidden key.

## Solution Walkthrough

A quick look at `ch_y4.dat` reveals a line of base64-encoded string, which, when decoded, is the second half of the flag (`3assembled_4cross_fragments}}`).

The first half of the flag can be found in `recovered_messages` within `messages.db`, where there are two base64-encoded strings: `Yml0Y3Rme3tzbTF0aDNy` and `MzNuX3RocjM0ZF9y`. Decoding them yields `bitctf{{sm1th3r33n_thr34d_r`.

## Flag

```text
bitctf{{sm1th3r33n_thr34d_r3assembled_4cross_fragments}}
```
