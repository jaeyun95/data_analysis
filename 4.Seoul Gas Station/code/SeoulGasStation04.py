import json
import folium
import googlemaps
import pandas as pd
import numpy as np

stations = pd.read_csv("C:/Users/jaeyun/Desktop/github/data_analysis/4.Seoul Gas Station/data/station.csv",index_col=0)

gu_data = pd.pivot_table(stations, index="Location",values=["Price"],aggfunc=np.mean)

## draw map
'''
geo_path = "C:/Users/jaeyun/Desktop/github/data_analysis/4.Seoul Gas Station/data/skorea_municipalities_geo_simple.json"
geo_str = json.load(open(geo_path, encoding="utf-8"))

map = folium.Map(location=[37.5502,126.982],zoom_start=10.5,titles="Stamen Toner")
map.choropleth(geo_data=geo_str, data=gu_data["Price"],
             columns=[gu_data.index, gu_data["Price"]],
             key_on='feature.id',
             fill_color='PuRd')

map.save("C:/Users/jaeyun/Desktop/github/data_analysis/4.Seoul Gas Station/data/seoul_map1.html")
'''

## top 10 / buttom 10
oil_price_top10 = stations.sort_values(by="Price",ascending=False).head(10)
oil_price_bottom10 = stations.sort_values(by="Price",ascending=True).head(10)

gmap_key = "*************************"
gmaps = googlemaps.Client(key=gmap_key)

lat = []
lng = []

for n in oil_price_top10.index:
    address = str(oil_price_top10["Address"][n]).split('(')[0]
    tmp_map = gmaps.geocode(address)
    tmp_loc = tmp_map[0].get('geometry')
    lat.append(tmp_loc['location']['lat'])
    lng.append(tmp_loc['location']['lng'])

oil_price_top10['lat'] = lat
oil_price_top10['lng'] = lng

lat = []
lng = []

for n in oil_price_bottom10.index:
    address = str(oil_price_bottom10["Address"][n]).split('(')[0]
    tmp_map = gmaps.geocode(address)
    tmp_loc = tmp_map[0].get('geometry')
    lat.append(tmp_loc['location']['lat'])
    lng.append(tmp_loc['location']['lng'])

oil_price_bottom10['lat'] = lat
oil_price_bottom10['lng'] = lng

geo_path = "C:/Users/jaeyun/Desktop/github/data_analysis/4.Seoul Gas Station/data/skorea_municipalities_geo_simple.json"
geo_str = json.load(open(geo_path, encoding="utf-8"))

map = folium.Map(location=[37.5502,126.982],zoom_start=10.5,titles="Stamen Toner")

for lat,lng in zip(oil_price_top10["lat"],oil_price_top10["lng"]):
    folium.CircleMarker([lat, lng],
                        radius=15, color="#CD3181",
                        fill_color="#CD3181").add_to(map)
for lat,lng in zip(oil_price_bottom10["lat"],oil_price_bottom10["lng"]):
    folium.CircleMarker([lat, lng],
                        radius=15, color="#3186cc",
                        fill_color="#3186cc").add_to(map)
map.save("C:/Users/jaeyun/Desktop/github/data_analysis/4.Seoul Gas Station/data/seoul_map2.html")
