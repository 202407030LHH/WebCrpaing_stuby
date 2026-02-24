import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd

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
    sqld_data.append([division, written_form, written_exam, written_result_date, practical_form, practical_exam, final_result_date])
    
print(sqld_data)