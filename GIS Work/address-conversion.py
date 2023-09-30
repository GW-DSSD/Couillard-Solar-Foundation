#%%
import numpy as np
import pandas as pd
import geopy
from geopy.geocoders import Nominatim

# %%
df = pd.read_excel("Project Site Information for Map.xlsx")
df.head()
df.info()
# %%
errorCount=0
print(errorCount)
# %%
errorcount_geoapify=0
import requests
df["Latitude"]=""
df["Longitude"]=""
lats=list()
longs=list()
# Replace YOUR_API_KEY with your actual API key. Sign up and get an API key on https://www.geoapify.com/ 
API_KEY = "d7962919004849b8828dd7ab4ddb2bfe"
for i in df["Site Address"]:
# Define the address to geocode
    address = i

# Build the API URL
    url = f"https://api.geoapify.com/v1/geocode/search?text={address}&limit=1&apiKey={API_KEY}"

    # Send the API request and get the response
    response = requests.get(url)

    # Check the response status code
    if response.status_code == 200:
        # Parse the JSON data from the response
        data = response.json()

        # Extract the first result from the data
        result = data["features"][0]

        # Extract the latitude and longitude of the result
        latitude = result["geometry"]["coordinates"][1]
        longitude = result["geometry"]["coordinates"][0]

        print(f"Latitude: {latitude}, Longitude: {longitude}")
        
        lats.append(latitude)
        longs.append(longitude)
    else:
        errorcount_geoapify+=1
        print(f"Request failed with status code {response.status_code}")
        
print("Total errors = "+str(errorcount_geoapify))        
# %%
df["Latitude"]=lats
df["Longitude"]=longs
df.to_csv("Project Site Information for Map - With Coordinates.csv")
df.head()
# %%
