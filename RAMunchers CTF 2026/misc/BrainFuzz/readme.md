BrainFuzz
We have observed strange behaviour from the Gibson lately. Recently, the Gibson has been generating images of itself and random blobs of data. Can you look into this and see if there is any hidden meaning?

仔細~~觀察~~通靈 output.bin，把他變成每八個 bytes 一行以後就會發現有些全部都是 FF 有些則是隨機的 bytes
設全部都是 FF 的那行為 0，反之則為 1
接著把每八個 bit 轉成一個 byte，接著就會得到一串字串 `definitely_not_a_secret_p4ssw0rd`
完成以後會發現 generated_gibson.jpg 好像沒派上用場，通靈一下以後我覺得可能是 steghide 的 passphrase，結果還真的是

```txt
┌──(kali㉿kali)-[~/Desktop]
└─$ steghide extract -sf generated_gibson.jpg
Enter passphrase: 
wrote extracted data to "flag.txt".
```

好了以後就可以取得 flag 了
RMCTF{m37h0d_b3h1nd_7h3_m4dn355!}