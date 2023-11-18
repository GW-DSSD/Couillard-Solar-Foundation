import folium 
import pandas as pd 
from folium.plugins import Geocoder

#Read csv file containing coordinates and other factors/features
data = pd.read_csv('Dataset/multi_image_data.csv').drop(['Unnamed: 0'],axis=1)

#Intiate a default map 
usa = folium.Map([43.7844,-88.7879],zoom_start=7)


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
group_5 = folium.FeatureGroup(name='''<style> #gallerywrapper { width:640px; height:450px; margin:0 auto; position:relative; font-family:verdana, arial, sans-serif; } #gallerywrapper #gallery { position:absolute; left:0; top:0; height:450px; width:640px; overflow:hidden; text-align:center; } #gallerywrapper #gallery div { width:640px; height:900px; padding-top:10px; position:relative; } #gallerywrapper #gallery div img { clear:both; display:block; margin:0 auto; border:0; } #gallerywrapper #gallery div h3 { padding:10px 0 0 0; margin:0; font-size:18px; } #gallerywrapper #gallery div p { padding:5px 0; margin:0; font-size:12px; line-height:18px; } #gallery .previous{ display:inline; float:left; margin-left:80px; text-decoration:none; } #gallery .next{ display:inline; float:right; margin-right:80px; text-decoration:none; } </style>''',overlay=True,control=True).add_to(usa)

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
        img_list = eval(row["Image URL"])
        popup_html += '<div id="gallerywrapper"><div id="gallery">'
        for i in range(len(img_list)):
            current_pic = i
            next_pic = i+1 if i != len(img_list)-1 else 0
            prev_pic = i-1 if i != 0 else len(img_list)-1
            popup_html += f'<div id="pic{current_pic}"><img src="{img_list[current_pic]}" height="350" width="500" alt="Image {current_pic}"><a class="previous" href="#pic{prev_pic}">&lt;</a><a class="next" href="#pic{next_pic}">&gt;</a></div>'
        popup_html += '</div></div>'

        # popup_html += '<center><img src=' + row["Image URL"] + ' alt="logo"  height="250" width="400"></center>' 

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

folium.LayerControl().add_to(usa)
Geocoder().add_to(usa)
usa.save('dev/usa_multi_img.html')









# #print(pd.value_counts(data["Marker_type"]))
# for idx, row in data.iterrows():
#     row['Value of grant'] = str('{:,}'.format(row['Value of grant']))
#     if (row['Marker_type'] == 'Education Institutes'):
#         if(not pd.isnull(row["Image URL"])):
#             if(row['Installer'] != 'Unknown'):
#                 test = folium.Html('<center><img src=' + row["Image URL"] + ' alt="logo" width=100 height=100 ></center>'+'<h5>'+row["Recipient"]+'</h5>'+'<p>('+row['Type']+')</p>'+'<b> Project Grant : $' +str(row['Value of grant'])+ '</b> <br>'+'<b> Array Size : '+str(row['Size of Array (in kW)'])+'</b> <br>'+'<b> Installer :'+row['Installer']+'</b>', script=True)
#                 popup = folium.Popup(test, max_width=2650)
#                 folium.Marker(location=[row["Latitude"], row["Longitude"]],popup=popup,icon=folium.Icon(color='red',icon='university', prefix='fa')).add_to(group_1)
#             else:
#                 test = folium.Html('<h5>'+row["Recipient"]+'</h5>'+'<p>('+row['Type']+')</p>'+'<b> Project Grant : $' +str(row['Value of grant'])+ '</b> <br>'+'<b> Array Size : '+str(row['Size of Array (in kW)'])+'</b>', script=True)
#                 popup = folium.Popup(test, max_width=2650)
#                 folium.Marker(location=[row["Latitude"], row["Longitude"]],popup=popup,icon=folium.Icon(color='red',icon='university', prefix='fa')).add_to(group_1)
#         else:
#             if(row['Installer'] != 'Unknown'):
#                 test = folium.Html('<h5>'+row["Recipient"]+'</h5>'+'<p>('+row['Type']+')</p>'+'<b> Project Grant : $' +str(row['Value of grant'])+ '</b> <br>'+'<b> Array Size : '+str(row['Size of Array (in kW)'])+'</b> <br>'+'<b> Installer :'+row['Installer']+'</b>', script=True)
#                 popup = folium.Popup(test, max_width=2650)
#                 folium.Marker(location=[row["Latitude"], row["Longitude"]],popup=popup,icon=folium.Icon(color='red',icon='university', prefix='fa')).add_to(group_1)
#             else:
#                 test = folium.Html('<h5>'+row["Recipient"]+'</h5>'+'<p>('+row['Type']+')</p>'+'<b> Project Grant : $' +str(row['Value of grant'])+ '</b> <br>'+'<b> Array Size : '+str(row['Size of Array (in kW)'])+'</b>', script=True)
#                 popup = folium.Popup(test, max_width=2650)
#                 folium.Marker(location=[row["Latitude"], row["Longitude"]],popup=popup,icon=folium.Icon(color='red',icon='university', prefix='fa')).add_to(group_1)

    
#     elif (row['Marker_type'] == 'Faith'):
#         if(row['Installer'] != 'Unknown'):
#             test = folium.Html('<h5>'+row["Recipient"]+'</h5>'+'<p>('+row['Type']+')</p>'+'<b> Project Grant : $' +str(row['Value of grant'])+ '</b> <br>'+'<b> Array Size : '+str(row['Size of Array (in kW)'])+'</b> <br>'+'<b> Installer :'+row['Installer']+'</b>', script=True)
#             popup = folium.Popup(test, max_width=2650)
#             folium.Marker(location=[row["Latitude"], row["Longitude"]],popup=popup,icon=folium.Icon(color='blue',icon='church', prefix='fa')).add_to(group_2)
#         else:
#             test = folium.Html('<h5>'+row["Recipient"]+'</h5>'+'<p>('+row['Type']+')</p>'+'<b> Project Grant : $' +str(row['Value of grant'])+ '</b> <br>'+'<b> Array Size : '+str(row['Size of Array (in kW)'])+'</b>', script=True)
#             popup = folium.Popup(test, max_width=2650)
#             folium.Marker(location=[row["Latitude"], row["Longitude"]],popup=popup,icon=folium.Icon(color='blue',icon='church', prefix='fa')).add_to(group_2)

