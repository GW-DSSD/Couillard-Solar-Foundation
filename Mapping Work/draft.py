import folium 
import pandas as pd 
from folium.plugins import Geocoder

#Read csv file containing coordinates and other factors/features
data = pd.read_csv('Couillard-Solar-Foundation/Dataset/data.csv').drop(['Unnamed: 0'],axis=1)

#Intiate a default map 
usa = folium.Map([44.5, -89.5],zoom_start=7.4)


#Data preprocessing
data = data[:-4]
data["Marker_type"] = data["Type"].replace(["Education", "College", "Adult Education", "Library", "Technical College","School"], 'Education Institutes')
data["Marker_type"] = data["Marker_type"].replace(["Public Safety", "Human Services"], 'Human Services')

data.loc[~data["Marker_type"].isin(['Education Institutes', 'Human Services', 'Faith']), "Marker_type"] = 'Others'

data['Installer'].fillna('Unknown', inplace=True)

#Grouping the data points based on Marker type
group_1 = folium.FeatureGroup(name=f'''<span style="color:red;"><i class="fa fa-university"></i> Education Institutes</span>''',overlay=True,control=True).add_to(usa)
group_2 = folium.FeatureGroup(name=f'''<span style="color:blue;"><i class="fa fa-church"></i> Faith</span>''',overlay=True,control=True).add_to(usa)
group_3 = folium.FeatureGroup(name=f'''<span style="color:green;"><i class="fa fa-building"></i> Human Services</span>''',overlay=True,control=True).add_to(usa)
group_4 = folium.FeatureGroup(name=f'''<span style="color:purple;"><i class="fa fa-flag"></i> Others</span>''',overlay=True,control=True).add_to(usa)

#Function to mark the points on the map accordingly 
def marker(row,icon_param,group):
    popup_html = f'<h5>{row["Recipient"]}</h5>' + \
                 f'<p>({row["Type"]})</p>' + \
                 f'<b>Project Grant: ${row["Value of grant"]:,}</b><br>' + \
                 f'<b>Array Size: {row["Size of Array (in kW)"]} kW</b>'

    #If  the point have Installer
    if row['Installer'] != 'Unknown':
        popup_html += f'<br><b>Installer: {row["Installer"]}</b><br>'
    #If there is a link 
    if(not pd.isnull(row["link"])):
        popup_html += '<a style="font-weight:bold" href='+ row["link"] +'> pdf link </a>'
    #If the point has an image
    if(not pd.isnull(row["Image URL"])):
        popup_html += '<center><img src=' + row["Image URL"] + ' alt="logo" height="250" width="400"></center>' 

    test = folium.Html(popup_html, script=True)
    popup = folium.Popup(test, max_width=2650)

    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=popup,
        icon=folium.Icon(**icon_param)
    ).add_to(group)

#Creating dictionary for marker_type
marker_types = {
    'Education Institutes': [{'color': 'red', 'icon': 'university', 'prefix': 'fa'},group_1],
    'Faith': [{'color': 'blue', 'icon': 'church', 'prefix': 'fa'},group_2],
    'Human Services': [{'color': 'green', 'icon': 'building', 'prefix': 'fa'},group_3],
    'Others': [{'color': 'purple', 'icon': 'flag', 'prefix': 'fa'},group_4]
}


for marker_type, icon_params in marker_types.items():
    for idx, row in data[data['Marker_type'] == marker_type].iterrows():
        marker(row, icon_params[0],icon_params[1])

borderStyle = {
    'color' : 'black',
    'weight' : 2,
    'fillcolor' : 'black',
    'fillOpacity' : 0.2

}
folium.GeoJson("Couillard-Solar-Foundation/Mapping Work/us-state-boundaries_1.geojson",
               name="Country",
               style_function=lambda x:borderStyle).add_to(usa)
bordersStyle = {
    'color' : 'white',
    'weight' : 2,
    'fillcolor' : 'white',
    'fillOpacity' : 0

}

folium.GeoJson("Couillard-Solar-Foundation/Mapping Work/us-state-boundaries.geojson",
               name="Wisconsin",
               style_function=lambda x:bordersStyle).add_to(usa)

folium.LayerControl().add_to(usa)
Geocoder().add_to(usa)
usa.save('Couillard-Solar-Foundation/Mapping Work/Sample Maps/usa.html')










