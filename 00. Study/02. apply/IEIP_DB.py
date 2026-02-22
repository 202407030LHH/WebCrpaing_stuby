# 정보처리산업기사 시험 일정
# Q-net 크롤링 방지 기능 때문에 에듀온 사이트 참조
import requests
from bs4 import BeautifulSoup
import pandas as pd

IEIP_data = []
IEIP_response = requests.get("https://eduon.com/info/contents/exam_schedule")
html = IEIP_response.text
soup = BeautifulSoup(html, "html.parser")

IEIP_items = soup.select("div.table_wrap > table > tbody > tr")
# division : 회차, written_form : 필기시험 원서, written_exam : 필기시험 날짜, written_result_date : 필기시험 합격자 발표 날짜, 
# practical_form : 실기시험 원서, practical_exam : 실기시험 날짜, final_result_date : 최종 합격자 발표 날짜
for item in IEIP_items:
    division = item.select_one("td:nth-child(1)").text
    written_form = item.select_one("td:nth-child(2)").text
    written_exam = item.select_one("td:nth-child(3)").text
    written_result_date = item.select_one("td:nth-child(4)").text
    practical_form = item.select_one("td:nth-child(5)").text
    practical_exam = item.select_one("td:nth-child(6)").text
    final_result_date = item.select_one("td:nth-child(7)").text
    IEIP_data.append([division, written_form, written_exam, written_result_date, practical_form, practical_exam, final_result_date])
    # IEIP_data.append([days,contents])