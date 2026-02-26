import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
from datetime import datetime
import re

# 파일에 저장하기 위해 리스트 형태로 선언
calender_data = []

# 유한대학교 일정 데이터 크롤링
# 유한대 일정은 데이터 형식이 달라 제외
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
comment = linux_items.find(string=lambda text: isinstance(text, Comment) and "2급" in str(text))
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
            linux_data[-1].update({"practical_form": wrritten_form, "practical_exam": written_exam, "final_result_date": written_result_date})

    elif len(rows) >= 5:
        division = rows[0].text.strip()
        exam_type = rows[1].text.strip()
        wrritten_form = rows[2].text.strip()
        written_exam = rows[3].text.strip()
        written_result_date = rows[4].text.strip()
        if(exam_type == "1차"):
            linux_data.append({"division": division, "written_form": wrritten_form, "written_exam": written_exam, "written_result_date": written_result_date})
        else:
            linux_data[-1].update({"practical_form": wrritten_form, "practical_exam": written_exam, "final_result_date": written_result_date})

    elif len(rows) >=4: 
        exam_type = rows[0].text.strip()
        wrritten_form = rows[1].text.strip()
        written_exam = rows[2].text.strip()
        written_result_date = rows[3].text.strip()
        if(exam_type == "1차"):
            linux_data.append({"division": division, "written_form": wrritten_form, "written_exam": written_exam, "written_result_date": written_result_date})
        else:
            linux_data[-1].update({"practical_form": wrritten_form, "practical_exam": written_exam, "final_result_date": written_result_date})

sqld_data = []
sqld_response = requests.get("https://www.wowpass.com/ExamInfo/235474")
html = sqld_response.text
soup = BeautifulSoup(html, "html.parser")

# sqld_items = soup.find("table.examinfo_col > tbody > tr")
sqld_items = soup.find_all("table", class_="examinfo_col")
select_items = sqld_items[0].find("tbody").find_all("tr")
for item in select_items:
    division = item.select_one("td:nth-child(1)").text
    written_form = ""
    written_exam = ""
    written_result_date = ""
    practical_form = item.select_one("td:nth-child(3)").text
    practical_exam = item.select_one("td:nth-child(2)").text
    final_result_date = item.select_one("td:nth-child(4)").text
    sqld_data.append({"division": division, "written_form": written_form, "written_exam": written_exam, "written_result_date": written_result_date, "practical_form": practical_form, "practical_exam": practical_exam, "final_result_date": final_result_date})

# 엑셀 파일로 저장 (시트별로 분리)
with pd.ExcelWriter("../../01. xlsx/calender_data.xlsx") as writer:
    pd.DataFrame(yuhan_data).to_excel(writer, sheet_name="Yuhan", index=False)
    pd.DataFrame(IEIP_data).to_excel(writer, sheet_name="IEIP", index=False)
    pd.DataFrame(linux_data).to_excel(writer, sheet_name="Linux", index=False)
    pd.DataFrame(sqld_data).to_excel(writer, sheet_name="Sqld", index=False)

# CSV로 저장 (하나의 파일에 모든 데이터)
# source 열을 첫 번째 열로 설정
df_yuhan = pd.DataFrame(yuhan_data)
df_ieip = pd.DataFrame(IEIP_data)
df_ieip.insert(0, 'source', 'IEIP')
df_linux = pd.DataFrame(linux_data)
df_linux.insert(0, 'source', 'Linux')
df_sqld = pd.DataFrame(sqld_data)
df_sqld.insert(0, 'source', 'Sqld')

df_all = pd.concat([df_ieip, df_linux, df_sqld], ignore_index=True)

