import requests

url =  "https://datapilots.tistory.com/"
custom_header = { "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"}
res = requests.get(url)
res.raise_for_status()

with open("tistory.html","w",encoding="utf-8") as f : f.write(res.text)