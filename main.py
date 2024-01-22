import folium
import pandas

data = pandas.read_csv("VolcanoMap.txt")
lat = list(data["Latitude"])
lon = list(data["Longitude"])
elevation = list(data["Elevation"])
name = list(data["Name"])
country = list(data["Country"])
vol_type = list(data["Type"])

map = folium.Map(location=[38.58, -99.09],
                 zoom_start=5,
                 tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
                 attr='Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, '
                      'GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS '
                      'User Community',
                 world_copy_jump=True
                 )

# Add a single marker
# map.add_child(folium.Marker(location=[38.2, -99.1], popup="Hi I am a marker", icon=folium.Icon(color='green')))

# Creates  feature group.
fg = folium.FeatureGroup(name="My Map")
# iterate through two lists at once. Need to use zip function
for lt, ln, el, v_name, v_country, vol_t in zip(lat, lon, elevation, name, country, vol_type):
    fg.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(f"""<h3 style="font-size:16px;">{v_name}</h3>
                                                                    Country = {v_country} <br>
                                                                    Type = {vol_t} <br>
                                                                    Elevation = {el} m <br>
                                                                    <a href='https://www.google.com/search?q={v_name} +
                                                                    volcano' 
                                                                    target='_blank'>Learn More!</a>
                    """, max_width=len(f"name= {name}")*20), icon=folium.Icon(color='green')))
map.add_child(fg)

map.save("Map1.html")
