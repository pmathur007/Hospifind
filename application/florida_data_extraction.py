import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

beds = "https://bi.ahca.myflorida.com/t/ABICC/views/Public/HospitalBedsHospital"
icus = "https://bi.ahca.myflorida.com/t/ABICC/views/Public/ICUBedsHospital"

# beds_page = requests.get(beds)
# icus_page = requests.get(icus)
# beds_soup = BeautifulSoup(beds_page.content, 'html.parser')
# print(beds_soup)

session = HTMLSession()
beds_resp = session.get(beds)
beds_resp.html.render()
soup = BeautifulSoup(beds_resp.html.html, 'html.parser')
print(soup)