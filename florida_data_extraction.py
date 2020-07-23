from selenium import webdriver 
from selenium.webdriver.common.action_chains import ActionChains
import time
import os

beds = "https://bi.ahca.myflorida.com/t/ABICC/views/Public/HospitalBedsHospital"
icus = "https://bi.ahca.myflorida.com/t/ABICC/views/Public/ICUBedsHospital"
path = "C:\\Users\\Ron\\Hospifind\\data"
chrome_path = "C:\\Users\\Ron\\GMUInternship\\FitbitAnalysis\\Scripts\\chromedriver.exe"

def press_button(driver, type, identifier):
    clicked = False
    while not clicked:
        buttons = []
        if type == 'name':
            buttons = driver.find_elements_by_class_name(identifier)
        elif type == 'id':
            buttons = driver.find_elements_by_id(identifier)
        elif type == 'text':
            buttons = driver.find_elements_by_xpath(f"//*[contains(text(), '{identifier}')]")
        for button in buttons:
            try:
                # print(button.get_attribute('innerHTML'))
                button.click()
                clicked = True
            except Exception:
                pass

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
prefs = {"download.default_directory": path, "directory_upgrade": True}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options) # service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])

for i in [beds, icus]:
    driver.get(i)
    while True:
        try:
            elem = driver.find_element_by_id("download-ToolbarButton")
            break
        except Exception:
            continue
    ac = ActionChains(driver)
    print(elem)
    ac.move_to_element(elem).move_by_offset(-500, -300).click().perform()
    time.sleep(0.5)
    press_button(driver, 'id', 'download-ToolbarButton')
    time.sleep(0.5)
    press_button(driver, 'text', 'Crosstab')
    time.sleep(0.5)
    print("Download Done")

import update_florida_hospital_data

beds = os.path.join(path, "Hospital_BedsHospital1_crosstab.csv")
icus = os.path.join(path, "ICU_BedsHospital1_crosstab.csv")
if os.path.exists(beds):
    os.remove(beds)
if os.path.exists(icus):
    os.remove(icus)