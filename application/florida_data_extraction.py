import requests
from bs4 import BeautifulSoup

beds = "https://bi.ahca.myflorida.com/t/ABICC/views/Public/HospitalBedsHospital"
icus = "https://bi.ahca.myflorida.com/t/ABICC/views/Public/ICUBedsHospital"

beds_page = requests.get(beds)
icus_page = requests.get(icus)

beds_soup = BeautifulSoup(beds_page.content, 'html.parser')

print(beds_soup)