# 날짜 형식 변환 함수
def convert_to_date_format(date_str):
    """문자열을 YYYY-MM-DD 형식으로 변환"""
    if not date_str or date_str.strip() == "":
        return ""
    
    date_str = date_str.strip()
    
    try:
        # "2026년 02월 24일" 형식
        if "년" in date_str and "월" in date_str and "일" in date_str:
            date_obj = datetime.strptime(date_str, "%Y년 %m월 %d일")
            return date_obj.strftime("%Y-%m-%d")
        
        # "01월 01일" 형식 (유한대학교) - 년도 없음 (현재 년도 2026 추가)
        if "월" in date_str and "일" in date_str:
            parts = date_str.replace("월", " ").replace("일", "").strip().split()
            if len(parts) == 2:
                month, day = parts[0], parts[1]
                return f"2026-{month.zfill(2)}-{day.zfill(2)}"
        
        # "01.27.(화) ~ 02.05.(목)" 또는 "01.30~03.03" 형식 - 첫 번째 날짜만 추출
        if "~" in date_str:
            date_str = date_str.split("~")[0].strip()
        
        # 날짜 문자 제거 (예: "(토)", "(화)" 등)
        date_str = re.sub(r'\([^)]*\)', '', date_str).strip()
        
        # 끝의 특수문자 제거 (예: 끝의 '.')
        date_str = re.sub(r'[\\.\\s]+$', '', date_str).strip()
        
        # "01.30" 또는 "2026.01.30" 형식
        if "." in date_str:
            parts = [p for p in date_str.split(".") if p]  # 빈 문자열 제외
            
            if len(parts) == 2:
                # "01.30" 형식 - 년도 없음 (현재 년도 2026 추가)
                month, day = parts[0].strip(), parts[1].strip()
                return f"2026-{month.zfill(2)}-{day.zfill(2)}"
            
            elif len(parts) >= 3:
                # "2026.01.30" 형식
                year, month, day = parts[0].strip(), parts[1].strip(), parts[2].strip()
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        
        # "2026-02-24" 형식 (이미 변환됨)
        elif date_str.count("-") == 2:
            return date_str
        
        # 다른 형식은 그대로 반환
        else:
            return date_str
    except Exception as e:
        return date_str

# 날짜 필드 변환
# 유한대학교는 'days', 'contents' 컬럼 변환
if not df_yuhan.empty:
    df_yuhan['days'] = df_yuhan['days'].apply(convert_to_date_format)
    df_yuhan['contents'] = df_yuhan['contents'].apply(convert_to_date_format)

# 다른 시험들은 standard 컬럼 변환
date_columns = ["written_form", "written_exam", "written_result_date", "practical_form", "practical_exam", "final_result_date"]
for col in date_columns:
    if col in df_ieip.columns:
        df_ieip[col] = df_ieip[col].apply(convert_to_date_format)
    if col in df_linux.columns:
        df_linux[col] = df_linux[col].apply(convert_to_date_format)
    if col in df_sqld.columns:
        df_sqld[col] = df_sqld[col].apply(convert_to_date_format)

# 데이터 구조 변경: 가로 형식 (항목명 | 날짜)
def restructure_data_horizontal(df, source):
    """데이터를 가로 형식으로 변환: 항목명 | 날짜"""
    new_rows = []
    
    for _, row in df.iterrows():
        division = row.get('division', '')
        
        # 필기 관련 데이터
        if pd.notna(row.get('written_exam', None)) and row['written_exam'] != '':
            if row.get('written_form', '') != '':
