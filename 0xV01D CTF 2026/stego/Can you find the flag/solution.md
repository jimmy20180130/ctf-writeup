# Can you find the flag

## Description

i accedntly downloaded this picture insted of a whole website can you find the website files or a flag?

### Hints

1. Hint: fr it's easy  
    Have you checked E9 exif my guy? forget about the zip it's just a fake flag  
    Go on i wanna see the 1st blood guys!!!
2. Hint: trust me it worth it  
    `https://gofile.io/d/tdNLHn` i changed sth in it to make it easier for you now!!

## Solution Walkthrough

First, examine the downloaded `cicada_original.jpg` file, where you can find a hex string.  
Next, based on the hints, download `E9.jpg` from the provided link. Inside the image, there is a base64-encoded string: `aHR0cHM6Ly93d3cubWVkaWFmaXJlLmNvbS9maWxlLzV4a21ubGVueWI5a3QzaC81RTJSL2ZpbGU=`  
Decoding this gives: `https://www.mediafire.com/file/5xkmnlenyb9kt3h/5E2R/file`.  
Download the file and you'll find `5E2R`,  which is a gzip/tar archive. Using a hex editor, you can see the second half of the flag: `1ng_St3g0_D4mn_WP}` and the first half: `0xV01D{St4rt3d_S0lv`.  
Combine them together to get the flag

## Flag

```text
0xV01D{St4rt3d_S0lv1ng_St3g0_D4mn_WP}
```
