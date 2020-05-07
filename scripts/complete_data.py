import pandas as pd
import os
from os import path
import geocoder

# if path.exists(os.path.join('application', 'environment_variables.txt')):
#     f = open(os.path.join('application', 'environment_variables.txt'), 'r')
#     google_api_key = f.readline().strip()
#
#     csv = os.path.join(os.getcwd(), 'all_us_data.csv')
#     df = pd.read_csv(csv)
#     df = df.dropna(thresh=3)
#     print(df)
#
#     for i, row in df.iterrows():
#         if not pd.isnull(df['Name'][i]) and not pd.isnull(df['Address'][i]):
#             if pd.isnull(df['Lat'][i]) or pd.isnull(df['Long'][i]):
#                 g = geocoder.google(df['Address'][i], key=google_api_key)
#                 if g.ok and g.latlng[0] is not None:
#                     latlng = g.latlng
#                     df['Lat'][i] = latlng[0]; df['Long'][i] = latlng[1]
#                     print(latlng)
#
#     df.to_csv('filled_all_us_data.csv', index=False)

csv = os.path.join(os.path.dirname(os.getcwd()), 'data', 'all_us_data.csv')
df = pd.read_csv(csv)
df = df.dropna(thresh=2)
print(df)

count = 0
for i, row in df.iterrows():
    if not pd.isnull(df['Name'][i]) and pd.isnull(df['Address'][i]):
        print(df['Name'][i])
        count += 1

print(count)
