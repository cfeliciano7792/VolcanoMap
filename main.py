import folium
import pandas

data = pandas.read_csv("VolcanoMap.txt")
lat = list(data["Latitude"])
lon = list(data["Longitude"])
elevation = list(data["Elevation"])
name = list(data["Name"])
country = list(data["Country"])
vol_type = list(data["Type"])

def color_producer(elevation_val):
    if elevation_val < 1000:
        return "green"
    elif 1000 <= elevation_val < 3000:
        return "orange"
    else:
        return "red"

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

fgp = folium.FeatureGroup(name="Population")
fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
                            style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
                            else 'orange' if 10000000 <= x['properties']['POP2005'] < 50000000
                            else "red"}))



# Creates  feature group.
fgv = folium.FeatureGroup(name="Volcanoes")
# iterate through two lists at once. Need to use zip function
for lt, ln, el, v_name, v_country, vol_t in zip(lat, lon, elevation, name, country, vol_type):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius = 6, popup=folium.Popup(f"""<h3 style="font-size:16px;">{v_name}</h3>
                                                                    Country = {v_country} <br>
                                                                    Type = {vol_t} <br>
                                                                    Elevation = {el} m <br>
                                                                    <a href='https://www.google.com/search?q={v_name} +
                                                                    volcano' 
                                                                    target='_blank'>Learn More!</a>
                    """, max_width=len(f"name= {name}")*20), fill_color = color_producer(el), color = 'grey', fill_opacity = 0.7))


map.add_child(fgp)
map.add_child(fgv)


# Adds layer control functionality
map.add_child(folium.LayerControl())

map.save("Map1.html")
