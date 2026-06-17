# Anatomically Incorrect

## Description

Hey, I found this random assortment of characters on the ground in class. What does it mean?

1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p4 1s2 2s2 2p6 3s2 3p6 1s2 2s2 2p6 3s2 3p6 4s2 3d3 1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6 5s2 4d2 1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6 5s2 4d10 5p6 6s2 4f14 5d10 6p6 7s2 5f13 1s2 2s2 2p6 3s2 3p4 1s2 2s2 1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6 5s2 4d10 5p6 6s2 4f14 5d10 6p6 7s2 5f14 6d9 1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6 5s2 4d10 5p6 6s2 4f14 5d10 6p6 7s2 5f14 6d10 7p3 1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6 5s2 4d10 5p6

This challenge does not contain boroCTF in the solution. Please put in the format boroCTF{ExAmPlE}

## Solution Walkthrough

1. **Step 1**:

    After three years of high school torture, you should be able to tell with your eyes closed that this is an electron configuration:

    ```text
    1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p4   Se
    1s2 2s2 2p6 3s2 3p6   Ar
    1s2 2s2 2p6 3s2 3p6 4s2 3d3   V
    1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6 5s2 4d2  Zr
    1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6 5s2 4d10 5p6 6s2 4f14 5d10 6p6 7s2 5f13  Md
    1s2 2s2 2p6 3s2 3p4  S
    1s2 2s2  Be
    1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6 5s2 4d10 5p6 6s2 4f14 5d10 6p6 7s2 5f14 6d9  Rg
    1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6 5s2 4d10 5p6 6s2 4f14 5d10 6p6 7s2 5f14 6d10 7p3  Mc
    1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6 5s2 4d10 5p6   Xe

    SeArVZrMdSBeRgMcXe
    ```

    However, this is not the flag; the challenge provided another reference table.

2. **Step 2**:

    I did some research and discovered that the reference table provided in the challenge is a variation of this table:

    ![alt text](image.png)

    The only difference is that the outer circle of a standard table is clockwise, while the one provided is counter-clockwise, and the provided table is shifted one space to the left.

    All that's left is to map it manually.

    ![alt text](image-1.png)

## Flag

```text
boroCTF{IFOoNEdHtEFlAgS}
```
