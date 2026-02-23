import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd

# 파일에 저장하기 위해 리스트 형태로 선언
calender_data = []

# 유한대학교 일정 데이터 크롤링
yuhan_data = []
yuhan_response = requests.get("https://www.yuhan.ac.kr/collegeService/schedule.do?menu_idx=3124&year=2026&toMonth=2&option=&SCH_DAY=&calPopDayId=&cal_Type=2")
html = yuhan_response.text
soup = BeautifulSoup(html, "html.parser")

yuhan_items = soup.select("tbody > tr > td > ul > li")
for item in yuhan_items:
    days = item.select_one("strong").text
    contents = item.select_one("p").text
    yuhan_data.append({"days": days, "contents": contents})

# 정보처리산업기사 일정 데이터 크롤링
IEIP_data = []
IEIP_response = requests.get("https://eduon.com/info/contents/exam_schedule")
html = IEIP_response.text
soup = BeautifulSoup(html, "html.parser")

# IEIP_items = soup.select_select("div.table_wrap > table > tbody")
IEIP_items = soup.find("tbody").find_all("tr")
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
    IEIP_data.append({"division": division, "written_form": written_form, "written_exam": written_exam, "written_result_date": written_result_date, "practical_form": practical_form, "practical_exam": practical_exam, "final_result_date": final_result_date})
    
linux_data = []

linux_response = requests.get("https://www.ihd.or.kr/guidecert1.do")
html = linux_response.text
soup = BeautifulSoup(html, "html.parser")

linux_items = soup.select_one(".table_wrap > table > tbody")
comment = linux_items.find(string=lambda text: isinstance(text, Comment) and "리눅스마스터 2급" in str(text))
next_trs = comment.find_next_siblings("tr")  # 다음의 모든 tr 태그

division = "reset"
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
        if(exam_type == "1차"):
            linux_data.append({"division": division, "written_form": wrritten_form, "written_exam": written_exam, "written_result_date": written_result_date})
        else:
            linux_data.update({"practical_form": wrritten_form, "practical_exam": written_exam, "final_result_date": written_result_date})

    elif len(rows) >= 5:
        division = rows[0].text.strip()
        exam_type = rows[1].text.strip()
        wrritten_form = rows[2].text.strip()
        written_exam = rows[3].text.strip()
        written_result_date = rows[4].text.strip()
        if(exam_type == "1차"):
            linux_data.append({"division": division, "written_form": wrritten_form, "written_exam": written_exam, "written_result_date": written_result_date})
        else:
            linux_data.update({"practical_form": wrritten_form, "practical_exam": written_exam, "final_result_date": written_result_date})

    elif len(rows) >=4: 
        exam_type = rows[0].text.strip()
        wrritten_form = rows[1].text.strip()
        written_exam = rows[2].text.strip()
        written_result_date = rows[3].text.strip()
        if(exam_type == "1차"):
            linux_data.append({"division": division, "written_form": wrritten_form, "written_exam": written_exam, "written_result_date": written_result_date})
        else:
            linux_data[-1].update({"practical_form": wrritten_form, "practical_exam": written_exam, "final_result_date": written_result_date})


with pd.ExcelWriter("../../01. xlsx/calender_data.xlsx") as writer:
    pd.DataFrame(yuhan_data).to_excel(writer, sheet_name="Yuhan", index=False)
    pd.DataFrame(IEIP_data).to_excel(writer, sheet_name="IEIP", index=False)
    pd.DataFrame(linux_data).to_excel(writer, sheet_name="Linux", index=False)