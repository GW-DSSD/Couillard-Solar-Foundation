# import folium 
# import pandas as pd 
# from folium.plugins import Geocoder

# #Read csv file containing coordinates and other factors/features
# data = pd.read_csv('Couillard-Solar-Foundation/Dataset/data.csv').drop(['Unnamed: 0'],axis=1)

# #Intiate a default map 
# usa = folium.Map([44.5, -89.5],zoom_start=7.4)


# #Data preprocessing
# data = data[:-4]
# data["Marker_type"] = data["Type"].replace(["Education", "College", "Adult Education", "Library", "Technical College","School"], 'Education Institutes')
# data["Marker_type"] = data["Marker_type"].replace(["Public Safety", "Human Services"], 'Human Services')

# data.loc[~data["Marker_type"].isin(['Education Institutes', 'Human Services', 'Faith']), "Marker_type"] = 'Others'

# data['Installer'].fillna('Unknown', inplace=True)

# #Grouping the data points based on Marker type
# group_1 = folium.FeatureGroup(name=f'''<span style="color:red;"><i class="fa fa-university"></i> Education Institutes</span>''',overlay=True,control=True).add_to(usa)
# group_2 = folium.FeatureGroup(name=f'''<span style="color:blue;"><i class="fa fa-church"></i> Faith</span>''',overlay=True,control=True).add_to(usa)
# group_3 = folium.FeatureGroup(name=f'''<span style="color:green;"><i class="fa fa-building"></i> Human Services</span>''',overlay=True,control=True).add_to(usa)
# group_4 = folium.FeatureGroup(name=f'''<span style="color:purple;"><i class="fa fa-flag"></i> Others</span>''',overlay=True,control=True).add_to(usa)

# #Function to mark the points on the map accordingly 
# def marker(row,icon_param,group):
#     popup_html = f'<h5>{row["Recipient"]}</h5>' + \
#                  f'<p>({row["Type"]})</p>' + \
#                  f'<b>Project Grant: ${row["Value of grant"]:,}</b><br>' + \
#                  f'<b>Array Size: {row["Size of Array (in kW)"]} kW</b>'

#     #If  the point have Installer
#     if row['Installer'] != 'Unknown':
#         popup_html += f'<br><b>Installer: {row["Installer"]}</b><br>'
#     #If there is a link 
#     if(not pd.isnull(row["link"])):
#         popup_html += '<a style="font-weight:bold" href='+ row["link"] +'> pdf link </a>'
#     #If the point has an image
#     if(not pd.isnull(row["Image URL"])):
#         popup_html += '<center><img src=' + row["Image URL"] + ' alt="logo" height="250" width="400"></center>' 

#     test = folium.Html(popup_html, script=True)
#     popup = folium.Popup(test, max_width=2650)

#     folium.Marker(
#         location=[row["Latitude"], row["Longitude"]],
#         popup=popup,
#         icon=folium.Icon(**icon_param)
#     ).add_to(group)

# #Creating dictionary for marker_type
# marker_types = {
#     'Education Institutes': [{'color': 'red', 'icon': 'university', 'prefix': 'fa'},group_1],
#     'Faith': [{'color': 'blue', 'icon': 'church', 'prefix': 'fa'},group_2],
#     'Human Services': [{'color': 'green', 'icon': 'building', 'prefix': 'fa'},group_3],
#     'Others': [{'color': 'purple', 'icon': 'flag', 'prefix': 'fa'},group_4]
# }


# for marker_type, icon_params in marker_types.items():
#     for idx, row in data[data['Marker_type'] == marker_type].iterrows():
#         marker(row, icon_params[0],icon_params[1])

# borderStyle = {
#     'color' : 'black',
#     'weight' : 2,
#     'fillcolor' : 'black',
#     'fillOpacity' : 0.2

# }
# folium.GeoJson("Couillard-Solar-Foundation/Mapping Work/us-state-boundaries_1.geojson",
#                name="Country",
#                style_function=lambda x:borderStyle).add_to(usa)
# bordersStyle = {
#     'color' : 'white',
#     'weight' : 2,
#     'fillcolor' : 'white',
#     'fillOpacity' : 0

# }

# folium.GeoJson("Couillard-Solar-Foundation/Mapping Work/us-state-boundaries.geojson",
#                name="Wisconsin",
#                style_function=lambda x:bordersStyle).add_to(usa)

# folium.LayerControl().add_to(usa)
# Geocoder().add_to(usa)
# usa.save('Couillard-Solar-Foundation/Mapping Work/Sample Maps/usa.html')

import folium
import pandas as pd
from folium.plugins import Geocoder
import streamlit as st
import os
def preprocessing(data):
    data["Installer"].fillna("Unknown", inplace=True)
    data["Unique ID"] = data["Unique ID"].str.replace("-", "")
    data["Image URL"] = ""
    entries = os.listdir("Project_Pictures/")
    for i in range(data.shape[0]):
        for entry in entries:
            if data["Unique ID"][i] == entry[:4]:
                data["Image URL"][i] = "https://couillardsolarfoundation.org/wp-content/uploads/2023/10/" + entry
            else:
                pass
    return data

