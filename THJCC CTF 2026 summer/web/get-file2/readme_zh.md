# get-file2

## 題目描述

`chal.thjcc.org:8082`

## 解題思路

beautify 完 `file.php` 長這樣

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
    $h = @get_headers($s, false, $c);
    $n = null;
    foreach ($h ?: [] as $v) {
        if (preg_match("/^Location:/i", $v)) {
            $n = trim(substr($v, strpos($v, ":") + 1));
            break;
        }
    }
    if ($n !== null && !a($n)) {
        throw new Exception();
    }
    $c = stream_context_create([
        "http" => ["timeout" => 3, "ignore_errors" => true],
    ]);
    $x = @file_get_contents($s, false, $c);
    if ($x === false) {
        throw new Exception();
    }
    return $x;
}
header("Content-Type: text/plain");
try {
    echo b($_GET["u"] ?? "");
} catch (Throwable $e) {
    http_response_code(400);
    echo "error";
}
```

可以看到 `a()` 會擋掉 scheme 不是 http/https，或 host 為 `flag.thjcc` 的 URL，這次 `Location:` 的比對用 `/^Location:/i`，大小寫繞不過去了，但 `b()` 是先用 `get_headers()` 預檢一次 header，遇到第一個 `Location:` 就 `break`，之後才用 `file_get_contents()` 真正抓一次，兩次請求檢查的東西不一定是同一個

docker-compose 裡一樣有 `redirector`，`/a` 這次回的是兩個 `Location` header，第一個是 `http://r/x`，第二個是 `http://flag.thjcc/flag.txt`

預檢時只看第一個，也就是 `http://r/x`，可以通過 `a()`；但 PHP 的 HTTP stream wrapper 在解析 header 時會被後面的 `Location` 覆寫掉前面的，實際 follow 的是最後一個，於是 `file_get_contents()` 直接打 `http://flag.thjcc/flag.txt`，Host 也是對的，成功拿到 flag

payload 是 `/file.php?u=http://r/a`

## Flag

```text
THJCC{PHP_stream_30x_DuAl_65de4980cf}
```
