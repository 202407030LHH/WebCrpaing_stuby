import requests
from bs4 import BeautifulSoup

response = requests.get("https://startcoding.pythonanywhere.com/basic")
html = response.text
soup = BeautifulSoup(html, "html.parser")

category = soup.select_one(".product-category")
name = soup.select_one(".product-name").text

# 별명이 아니기 때문에 불가능
# print(soup.select_one(".product1_detail.html").text)

# 자식 태그를 찾아야 하기 때문에 > 지정자 사용
link = soup.select_one(".product-name > a").attrs['href']

#strip() : 문자열 양쪽의 공백 제거
price_t = soup.select_one(".product-price").text.strip()

price = soup.select_one(".product-price").text.strip().replace(",",'').replace("원",'')
print(category, name, link, price)