def rename_image_urls(data):
    """
    Function that reads a dataframe and then corrects the image link in such a way that replaces all the space in the image url with an underscore
    Returns the dataframe with the corrected image URL
    Example: https://couillardsolarfoundation.org/wp-content/uploads/2023/10/P076-Covenant Lutheran Church arial.jpg
    is renamed as - https://couillardsolarfoundation.org/wp-content/uploads/2023/10/P076-Covenant_Lutheran_Church_arial.jpg 
    """
    corrected_image_link_list = []

    for i in data["Image URL"]:
        corrected_image_link = i
        if len(str(i).split()) > 1:
            print(i)
            corrected_image_link = "_".join(str(i).split())
            print("converted:", corrected_image_link)
        corrected_image_link_list.append(corrected_image_link)

    data["Image URL"] = corrected_image_link_list
    return data

# data = pd.read_csv("Dataset/data.csv").drop(['Unnamed: 0'], axis=1)
def main(data):
    # preprocessing - includes image url insertion
    preprocessed_data = preprocessing(data)
    data = rename_image_urls(preprocessed_data)
    
    print(data.head())
    data.to_csv("PreprocessedData.csv",index=False)

    # Initiate a default map
    usa = folium.Map([44.5, -89.5], zoom_start=7.4)

    # Data preprocessing
    # data = data[:-4]
    data["Marker_type"] = data["Type"].replace(
        ["Education", "College", "Adult Education", "Library", "Technical College", "School"], 'Education Institutes')
    data["Marker_type"] = data["Marker_type"].replace(["Public Safety", "Human Services"], 'Human Services')

    data.loc[~data["Marker_type"].isin(['Education Institutes', 'Human Services', 'Faith']), "Marker_type"] = 'Others'

    data['Installer'].fillna('Unknown', inplace=True)

    # Grouping the data points based on Marker type
    group_1 = folium.FeatureGroup(name=f'''<span style="color:red;"><i class="fa fa-university"></i> Education Institutes</span>''',
                                  overlay=True, control=True).add_to(usa)
    group_2 = folium.FeatureGroup(name=f'''<span style="color:blue;"><i class="fa fa-church"></i> Faith</span>''',
                                  overlay=True, control=True).add_to(usa)
    group_3 = folium.FeatureGroup(name=f'''<span style="color:green;"><i class="fa fa-building"></i> Human Services</span>''',
                                  overlay=True, control=True).add_to(usa)
    group_4 = folium.FeatureGroup(name=f'''<span style="color:purple;"><i class="fa fa-flag"></i> Others</span>''',
                                  overlay=True, control=True).add_to(usa)

    # Function to mark the points on the map accordingly
    def marker(row, icon_param, group):
        popup_html = f'<h5>{row["Recipient"]}</h5>' + \
                     f'<p>({row["Type"]})</p>' + \
                     f'<b>Project Grant: ${row["Value of grant"]:,}</b><br>' + \
                     f'<b>Array Size: {row["Size of Array (in kW)"]} kW</b>'

        
        # If the point has Installer
        if row['Installer'] != 'Unknown':
            popup_html += f'<br><b>Installer: {row["Installer"]}</b><br>'
        try:
            # If there is a link
            if not pd.isnull(row["link"]):
                popup_html += '<a style="font-weight:bold" href=' + row["link"] + '> pdf link </a>'
        except Exception as e:
            pass
        # If the point has an image
        if (len(row["Image URL"]) > 0):     #pd.isnull(row["Image URL"])
            popup_html += '<center><img src=' + row["Image URL"] + ' alt="logo" height="250" width="400"></center>'

        test = folium.Html(popup_html, script=True)
        popup = folium.Popup(test, max_width=2650)

        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=popup,
            icon=folium.Icon(**icon_param)
        ).add_to(group)

    # Creating dictionary for marker_type
    marker_types = {
        'Education Institutes': [{'color': 'red', 'icon': 'university', 'prefix': 'fa'}, group_1],
        'Faith': [{'color': 'blue', 'icon': 'church', 'prefix': 'fa'}, group_2],
        'Human Services': [{'color': 'green', 'icon': 'building', 'prefix': 'fa'}, group_3],
        'Others': [{'color': 'purple', 'icon': 'flag', 'prefix': 'fa'}, group_4]
    }

    for marker_type, icon_params in marker_types.items():
        for idx, row in data[data['Marker_type'] == marker_type].iterrows():
            marker(row, icon_params[0], icon_params[1])

    border_style = {
        'color': 'black',
        'weight': 2,
        'fillcolor': 'black',
        'fillOpacity': 0.2
    }
    folium.GeoJson("Mapping Work/us-state-boundaries_1.geojson",
                   name="Country",
                   style_function=lambda x: border_style).add_to(usa)

    borders_style = {
        'color': 'white',
        'weight': 2,
        'fillcolor': 'white',
        'fillOpacity': 0
    }
    folium.GeoJson("Mapping Work/us-state-boundaries.geojson",
                   name="Wisconsin",
                   style_function=lambda x: borders_style).add_to(usa)

    folium.LayerControl().add_to(usa)
    Geocoder().add_to(usa)

    # Save the map as an HTML file
    usa.save('Mapping Work/Sample Maps/usa.html')

    # Display the map using Streamlit
    # st.markdown('<h1>USA Solar Projects Map</h1>', unsafe_allow_html=True)
    # st.write(usa._repr_html_(), unsafe_allow_html=True)

# if __name__ == '__main__':
#     main(data)






