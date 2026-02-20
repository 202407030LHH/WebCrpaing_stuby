import requests
from bs4 import BeautifulSoup
import pandas as pd

# 리눅스 마스터 일정 데이터 크롤링
# 공식 페이지에서 작업이 어려워서  인비원 사이트 참조
linux_data = []

linux_response = requests.get("https://www.invione.com/board/lic/220")
html = linux_response.text
soup = BeautifulSoup(html, "html.parser")

linux_items = soup.select("div.lic_date > h4")

for item in linux_items:
    division = item.select_one(".lic_h4")
    # written_form = item.select_one("lic_dd:nth-child(1)")
    # written_exam = item.select_one("lic_dd:nth-child(2)")
    # written_result_date = item.select_one("lic_dd:nth-child(3)")
    # practical_form = item.select_one("lic_dd:nth-child(4)")
    # practical_exam = item.select_one("lic_dd:nth-child(5)")
    print(division)

