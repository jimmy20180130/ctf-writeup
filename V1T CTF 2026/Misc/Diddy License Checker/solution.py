from Crypto.Cipher import AES

key  = bytes.fromhex("7631745f3433355f6b33795f66726672")[:16] # http://v1t.site/license-for-user-deadbeef-diddy
iv   = bytes.fromhex("01123584371808876415628101123584") # lucky number
ct   = bytes.fromhex("9fad7f446b751ae0f12d06736710eb70110cd73f69976c5bfed1c5dc6432b8823d1378094fa60d347d9b4da3399db570")

pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
pt = pt[:-pt[-1]]
flag = bytes.fromhex(pt.decode()).decode()
print(flag) 