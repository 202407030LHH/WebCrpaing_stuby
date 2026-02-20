import requests

custom_header = { "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"} 
url = "https://www.yuhan.ac.kr/collegeService/schedule.do?menu_idx=3124" \

res = requests.get(url, headers=custom_header)
res.raise_for_status()

with open("UnivCalender-UserAgent-Add.html","w",encoding="utf8") as f : f.write(res.text)