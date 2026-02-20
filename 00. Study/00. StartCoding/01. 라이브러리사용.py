import requests
from bs4 import BeautifulSoup

response = requests.get("https://startcoding.pythonanywhere.com/basic")
html = response.text
soup = BeautifulSoup(html, "html.parser")

#select의 요소에 코드를 다 들고 옮
print(soup.select_one(".brand-name"))

#select의 요소의 내용 중 텍스트만 가지고 옮
print(soup.select_one(".brand-name").text)

#select의 요소 중 ()안에 원하는 키만 가지고 오거나, 전체 키의 요소를 가지고 옮
print(soup.select_one(".brand-name").attrs)


