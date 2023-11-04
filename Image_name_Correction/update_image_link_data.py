#%%
import numpy as np
import pandas as pd
#%%
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

data = pd.read_csv("data.csv")
data = rename_image_urls(data)

# %%
# save the new dataframe with corrected address onto the the same csv file
data.to_csv("data.csv")
# %%
# google drive image link updates
import os

# Replace with the path to your local directory
local_directory = 'Project_Pictures'

def rename_files_with_spaces(directory):
    """
    Function that reads a folder from a directory path and then corrects the image file name in such a way that replaces all the space in the file name with an underscore
    Function renames the file itself
    Example: P076-Covenant Lutheran Church arial.jpg
    is renamed as - P076-Covenant_Lutheran_Church_arial.jpg 
    """
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)) and ' ' in filename:
            new_name = filename.replace(' ', '_')
            new_path = os.path.join(directory, new_name)
            os.rename(os.path.join(directory, filename), new_path)
            print(f'Renamed {filename} to {new_name}')

rename_files_with_spaces(local_directory)
# %%
