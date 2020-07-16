from arcgis.gis import GIS 
import os 
from zipfile import ZipFile
import time

data_id = '7572b118dc3c48d885d1c643c195314e/'
directory = "C:\\Users\\Ron\\Hospifind\\application\\testing_centers"

anon_gis = GIS()
data = anon_gis.content.get(data_id)
data_path = os.path.join(directory, "data")


if not os.path.isdir(data_path):
    os.mkdir(data_path)
zip_path = os.path.join(data_path, "Florida's Coronavirus Community Dashboard.zip")
extract_path = os.path.join(data_path, "fl")

data.download(save_path=data_path)

zip_file = ZipFile(zip_path)
time.sleep(3)
zip_file.extractall(path=extract_path)