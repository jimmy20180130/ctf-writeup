先看到 https://bluepeakcyber.co.uk 的網頁原始碼，有一行
<!-- synced footers from internalit.bluepeakcyber -->
於是去看 https://internalit.bluepeakcyber.co.uk，發現在維護中
去看看 https://internalit.bluepeakcyber.co.uk/robots.txt
結果發現
User-agent: *
Disallow: /memo.pdf
去 /memo.pdf 發現一篇文件關於 dns record 的，於是去看 bluepeakcyber.co.uk 的 dns record
發現有個 txt data
TXT data
"Legacy systems have been left running while the new infrastructure is under maintenance. To contact the infrastructure team get in contact with support@coventry.r032.bluepeakcyber.co.uk"

去找 coventry.r032.bluepeakcyber.co.uk 的 txt record 即可得到 flag
https://www.nslookup.io/domains/coventry.r032.bluepeakcyber.co.uk/dns-records/

RMCTF{DN5_1S_PUBLIC}