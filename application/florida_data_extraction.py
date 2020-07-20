import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from arcgis.gis import GIS
from selenium import webdriver 
import time
import os

beds = "https://bi.ahca.myflorida.com/t/ABICC/views/Public/HospitalBedsHospital"
icus = "https://bi.ahca.myflorida.com/t/ABICC/views/Public/ICUBedsHospital"

def press_button(driver, type, identifier):
    clicked = False
    while not clicked:
        buttons = []
        if type == 'name':
            buttons = driver.find_elements_by_class_name(identifier)
        elif type == 'id':
            buttons = driver.find_elements_by_id(identifier)
        for button in buttons:
            try:
                button.click()
                clicked = True
            except Exception:
                pass

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path='C:\\Users\\Ron\\GMUInternship\\FitbitAnalysis\\Scripts\\chromedriver.exe', options=chrome_options) # service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])

driver.get(beds)
press_button(driver, 'id', 'download-ToolbarButton')
print("TITLE: ", driver.title, sep="")
soup = BeautifulSoup(driver.page_source, 'html.parser')
print("SOURCE", soup, sep="\n")
