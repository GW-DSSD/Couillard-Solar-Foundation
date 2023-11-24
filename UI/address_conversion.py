import pandas as pd
import numpy as np
import streamlit as st
import time

def convert_address_to_coords(original_file_name,progress_callback=None):
    df = pd.read_excel(original_file_name,header=0)

    addresses_converted =0
    total_addresses=0
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
    for row, i in enumerate(df["Site Address"]):
        total_addresses+=1
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
        print("Address:",address)
        # Check the response status code
        if response.status_code == 200:
            try:
                # Parse the JSON data from the response
                data = response.json()

                # Extract the first result from the data
                result = data["features"][0]

                # Extract the latitude and longitude of the result
                latitude = result["geometry"]["coordinates"][1]
                longitude = result["geometry"]["coordinates"][0]

                print(f"Latitude: {latitude}, Longitude: {longitude}")
                time.sleep(0.1)
                progress = int((row + 1) / len(df) * 100)
                if progress_callback:
                    progress_callback(progress)
                lats.append(latitude)
                longs.append(longitude)
                addresses_converted+=1
            except Exception as e:
                errorcount_geoapify+=1
                print(f"Error processing address {address}: {e}")
        else:
            lats.append(np.nan)
            longs.append(np.nan)
            errorcount_geoapify+=1
            print(f"Request failed with status code {response.status_code} for address {i}")
            incomplete_address_flag.append("TRUE")         
    print("Total errors = "+str(errorcount_geoapify))        

    df["Latitude"]=lats
    df["Longitude"]=longs
    df["Incomplete Address"]=incomplete_address_flag
    st.write("Number of total addresses to be converted: ",total_addresses)
    st.write("Number of total addresses converted successfully: ",addresses_converted)
    st.write("Number of total addresses that were incomplete (without zip codes): " + str(incomplete_address_flag.count(True)))
    st.write("Number of total address conversions that failed: ",errorcount_geoapify)
    return df