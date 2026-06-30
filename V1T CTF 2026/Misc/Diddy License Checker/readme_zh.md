# Diddy License Checker

## 題目描述

giggle

## 解題思路

用 ida 打開 diddy 以後可以發現他會問三個問題，第三個問題他還會發 http 請求，所以代表我們應該沒辦法直接透過靜態分析就拿到 flag

第一個問題非常簡單，回答 duck 就對了

![alt text](image.png)

第二個問題，他會檢查你的第一個字元是不是 0，接著就開始算費波那契數列，所以答案就是 `01123584371808876415628101123584`

![alt text](image-1.png)

第三個問題他是會去 `aHR0cDovL3YxdC5zaXRlLw==` 也就是 `http://v1t.site`，然後找剛剛輸入的 license，也就是說他會發 http get 到 `http://v1t.site/<licence>`

由於之前我做別題有剛好看到他們網站是用 Github pages 搞的，而且裡面有個 `license-for-user-deadbeef-diddy`，所以 license 很明顯就是他

```c
if (v7 == 32)
{
    printf("3. Enter your license name: ");
    __isoc23_scanf("%63s", v44);
    v12 = (void *)base64_decode("aHR0cDovL3YxdC5zaXRlLw==");
    ptr = v12;
    *((_BYTE *)v12 + v35) = 0;
    sprintf(s, "%s%s", (const char *)v12, v44);
    v33 = (void *)http_get(s);
    v13 = arr_len;
    v14 = alloca(arr_len);
    p_ptr = &ptr;
    xor_bytes(&arr, (unsigned int)arr_len, v44, &ptr);
    v31 = v13 / 2;
    v16 = alloca(v13 / 2);
    v32 = &ptr;
    if (v13 > 0)
    {
        v17 = &ptr;
        do
        {
            __isoc23_sscanf(p_ptr, "%2hhx", v17);
            v4 += 2;
            p_ptr = (void **)((char *)p_ptr + 2);
            v17 = (void **)((char *)v17 + 1);
        } while (arr_len > v4);
    }
    v18 = (char *)v33;
    v30 = v38;
    v19 = v38;
    do
    {
        __isoc23_sscanf(v18, "%2hhx", v19++);
        v18 += 2;
    } while (v39 != v19);
    v20 = v39;
    v21 = v34 + 32;
    do
    {
        __isoc23_sscanf(v5, "%2hhx", v20);
        v5 += 2;
        ++v20;
    } while (v21 != v5);
    v22 = 0;
    v23 = EVP_CIPHER_CTX_new();
    v24 = EVP_aes_128_cbc();
    EVP_DecryptInit_ex(v23, v24, 0, v30, v39);
    EVP_DecryptUpdate(v23, v46, &v36, v32, v31);
    EVP_DecryptFinal_ex(v23, &v46[v36], &v37);
    v36 += v37;
    EVP_CIPHER_CTX_free(v23);
    v25 = v36;
    LODWORD(v25) = v36;
    v26 = v36 >> 31;
    v27 = v36;
    v46[v25] = 0;
    v28 = (int)(__SPAIR64__(v26, v25) / 2);
    if (v27 > 1)
    {
        do
        {
            __isoc23_sscanf(&v46[2 * v22], "%2hhx", &s1[v22]);
            ++v22;
        } while ((int)v28 > (int)v22);
    }
    s1[v28] = 0;
    if (!strncmp(s1, "v1t", 3u))
    {
        printf("Oh hi diddy here your flag: %s\n", s1);
        free(ptr);
        free(v33);
        return 0;
    }
    break;
}
```

~~最後打開程式輸入以上三個答案就可以得到 flag 了~~並沒有，我也不知道為什麼。喔原來是被我的防毒軟體擋掉了

反正我就照上面的思路寫了一個 `solution.py` 之後就拿到 flag 了

## Flag

```text
v1t{435_f1b0_w3bs1t3}
```
