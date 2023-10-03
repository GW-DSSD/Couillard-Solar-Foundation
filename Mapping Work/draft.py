import folium 
import pandas as pd 

data = pd.read_csv('Project Site Information for Map - Coordinates.csv')

usa = folium.Map([37.0902,-95.7129],zoom_start=4)

data = data[:-4]
data["Marker_type"] = data["Type"].replace(["Education", "College", "Adult Education", "Library", "Technical College","School"], 'Education Institutes')
data["Marker_type"] = data["Marker_type"].replace(["Public Safety", "Recreation", "Human Services"], 'Public Services')

data.loc[~data["Marker_type"].isin(['Education Institutes', 'Public Services', 'Faith']), "Marker_type"] = 'Other'

group_1 = folium.FeatureGroup("Education Institutes").add_to(usa)
group_2 = folium.FeatureGroup("Faith").add_to(usa)
group_3 = folium.FeatureGroup("Public Services").add_to(usa)
group_4 = folium.FeatureGroup("Others").add_to(usa)


#print(pd.value_counts(data["Marker_type"]))
for idx, row in data.iterrows():
    if (row['Marker_type'] == 'Education Institutes'):
        variable = row["Recipient"]
        test = folium.Html('<h5>'+variable+'</h5>', script=True)
        popup = folium.Popup(test, max_width=2650)
        folium.Marker(location=[row["Latitude"], row["Longitude"]],popup=popup,icon=folium.Icon(color='red',icon='university', prefix='fa')).add_to(group_1)
    
    elif (row['Marker_type'] == 'Faith'):
        variable = row["Recipient"]
        test = folium.Html('<h5>'+variable+'</h5>', script=True)
        popup = folium.Popup(test, max_width=2650)
        folium.Marker(location=[row["Latitude"], row["Longitude"]],popup=popup,icon=folium.Icon(color='blue',icon='church', prefix='fa')).add_to(group_2)

    elif(row['Marker_type'] == 'Public Services'):
        variable = row["Recipient"]
        test = folium.Html('<h5>'+variable+'</h5>', script=True)
        popup = folium.Popup(test, max_width=2650)
        folium.Marker(location=[row["Latitude"], row["Longitude"]],popup=popup,icon=folium.Icon(color='green',icon='building', prefix='fa')).add_to(group_3)
    
    else:
        variable = row["Recipient"]
        test = folium.Html('<h5>'+variable+'</h5>', script=True)
        popup = folium.Popup(test, max_width=2650)
        folium.Marker(location=[row["Latitude"], row["Longitude"]],popup=popup,icon=folium.Icon(color='purple',icon='flag', prefix='fa')).add_to(group_4)

folium.LayerControl().add_to(usa)
usa.save('usa.html')

# # for idx, row in data.iterrows():
# #     folium.CircleMarker(location=[row["Latitude"], row["Longitude"]],radius=25,fill=True,popup=row["Place Name"]).add_to(usa)
# usa.save('usa.html')

