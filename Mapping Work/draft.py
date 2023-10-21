import folium 
import pandas as pd 
from folium.plugins import Geocoder


data = pd.read_csv('Project Site Information for Map - Coordinates.csv')

usa = folium.Map([37.0902,-95.7129],zoom_start=4)

data = data[:-4]
data["Marker_type"] = data["Type"].replace(["Education", "College", "Adult Education", "Library", "Technical College","School"], 'Education Institutes')
data["Marker_type"] = data["Marker_type"].replace(["Public Safety", "Human Services"], 'Human Services')

data.loc[~data["Marker_type"].isin(['Education Institutes', 'Human Services', 'Faith']), "Marker_type"] = 'Other'

group_1 = folium.FeatureGroup("Education Institutes").add_to(usa)
group_2 = folium.FeatureGroup("Faith").add_to(usa)
group_3 = folium.FeatureGroup("Human Services").add_to(usa)
group_4 = folium.FeatureGroup("Others").add_to(usa)

data['Installer'].fillna('Unknown', inplace=True)
#print(pd.value_counts(data["Marker_type"]))
for idx, row in data.iterrows():
    row['Value of grant'] = str('{:,}'.format(row['Value of grant']))
    if (row['Marker_type'] == 'Education Institutes'):
        if(row['Installer'] != 'Unknown'):
            test = folium.Html('<h5>'+row["Recipient"]+'</h5>'+'<p>('+row['Type']+')</p>'+'<b> Project Grant : $' +str(row['Value of grant'])+ '</b> <br>'+'<b> Array Size : '+str(row['Size of Array (in kW)'])+'</b> <br>'+'<b> Installer :'+row['Installer']+'</b>', script=True)
            popup = folium.Popup(test, max_width=2650)
            folium.Marker(location=[row["Latitude"], row["Longitude"]],popup=popup,icon=folium.Icon(color='red',icon='university', prefix='fa')).add_to(group_1)
        else:
            test = folium.Html('<h5>'+row["Recipient"]+'</h5>'+'<p>('+row['Type']+')</p>'+'<b> Project Grant : $' +str(row['Value of grant'])+ '</b> <br>'+'<b> Array Size : '+str(row['Size of Array (in kW)'])+'</b>', script=True)
            popup = folium.Popup(test, max_width=2650)
            folium.Marker(location=[row["Latitude"], row["Longitude"]],popup=popup,icon=folium.Icon(color='red',icon='university', prefix='fa')).add_to(group_1)

    
    elif (row['Marker_type'] == 'Faith'):
        if(row['Installer'] != 'Unknown'):
            test = folium.Html('<h5>'+row["Recipient"]+'</h5>'+'<p>('+row['Type']+')</p>'+'<b> Project Grant : $' +str(row['Value of grant'])+ '</b> <br>'+'<b> Array Size : '+str(row['Size of Array (in kW)'])+'</b> <br>'+'<b> Installer :'+row['Installer']+'</b>', script=True)
            popup = folium.Popup(test, max_width=2650)
            folium.Marker(location=[row["Latitude"], row["Longitude"]],popup=popup,icon=folium.Icon(color='blue',icon='church', prefix='fa')).add_to(group_2)
        else:
            test = folium.Html('<h5>'+row["Recipient"]+'</h5>'+'<p>('+row['Type']+')</p>'+'<b> Project Grant : $' +str(row['Value of grant'])+ '</b> <br>'+'<b> Array Size : '+str(row['Size of Array (in kW)'])+'</b>', script=True)
            popup = folium.Popup(test, max_width=2650)
            folium.Marker(location=[row["Latitude"], row["Longitude"]],popup=popup,icon=folium.Icon(color='blue',icon='church', prefix='fa')).add_to(group_2)

    elif(row['Marker_type'] == 'Human Services'):
        if(row['Installer'] != 'Unknown'):
            test = folium.Html('<h5>'+row["Recipient"]+'</h5>'+'<p>('+row['Type']+')</p>'+'<b> Project Grant : $' +str(row['Value of grant'])+ '</b> <br>'+'<b> Array Size : '+str(row['Size of Array (in kW)'])+'</b> <br>'+'<b> Installer :'+row['Installer']+'</b>', script=True)
            popup = folium.Popup(test, max_width=2650)
            folium.Marker(location=[row["Latitude"], row["Longitude"]],popup=popup,icon=folium.Icon(color='green',icon='building', prefix='fa')).add_to(group_3)
        else:
            test = folium.Html('<h5>'+row["Recipient"]+'</h5>'+'<p>('+row['Type']+')</p>'+'<b> Project Grant : $' +str(row['Value of grant'])+ '</b> <br>'+'<b> Array Size : '+str(row['Size of Array (in kW)'])+'</b>', script=True)
            popup = folium.Popup(test, max_width=2650)
            folium.Marker(location=[row["Latitude"], row["Longitude"]],popup=popup,icon=folium.Icon(color='green',icon='building', prefix='fa')).add_to(group_3)
    
    else:
        if(row['Installer'] != 'Unknown'):
            test = folium.Html('<h5>'+row["Recipient"]+'</h5>'+'<p>('+row['Type']+')</p>'+'<b> Project Grant : $' +str(row['Value of grant'])+ '</b> <br>'+'<b> Array Size : '+str(row['Size of Array (in kW)'])+'</b> <br>'+'<b> Installer :'+row['Installer']+'</b>', script=True)
            popup = folium.Popup(test, max_width=2650)
            folium.Marker(location=[row["Latitude"], row["Longitude"]],popup=popup,icon=folium.Icon(color='purple',icon='flag', prefix='fa')).add_to(group_4)
        else:
            test = folium.Html('<h5>'+row["Recipient"]+'</h5>'+'<p>('+row['Type']+')</p>'+'<b> Project Grant : $' +str(row['Value of grant'])+ '</b> <br>'+'<b> Array Size : '+str(row['Size of Array (in kW)'])+'</b>', script=True)
            popup = folium.Popup(test, max_width=2650)
            folium.Marker(location=[row["Latitude"], row["Longitude"]],popup=popup,icon=folium.Icon(color='purple',icon='flag', prefix='fa')).add_to(group_4)

folium.LayerControl().add_to(usa)
Geocoder().add_to(usa)
usa.save('usa.html')

# # for idx, row in data.iterrows():
# #     folium.CircleMarker(location=[row["Latitude"], row["Longitude"]],radius=25,fill=True,popup=row["Place Name"]).add_to(usa)
# usa.save('usa.html')