<<<<<<< HEAD
                new_rows.append({
                    'source': source,
                    'division': division,
                    'exam_type': '필기',
                    'category': 'written_form',
                    'date': row.get('written_form', '')
                })
            
            new_rows.append({
                'source': source,
                'division': division,
                'exam_type': '필기',
                'category': 'written_exam',
=======
                item = f"{source}_{'필기'}_{('written_form')}_{division}"
                new_rows.append({
                    'item': item,
                    'date': row.get('written_form', '')
                })
            
            item = f"{source}_{('필기')}_{('written_exam')}_{division}"
            new_rows.append({
                'item': item,
>>>>>>> origin/feature/notion_ai
                'date': row.get('written_exam', '')
            })
            
            if row.get('written_result_date', '') != '':
<<<<<<< HEAD
                new_rows.append({
                    'source': source,
                    'division': division,
                    'exam_type': '필기',
                    'category': 'written_result_date',
=======
                item = f"{source}_{('필기')}_{('written_result_date')}_{division}"
                new_rows.append({
                    'item': item,
>>>>>>> origin/feature/notion_ai
                    'date': row.get('written_result_date', '')
                })
        
        # 실기 관련 데이터
        if pd.notna(row.get('practical_exam', None)) and row['practical_exam'] != '':
            if row.get('practical_form', '') != '':
<<<<<<< HEAD
                new_rows.append({
                    'source': source,
                    'division': division,
                    'exam_type': '실기',
                    'category': 'practical_form',
                    'date': row.get('practical_form', '')
                })
            
            new_rows.append({
                'source': source,
                'division': division,
                'exam_type': '실기',
                'category': 'practical_exam',
=======
                item = f"{source}_{('실기')}_{('practical_form')}_{division}"
                new_rows.append({
                    'item': item,
                    'date': row.get('practical_form', '')
                })
            
            item = f"{source}_{('실기')}_{('practical_exam')}_{division}"
            new_rows.append({
                'item': item,
>>>>>>> origin/feature/notion_ai
                'date': row.get('practical_exam', '')
            })
            
            if row.get('final_result_date', '') != '':
<<<<<<< HEAD
                new_rows.append({
                    'source': source,
                    'division': division,
                    'exam_type': '실기',
                    'category': 'final_result_date',
=======
                item = f"{source}_{('실기')}_{('final_result_date')}_{division}"
                new_rows.append({
                    'item': item,
>>>>>>> origin/feature/notion_ai
                    'date': row.get('final_result_date', '')
                })
    
    return pd.DataFrame(new_rows)

# 각 소스별로 재구성
<<<<<<< HEAD
=======
# 유한대학교는 그대로 사용 (days, contents 컬럼을 item, date로 변환)
if not df_yuhan.empty:
    # 날짜 형식을 다시 한 번 확인하면서 변환
    days_formatted = df_yuhan['days'].apply(lambda x: convert_to_date_format(str(x)))
    contents_formatted = df_yuhan['contents'].apply(lambda x: convert_to_date_format(str(x)))
    df_yuhan_restructured = pd.DataFrame({
        'item': days_formatted,
        'date': contents_formatted
    })
else:
    df_yuhan_restructured = pd.DataFrame(columns=['item', 'date'])

>>>>>>> origin/feature/notion_ai
df_ieip_restructured = restructure_data_horizontal(df_ieip, 'IEIP')
df_linux_restructured = restructure_data_horizontal(df_linux, 'Linux')
df_sqld_restructured = restructure_data_horizontal(df_sqld, 'Sqld')

# 모든 데이터 합치기
df_all_restructured = pd.concat([df_yuhan_restructured, df_ieip_restructured, df_linux_restructured, df_sqld_restructured], ignore_index=True)

# CSV 저장 (각 소스별로 분리)
import os
csv_dir = os.path.join(os.path.dirname(__file__), "..", "..", "02. csv")

# 통합 CSV
all_csv_path = os.path.join(csv_dir, "calender_data_restructured.csv")
df_all_restructured[['item', 'date']].to_csv(all_csv_path, index=False, encoding="utf-8-sig")
print(f"통합 CSV 저장: {all_csv_path}")

# 개별 CSV
yuhan_csv_path = os.path.join(csv_dir, "Yuhan_restructured.csv")
df_yuhan_restructured[['item', 'date']].to_csv(yuhan_csv_path, index=False, encoding="utf-8-sig")
print(f"Yuhan CSV 저장: {yuhan_csv_path}")

ieip_csv_path = os.path.join(csv_dir, "IEIP_restructured.csv")
df_ieip_restructured[['item', 'date']].to_csv(ieip_csv_path, index=False, encoding="utf-8-sig")
print(f"IEIP CSV 저장: {ieip_csv_path}")

linux_csv_path = os.path.join(csv_dir, "Linux_restructured.csv")
df_linux_restructured[['item', 'date']].to_csv(linux_csv_path, index=False, encoding="utf-8-sig")
print(f"Linux CSV 저장: {linux_csv_path}")

sqld_csv_path = os.path.join(csv_dir, "Sqld_restructured.csv")
df_sqld_restructured[['item', 'date']].to_csv(sqld_csv_path, index=False, encoding="utf-8-sig")
print(f"Sqld CSV 저장: {sqld_csv_path}")

print("\n=== 재구성된 데이터 샘플 (가로 형식) ===")
print(df_all_restructured.to_string())
