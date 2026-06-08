# MS DOS Plumber Writeup

## Description

My friend gave me a floppy with her modded version of Angel Ortega's game Space Plumber (1997), but she said there was something wrong with one of the files. Can you help me fix, build, and run it?

## Solution Walkthrough

Since I did not expect to solve this challenge at the time, I did not take screenshots for every step. Sorry about that.

1. **Step 1**：

    The challenge provided a noVNC DosBox virtual machine, and the initial disk was on the Z drive.

    First, check which drives are mounted:

    ![alt text](pictures/image.png)

    I found that there were A, C, and Z drives.

    There was nothing useful inside Z:. It was just a virtual system drive.

    So I switched to A:

    ```bash
    a:
    dir
    cd splumber
    dir
    ```

    ![alt text](pictures/image-1.png)

    ![alt text](pictures/image-2.png)

    Since there was a makefile inside, I tried running make directly inside \splumber, but it showed:

    ```text
    'make' is a illegal command
    ```

2. **Step 2**：

    There did not seem to be any build tools inside A:, so I checked C:. Then I found some compilers inside util:

    ![alt text](pictures/image-3.png)

    Since they were zip files, I extracted all of them first:

    ```bash
    mkdir \djgpp
    unzip32 djdev205.zip -d c:\djgpp
    unzip32 bnu2351b.zip -d c:\djgpp
    unzip32 gcc930b.zip -d c:\djgpp
    unzip32 mak44b.zip -d c:\djgpp
    unzip32 csdpmi7b.zip -d c:\djgpp
    ```

    After extracting them, set up the build environment:

    ```bash
    set DJGPP=c:\djgpp\djgpp.env
    set PATH=c:\djgpp\bin;c:\util;%PATH%
    ```

    This should make make available.

3. **Step 3**：

    ```bash
    a:
    cd \splumber
    make
    ```

    After that, many errors appeared. Since noVNC did not allow me to scroll the terminal up and down, I started by checking the earlier errors:

    ![alt text](pictures/image-4.png)

    I found that src/sp_sb.c was broken.

    In the terminal, enter:

    ```bash
    edit src\sp_sb.c
    ```

    This opens the editor. Click Search at the top and enter:

    ```text
    movl $96
    ```

    You will see a large chunk of C code. The reason for the error is that C cannot directly have line breaks inside a string, so we need to turn it into a proper string. Change it to:

    ```c
    asm("movl $96, %%ecx\n"
        "movl $0x80, %%eax\n"
        "movl %0, %%edi\n"
        "cld\n"
        "rep\n"
        "stosl"
        :
        : "m" (sb_mixing_buffer)
        : "%eax", "%ecx", "%edi");
    ```

    ![alt text](pictures/image-5.png)

    Then it should be fixed.

    After that, click File in the top-left corner, Save, then Exit to return to the terminal.

4. **Step 4**：

    After fixing it, go back to A: and run make. It will start building.

    After the build finishes, run dir again and you will see splumber.exe.

    Enter splumber to run it. The game screen will appear, and you will get the flag.

    Commands:

    ```bash
    a:            # You should be in A:\splumber
    make
    dir
    splumber
    ```

    ![alt text](pictures/image-6.png)

## Flag

```text
dalctf{d0s_d0s_d0s_yeah}
```
