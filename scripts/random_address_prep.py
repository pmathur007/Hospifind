import geocoder

data = []
f = open("C:\\Users\\Ron\\Hospifind\\data\\florida_addresses.txt", "r")
for address in f.readlines():
    g = geocoder.google(address, sensor=False, api_key="")
    print(g.status)
    if g.ok and g.latlng is not None:
        lat, long = g.latlng
        data.append(address + " " + str(lat) + " " + str(long))

if len(data) > 0:
    f.writelines(data)
    print(data)