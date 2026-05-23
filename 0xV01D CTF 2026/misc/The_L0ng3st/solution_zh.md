# The_L0ng3st

## 題目描述

576a5debdec404ec476c1823fc8b45d909040f2da92195624b77c92fcc9c232a18f2f71ee81281fde3d8fe5763a3e7db576a5debdec404ec476c1823fc8b45d909040f2da92195624b77c92fcc9c232a18f2f71ee81281fde3d8fe5763a3e7db

type = hash

flagformat: 0xV01D{firsttype_secondetype.......} flag example: 0xV01D{sha3_sha1_sha4_sha9}

note : no - in the flag

### 提示

1. Hint 1  
    1- read carefully 2- divide 3- identify 4- get the flag

## 解題思路

通靈很久不知道怎麼解，於是去私訊作者

```text
Listen look at the hash closely 
There u can see parts is repeted u need to name the hashes 

Example : “word” —-> 12345abcd (md5 for the word) 
67890efghi (sha256 for the word ) 

The challenge is written in that way 
12345abcd67890efghi12345abcd67890efghi 

So u can cut it and count the length of the hash to identify the type of hash, in our example the arrangement is 
md5_sha256_md5_sha256 

So the flag will be 
0xV01D{md5_sha256_md5_sha256 } 


Do the same thing in the real challenge
Hope it helps
```

得到上述的東西後排列組合一下就有 flag 了

## Flag

```text
0xV01D{sha256_md5_sha256_md5}
```
