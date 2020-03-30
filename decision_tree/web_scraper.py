import urllib
import requests
from bs4 import BeautifulSoup
import csv
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

def getInfo(name):
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    query = str(name)
    query = query.replace(' ', '+')
    URL = f"https://google.com/search?q={query}"

    headers = {"user-agent": USER_AGENT}
    resp = requests.get(URL, headers=headers)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
        for s in soup.find_all('span'):
            c = s.get("class")
            if c != None:
                if c[0] == "LrzXr":
                    t = str(s.text)
                    if len(t.split(",")) == 3:
                        locator = Nominatim(user_agent="myGeocoder")
                        #geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
                        location = locator.geocode(t)
                        if location != None:
                            return t, location.longitude, location.latitude
                        else:
                            return t, "", ""

    return "", "", ""


csvfile = open("us_hospital_data.csv",'r', newline = '')
fin = csv.reader(csvfile)

csvfile2 = open('us_data.csv','w+', newline='')
out = csv.writer(csvfile2)
c = 0
for row in fin:
    if row[0] != "Hospital Name":
        name = row[0]
        beds = row[2]
        if int(beds.replace(',','')) > 50:
            address,long,lat = getInfo(name)
            #print(name,address,long,lat,beds,"\n")
            try:
                out.writerow((name,address,long,lat,beds))
            except:
                out.writerow((name,address.encode('utf-8'),long,lat,beds))
    else:
        if c == 0:
            out.writerow(("Name","Address","Long","Lat","Num Beds"))
    c = 1
csvfile2.close()
