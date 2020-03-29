##########################
# Week 2: Data Wrangling #
##########################

# importing libraries
import requests # library to handle requests
import pandas as pd # library for data analysis
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation
import matplotlib.pyplot as plt

from geopy.geocoders import Nominatim # module to convert an address into latitidue and longitude values

# libraries for displaying images
from IPython.display import Image
from IPython.core.display import HTML

# transforming json file into a pandas dataframe library
from pandas.io.json import json_normalize

import folium # plotting library

# print('Folium installed')
# print('Libraries imported.')

######################################
# Foursquare Credentials and Version #
######################################
CLIENT_ID = 'QMGQSECG4KCJPOPJQKYUTDK5ETIN5AEAZXTB4A5JS2EUHT5C' # your Foursquare ID
CLIENT_SECRET = 'MP0PLFHFZKZWSIBTON3EDPKGORQA5UKWWSSVGZPB4RP30TQQ' # your Foursquare Secret
VERSION = '20180604'
LIMIT = 30
#print('Your credentials: ')
#print('CLIENT_ID: ' + CLIENT_ID)
#print('CLIENT_SECRET: ' + CLIENT_SECRET)

######################################
# Converting address to coordinates  #
######################################
address = '1003 Florida Ave NE, Washington, DC'
# address = '102 North End Ave, New York, NY'


geolocator = Nominatim(user_agent="foursquare_agent")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
#print(latitude, longitude)

############################################
# 1. Search for a specific venue category  #
############################################
#https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&ll=LATITUDE,LONGITUDE&v=VERSION&query=QUERY&radius=RADIUS&limit=LIMIT

# assuming lunch search, asian / ethiopian
search_query = 'Italian'
radius = 500
# print(search_query + ' .... OK!')

# Define the corresponding URL
url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query, radius, LIMIT)
# print(url)

# Send the GET request and examine the results
results = requests.get(url).json()
# print(results)

# Get relevant part of JSON and transfrom to pd df
# assign relevant part of JSON to venues
venues = results['response']['venues']

# transform venues into a dataframe
dataframe = json_normalize(venues)
print(dataframe.head())

# Define information of interests and filter
# keep only columns that include venue name, and locaton info
filtered_columns = ['name', 'categories'] + [col for col in dataframe.columns if col.startswith('location.')] + ['id']
dataframe_filtered = dataframe.loc[:, filtered_columns]

# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']

    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']

# filter the category for each row
dataframe_filtered['categories'] = dataframe_filtered.apply(get_category_type, axis=1)

# clean column names by keeping only last term
dataframe_filtered.columns = [column.split('.')[-1] for column in dataframe_filtered.columns]

# print(dataframe_filtered)

# visualizing italian restaurants nearby

dataframe_filtered.name

venues_map = folium.Map(location=[latitude, longitude], zoom_start=13) # generate map around home base

# add a red circle marker to represent home base
folium.CircleMarker(
    [latitude, longitude],
    radius=10,
    color='red',
    popup='Dhruv\'s House',
    fill = True,
    fill_color = 'red',
    fill_opacity = 0.6
).add_to(venues_map)

# add the Italian restaurants as blue circle markers
for lat, lng, label in zip(dataframe_filtered.lat, dataframe_filtered.lng, dataframe_filtered.categories):
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        color='blue',
        popup=label,
        fill = True,
        fill_color='blue',
        fill_opacity=0.6
    ).add_to(venues_map)


venues_map.save('venues_map.html')

#############################
# 2. Explore a Given Venue  #
#############################
# https://api.foursquare.com/v2/venues/VENUE_ID?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=VERSION

# exploring nearby italian rita's frozen yogurt and ice cream shop
venue_id = '4c27e695ed0ac9b6d9805faa'
url = 'https://api.foursquare.com/v2/venues/{}?client_id={}&client_secret={}&v={}'.format(venue_id, CLIENT_ID, CLIENT_SECRET, VERSION)
print(url)




























# in order to display plot within window
# plt.show()
