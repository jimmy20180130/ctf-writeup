# get-file1

## 題目描述

`chal.thjcc.org:8081`

## 解題思路

beautifty 完 `file.php` 長這樣

```php
<?php
function a($s)
{
    $p = parse_url($s);
    return $p &&
        isset($p["scheme"], $p["host"]) &&
        in_array(strtolower($p["scheme"]), ["http", "https"], true) &&
        strtolower(rtrim($p["host"], ".")) !== "flag.thjcc";
}
function b($s)
{
    for ($i = 0; $i < 5; $i++) {
        if (!a($s)) {
            throw new Exception();
        }
        $c = stream_context_create([
            "http" => [
                "follow_location" => false,
                "timeout" => 3,
                "ignore_errors" => true,
            ],
        ]);
        $x = @file_get_contents($s, false, $c);
        $h = $http_response_header ?? [];
        $n = null;
        foreach ($h as $v) {
            if (str_starts_with($v, "Location:")) {
                $n = trim(substr($v, strpos($v, ":") + 1));
            }
        }
        if ($n !== null) {
            if (!a($n)) {
                throw new Exception();
            }
            $s = $n;
            continue;
        }
        if ($x === false) {
            throw new Exception();
        }
        $d = stream_context_create([
            "http" => [
                "follow_location" => true,
                "timeout" => 3,
                "ignore_errors" => true,
            ],
        ]);
        $y = @file_get_contents($s, false, $d);
        if ($y === false) {
            throw new Exception();
        }
        return $y;
    }
    throw new Exception();
}
header("Content-Type: text/plain");
try {
    echo b($_GET["u"] ?? "");
} catch (Throwable $e) {
    http_response_code(400);
    echo "error";
}
```

可以看到 `a()` 會擋掉 host 為 `flag.thjcc` 的 URL，`b()` 最多手動跟 5 次 redirect，且只看 `Location:` 這個 header (大寫 `L`)，但如果若沒偵測到 `Location:` 的話就會改用 `follow_location=true` 直接抓，且不會再檢查目標 host

docker-compose 裡有個 `redirector`，`/a` 會回 `location: http://flag.thjcc/flag.txt` (小寫 `l`)，`/b` → 回 `Location: http://flag.thjcc/flag.txt` (大寫 `L`)

因為前面提到偵測 `Location:` 的東西大小寫敏感，`/a` 的小寫 header 不會被認成 redirect，於是會直接 follow，成功拿到 flag

payload 是 `/file.php?u=http://r/a`

## Flag

```text
THJCC{pHp_StReAm_30X_cAsE_43082ed528}
```
