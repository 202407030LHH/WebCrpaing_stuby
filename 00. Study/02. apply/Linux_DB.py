import requests
from bs4 import BeautifulSoup
import pandas as pd

# 리눅스 마스터 일정 데이터 크롤링
# 공식 페이지에서 작업이 어려워서  인비원 사이트 참조
linux_data = []

linux_response = requests.get("https://www.ihd.or.kr/guidecert1.do")
html = linux_response.text
soup = BeautifulSoup(html, "html.parser")

category = soup.select_one("h3")
print(category)    