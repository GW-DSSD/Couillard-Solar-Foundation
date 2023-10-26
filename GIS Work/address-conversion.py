#%%
import numpy as np
import pandas as pd
import geopy
from geopy.geocoders import Nominatim


#%%
""" Function to convert site address into coordinates of latitude and longitude 
:input_param - original_file_name: the original csv file provided by the client that contains the address in a column called "Site Address"
:return - updated dataframe that contains the latitude and longitude coordinates. Can save this dataframe in a csv file
"""
def convert_address_to_coords(original_file_name):
    df = pd.read_excel(original_file_name)

    errorcount_geoapify=0
    import requests
    df["Latitude"]=""
    df["Longitude"]=""
    df["Incomplete Address"]=""
    lats=list()
    longs=list()
    incomplete_address_flag=list()
    # Replace YOUR_API_KEY with your actual API key. Sign up and get an API key on https://www.geoapify.com/ 
    API_KEY = "d7962919004849b8828dd7ab4ddb2bfe"
    for i in df["Site Address"]:
    # Define the address to geocode
        address = i
        try:
            zip_code = int(address.split()[-1])
            incomplete_address_flag.append("FALSE")
        except:
            incomplete_address_flag.append("TRUE")
        
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
            print(f"Request failed with status code {response.status_code} for address {i}")
            incomplete_address_flag.append("TRUE")         
    print("Total errors = "+str(errorcount_geoapify))        

    df["Latitude"]=lats
    df["Longitude"]=longs
    df["Incomplete Address"]=incomplete_address_flag
    return df


converted_df = convert_address_to_coords("Project Site Information for Map.xlsx")
converted_df.head()
converted_df.to_csv("Project Site Information for Map - With GeoApiFy Coordinates.csv")
# %%
# Verification
geoapify_coords = pd.read_csv("Project Site Information for Map - With GeoApiFy Coordinates.csv")
google_earth_pro = pd.read_csv("Project Site Information - coords and full address - GEP.csv")
print(geoapify_coords["Latitude"].head())
print(google_earth_pro["Latitude"].head())

error_count_in_verification=0
for i in range(len(google_earth_pro)):
    if(abs(np.round(google_earth_pro["Latitude"].iloc[i],5) - np.round(geoapify_coords["Latitude"].iloc[i],5))>0.5):
        error_count_in_verification+=1
        print(google_earth_pro["Site Address"].iloc[i])
print(error_count_in_verification)    
    
# %%