#     elif(row['Marker_type'] == 'Human Services'):
#         if(row['Installer'] != 'Unknown'):
#             test = folium.Html('<h5>'+row["Recipient"]+'</h5>'+'<p>('+row['Type']+')</p>'+'<b> Project Grant : $' +str(row['Value of grant'])+ '</b> <br>'+'<b> Array Size : '+str(row['Size of Array (in kW)'])+'</b> <br>'+'<b> Installer :'+row['Installer']+'</b>', script=True)
#             popup = folium.Popup(test, max_width=2650)
#             folium.Marker(location=[row["Latitude"], row["Longitude"]],popup=popup,icon=folium.Icon(color='green',icon='building', prefix='fa')).add_to(group_3)
#         else:
#             test = folium.Html('<h5>'+row["Recipient"]+'</h5>'+'<p>('+row['Type']+')</p>'+'<b> Project Grant : $' +str(row['Value of grant'])+ '</b> <br>'+'<b> Array Size : '+str(row['Size of Array (in kW)'])+'</b>', script=True)
#             popup = folium.Popup(test, max_width=2650)
#             folium.Marker(location=[row["Latitude"], row["Longitude"]],popup=popup,icon=folium.Icon(color='green',icon='building', prefix='fa')).add_to(group_3)
    
#     else:
#         if(row['Installer'] != 'Unknown'):
#             test = folium.Html('<h5>'+row["Recipient"]+'</h5>'+'<p>('+row['Type']+')</p>'+'<b> Project Grant : $' +str(row['Value of grant'])+ '</b> <br>'+'<b> Array Size : '+str(row['Size of Array (in kW)'])+'</b> <br>'+'<b> Installer :'+row['Installer']+'</b>', script=True)
#             popup = folium.Popup(test, max_width=2650)
#             folium.Marker(location=[row["Latitude"], row["Longitude"]],popup=popup,icon=folium.Icon(color='purple',icon='flag', prefix='fa')).add_to(group_4)
#         else:
#             test = folium.Html('<h5>'+row["Recipient"]+'</h5>'+'<p>('+row['Type']+')</p>'+'<b> Project Grant : $' +str(row['Value of grant'])+ '</b> <br>'+'<b> Array Size : '+str(row['Size of Array (in kW)'])+'</b>', script=True)
#             popup = folium.Popup(test, max_width=2650)
#             folium.Marker(location=[row["Latitude"], row["Longitude"]],popup=popup,icon=folium.Icon(color='purple',icon='flag', prefix='fa')).add_to(group_4)

# folium.LayerControl().add_to(usa)
# Geocoder().add_to(usa)
# usa.save('usa.html')

# # for idx, row in data.iterrows():
# #     folium.CircleMarker(location=[row["Latitude"], row["Longitude"]],radius=25,fill=True,popup=row["Place Name"]).add_to(usa)
# usa.save('usa.html')