import requests
from bs4 import BeautifulSoup
import pandas as pd

# 파일에 저장하기 위해 리스트 형태로 선언
yuhan_data = []

yuhan_response = requests.get("https://www.yuhan.ac.kr/collegeService/schedule.do?menu_idx=3124&year=2026&toMonth=2&option=&SCH_DAY=&calPopDayId=&cal_Type=2")
html = yuhan_response.text
soup = BeautifulSoup(html, "html.parser")

yuhan_items = soup.select("tbody > tr > td > ul > li")
for item in yuhan_items:
    days = item.select_one("strong").text
    contents = item.select_one("p").text
    print(days, contents)
    yuhan_data.append([days,contents])

# 리눅스 마스터 일정 데이터 크롤링
linux_data = []

linux_response = requests.get("https://www.ihd.or.kr/guidecert1.do")
html = linux_response.text
soup = BeautifulSoup(html, "html.parser")
