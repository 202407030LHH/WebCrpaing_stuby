import requests
from bs4 import BeautifulSoup
from bs4 import Comment
import pandas as pd

# 리눅스 마스터 일정 데이터 크롤링
# 공식 페이지에서 작업이 어려워서  인비원 사이트 참조
linux_data = []

linux_response = requests.get("https://www.ihd.or.kr/guidecert1.do")
html = linux_response.text
soup = BeautifulSoup(html, "html.parser")

linux_items = soup.select_one(".table_wrap > table > tbody")
comment = linux_items.find(string=lambda text: isinstance(text, Comment) and "리눅스마스터 2급" in str(text))
next_trs = comment.find_next_siblings("tr")  # 다음의 모든 tr 태그

division = "test"
# division : 회차, written_form : 필기시험 원서, written_exam : 필기시험 날짜, written_result_date : 필기시험 합격자 발표 날짜, 
# practical_form : 실기시험 원서, practical_exam : 실기시험 날짜, final_result_date : 최종 합격자 발표 날짜
for item in next_trs:
    rows = item.select("td")
    if len(rows) >= 6:
        division = rows[1].text.strip()
        exam_type = rows[2].text.strip()
        wrritten_form = rows[3].text.strip()
        written_exam = rows[4].text.strip()
        written_result_date = rows[5].text.strip()
        linux_data.append([division, exam_type, wrritten_form, written_exam, written_result_date])

    elif len(rows) >= 5:
        division = rows[0].text.strip()
        exam_type = rows[1].text.strip()
        wrritten_form = rows[2].text.strip()
        written_exam = rows[3].text.strip()
        written_result_date = rows[4].text.strip()
        linux_data.append([division, exam_type, wrritten_form, written_exam, written_result_date])

    elif len(rows) >=4: 
        exam_type = rows[0].text.strip()
        wrritten_form = rows[1].text.strip()
        written_exam = rows[2].text.strip()
        written_result_date = rows[3].text.strip()
        linux_data.append([division, exam_type, wrritten_form, written_exam, written_result_date])
        
    else:
        print("Unexpected row structure:", rows)

    
print(linux_data)