import requests
import pprint
from bs4 import BeautifulSoup
import csv

URL = 'https://floridadisaster.org/covid19/testing-sites/'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find_all('p')
centers = []
uls = soup.find_all('ul')[31:86]
for result in results:
    if result.find('strong') and result.find('br'):
        centers.append(result)


csvfile2 = open('florida_testdata.csv','w+', newline='')
out = csv.writer(csvfile2)
out.writerow(("Name","Address", "Appointments Required", "Hours of Operation", "Type" ,"Phone-Number"))
#out.writerow(("Name", "Address"))
for val, ul in zip(centers, uls):
    items = ul.find_all('li')
    appointments = False
    availability = ""
    for item in items:
        if("appointment" in item.text.strip().lower()):
            appointments = True
        if("hours of operation" in item.text.strip().lower()):
            availability = item.get_text(separator=" ").strip()[19:]


    name_center = val.find('strong').text.strip()
    address = val.get_text(separator=" ").strip()
   # print(address)
    address_center= address[len(name_center):]
    #print(address_center)
    out.writerow((name_center, address_center, appointments, availability))

csvfile2.close()
