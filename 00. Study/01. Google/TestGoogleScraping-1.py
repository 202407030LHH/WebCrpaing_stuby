import requests

res = requests.get("https://www.yuhan.ac.kr/collegeService/schedule.do?menu_idx=3124")

res.raise_for_status()
print("응답코드:", res.status_code)

print(len(res.text))
print(res.text)

with open("UnivCalender.html","w",encoding="utf8") as f : f.write(res.text)
