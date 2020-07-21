from selenium import webdriver
import time
import os

os.system("chromedriver --url-base=/wd/hub")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=chrome_options) # service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])

beds = "https://bi.ahca.myflorida.com/t/ABICC/views/Public/HospitalBedsHospital"
icus = "https://bi.ahca.myflorida.com/t/ABICC/views/Public/ICUBedsHospital"
dashboard = "https://experience.arcgis.com/experience/7572b118dc3c48d885d1c643c195314e/"

driver.get("https://python.org")
# time.sleep(3)
# press_button(driver, 'id', 'ember715')
print(driver.title)
