# Time Machine

## 題目描述

Upload your archives.

Snapshot what you need.

Powered by Python's shutil.

http://chal.thjcc.org:9005/

## 解題思路

伺服器有三個 endpoint，`/restore` 上傳檔案和解壓、`/snapshot` 把整個工作目錄打包成 zip 後下載、`/reset` 清空

先丟一個含各種 symlink 的 tar 上去試水溫，首頁的檔案列表就直接顯示 `link  name  -> target`，代表 symlink 被原樣還原了，那就可以拿 symlink 去指容器裡的任意檔案

先指 `/app/app.py` 把原始碼撈出來對照，檢查函式只驗 `member.name`

```python
def escapes(name: str) -> bool:
    if not name:
        return True
    if name.startswith("/") or os.path.isabs(name):
        return True
    return ".." in name.replace("\\", "/").split("/")


def verify_archive(path: str) -> None:
    if tarfile.is_tarfile(path):
        with tarfile.open(path) as tf:
            for member in tf.getmembers():
                if escapes(member.name):          # 只看 name
                    raise UnsafeArchive(...)
```

`member.linkname` 從頭到尾沒進過 `escapes()`，所以 `name="67"` + `linkname="/proc/self/environ"` 會給過，然後就發現 flag 就在這裡面

## Flag

```text
THJCC{th3_v3r1f13r_ch3ck3d_th3_n4m3_but_n0t_th3_l1nkn4m3}
```
