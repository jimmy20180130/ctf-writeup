# Classless

## Description

Ever learnt OOP? If yes? Good, now forget what a class is xD

## Solution Walkthrough

This website is a music visualizer. By the end, you will notice something a bit sus; how did the emojis become part of the flag?

![alt text](image.png)

Furthermore, it uses its own custom font. Looking at the code, you can see the lyrics as follows:

```text
1\n00:00:18,768 --> 00:00:21,632\ntao kh\u00f4ng bao gi\u1edd mu\u1ed1n nghe \u0111\u00e2u ch\u00fang m\u00e0y cap cap\n\n2\n00:00:21,632 --> 00:00:24,551\npurple Haze m\u00f9i purple haze g\u1ecdi l\u00e0 kh\u00e9t l\u1eb9t\n\n3\n00:00:24,551 --> 00:00:27,595\nfuck tao \u0111\u00f3i r b\u1ee5ng tao l\u00e9p k\u1eb9p\n\n4\n00:00:27,595 --> 00:00:30,707\ntao ch\u1ec9 \u0111i ngang qua now she wet wet\n\n5\n00:00:30,707 --> 00:00:33,314\nnh\u1eafn cho anh l\u00e0 pls give me a chance\n\n6\n00:00:33,314 --> 00:00:36,186\nanh kh\u00f4ng th\u00edch l\u00e0 ph\u1ea3i l\u00e0m vi\u1ec7c qua middleman\n\n7\n00:00:36,186 --> 00:00:39,093\nanh th\u00edch k\u00ed cho fan c\u1ee7a anh b\u1eb1ng b\u00fat bi \u0111en\n\n8\n00:00:39,093 --> 00:00:40,407\nblown her back out\n\n9\n00:00:40,407 --> 00:00:42,085\nfill her coochie\n\n10\n00:00:42,085 --> 00:00:45,119\nI love that juicy pussy give it to me\n\n11\n00:00:45,119 --> 00:00:47,163\nb\u1ecdn ch\u00f3 n\u00e0y gh\u00e9t xong r l\u1ea1i th\u00edch \u00e0\n\n12\n00:00:47,163 --> 00:00:48,516\n\u0111\u00e9o mu\u1ed1n gi\u1ea3i th\u00edch\n\n13\n00:00:48,516 --> 00:00:49,984\ngh\u00e9t xong r l\u1ea1i th\u00edch \u00e0\n\n14\n00:00:49,984 --> 00:00:51,208\n\u0111\u00e9o mu\u1ed1n gi\u1ea3i th\u00edch\n\n15\n00:00:51,208 --> 00:00:53,010\ngh\u00e9t xong r l\u1ea1i th\u00edch \u00e0\n\n16\n00:00:53,010 --> 00:00:54,252\n\u0111\u00e9o mu\u1ed1n gi\u1ea3i th\u00edch\n\n17\n00:00:54,252 --> 00:00:55,806\ngh\u00e9t xong r l\u1ea1i th\u00edch \u00e0\n\n18\n00:00:55,806 --> 00:00:57,107\nkh\u00f4ng c\u1ea7n ph\u1ea3i gi\u1ea3i th\u00edch\n\n19\n00:00:57,107 --> 00:01:00,218\ntao th\u00edch ng\u1eafm g\u00e1i nh\u01b0ng em n\u00e0o vibe m\u1edbi \u0111\u01b0\u1ee3c tao follow\n\n20\n00:01:00,218 --> 00:01:03,196\nth\u1ea5y m\u00ecnh qu\u00e1 l\u00e0 bay nh\u01b0ng \u0111\u00e9o hi\u1ec3u \u0111\u1ea5y l\u00e0 do \u0111\u00e2u\n\n21\n00:01:03,196 --> 00:01:06,026\nMCKeyyyy n\u00f3 \u0111\u00e3 tr\u1edf l\u1ea1i r\u1ed3i \u0111\u00e9o c\u00f2n lo \u00e2u\n\n22\n00:01:06,026 --> 00:01:07,669\ntao set the trend\n\n23\n00:01:07,669 --> 00:01:09,175\nch\u00fang m\u00e0y follow\n\n24\n00:01:09,520 --> 00:01:10,988\ntao v\u1eabn \u0111ang tr\u00ean top\n\n25\n00:01:10,988 --> 00:01:12,345\nc\u00f9ng th\u00e0nh raw \u0111i xem van gogh\n\n26\n00:01:12,345 --> 00:01:13,776\nb\u1ecdn tao l\u00e0 vietnamese Hot\n\n27\n00:01:15,499 --> 00:01:17,018\nrick owens mob\n\n28\n00:01:17,018 --> 00:01:18,463\ntequila shots\n\n29\n00:01:18,463 --> 00:01:21,545\nvamp vamp vamp vamp vamp vamp vamp vamp\n\n30\n00:01:21,546 --> 00:01:22,941\nCH\u00daNG N\u00d3 GH\u00c9T XONG L\u1ea0I TH\u00cdCH \u00c0KKK?\n\n31\n00:01:22,941 --> 00:01:24,195\n\u0110\u00c9O C\u1ea6N PH\u1ea2I GI\u1ea2I TH\u00cdCH\n\n32\n00:01:24,195 --> 00:01:25,919\nGH\u00c9T XONG L\u1ea0I TH\u00cdCH \u00c0KKK?\n\n33\n00:01:25,919 --> 00:01:27,324\n\u0110\u00c9O C\u1ea6N PH\u1ea2I GI\u1ea2I TH\u00cdCH 🔥󠅘󠅕󠅜󠅜󠅟󠄐󠅣󠅙󠅢\n\n34\n00:01:27,324 --> 00:01:28,861\nGH\u00c9T XONG L\u1ea0I TH\u00cdCH \u00c0KKK? 😀😃😄😁😆\n\n35\n00:01:28,861 --> 00:01:30,169\n\u0110\u00c9O C\u1ea6N PH\u1ea2I GI\u1ea2I TH\u00cdCH 😅😂🤣\n\n36\n00:01:30,169 --> 00:01:31,882\nGH\u00c9T XONG L\u1ea0I TH\u00cdCH \u00c0KKK? 🥲😊😇\n\n37\n00:01:31,882 --> 00:01:33,685\n\u0110\u00c9O C\u1ea6N PH\u1ea2I GI\u1ea2I TH\u00cdCH 🙂🥲🙃\n\n38\n00:01:33,686 --> 00:01:35,685\n 😉😌😍";
```

By extracting the emojis, you can obtain the flag:

😀😃😄😁😆😅😂🤣🥲😊😇🙂🥲🙃😉😌😍 -> v1t{g04t_mck_hvl}

![alt text](image-1.png)

## Flag

```text
v1t{g04t_mck_hvl}
```
