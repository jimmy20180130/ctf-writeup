# Warmerer Up

## Description

What, what, the rules again again?

## Solution Walkthrough

After opening `rules2.pdf`, `teapot_2026` can be seen at the very bottom. At first, I thought it might be for steghide or the password for a hidden zip file.

So I opened it in 010 Hex Editor and found strings that looked like base64, which seemed to be separated by `@@ID:<data>@@`.

![alt text](image.png)

My first guess was that this must be the zip file, so I wrote a script to extract the data and save it as `hidden.zip`. After that, using `teapot_2026` as the password allowed me to get `image.sif`.

Checking it with the `file` command revealed that it is actually an image file: `image.sif: a run-singularity script executable (binary data)`. I first used `grep` to check for `flag.txt` and found it was located inside `/home/flag/flag.txt`.

Once that was done, running `apptainer exec --containall --no-home image.sif cat /home/flag/flag.txt` successfully yielded the flag.

## Flag

```text
dalctf{n0w_y0u_r3ally_b3tt3r_kn0w_th3_rul3s}
```
