import requests
from bs4 import BeautifulSoup
import pandas as pd

data = []
response = requests.get("https://www.yuhan.ac.kr/collegeService/schedule.do?menu_idx=3124&year=2026&toMonth=2&option=&SCH_DAY=&calPopDayId=&cal_Type=2")
html = response.text
soup = BeautifulSoup(html, "html.parser")

#현재 문제 : 원하는 데이터를 찾기엔 띄어쓰기 때문에 불가능, 원하는 데이터 많기 때문에 지금으로써는 불가능
# print(soup.select_one("strong style").text)

items= soup.select("tbody > tr > td > ul > li")
for item in items:
    days = item.select_one("strong").text
    contents = item.select_one("p").text
    print(days, contents)
    data.append([days,contents])

# 데이터 프레임 만들기
df = pd.DataFrame(data,columns=['날짜', '내용'])
df.to_excel("yuhan_calender.xlsx",index=False)

# 동적페이지, 웹 페이지 자동화를 하기 위해서는 셀레니움 라이브러리를 배워야함.