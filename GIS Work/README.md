The first step of this project is to convert the site address provided by client into latitude and longitudes which could then be plotted onto the graphical map with ease. 

The python file (address-conversion.py) in this GIS folder includes a function convert_address_to_coords() that returns a dataframe containing the latitude and longitude coordinates of the site address.

This function uses the Geoapify api to do the conversion. This is an API request that also uses an API key provided in the python file to make the requests.

Additionally, this function also adds a column called "Incorrect Address Flag" that return TRUE for those site addresses that are incomplete (example: ones missing a ZIP code).