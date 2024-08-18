import folium.raster_layers
import streamlit as st
from streamlit_folium import folium_static, st_folium
import folium

st.title("Dashboard")

m = folium.Map(
    location=[51.922408, 4.4695292],
    # location=[41, -70],
    zoom_start=5,
    #    tiles="cartodb positron"
)

host_root = "http://localhost"
# host_root = "docker.for.mac.host.internal"

# folium.WmsTileLayer(
#     url="https://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi",
#     name="test",
#     fmt="image/png",
#     layers="nexrad-n0r-900913",
#     attr="Weather data © 2012 IEM Nexrad",
#     transparent=True,
#     overlay=True,
#     control=True,
# ).add_to(m)
# add localhost geoserver wms tile layer
folium.raster_layers.WmsTileLayer(
    # url="http://localhost:8080/geoserver/wms",
    url=f"{host_root}:8080/geoserver/wms",
    name="geoserver-test",
    fmt="image/png",
    layers=["ne:world", "ne:populated_places", "ne:disputed_areas"],
    attr="ne-geoserver",
    transparent=True,
    overlay=True,
    control=True,
    show=True,
).add_to(m)
folium.raster_layers.WmsTileLayer(
    # url="http://localhost:8080/geoserver/wms",
    url=f"{host_root}:8080/geoserver/wms",
    name="geoserver-test-tasmania",
    fmt="image/png",
    layers=["spearfish", "tasmania"],
    attr="tas-geoserver",
    transparent=True,
    overlay=True,
    control=True,
    show=True,
).add_to(m)

# folium.raster_layers.WmsTileLayer(
#     url="https://service.pdok.nl/wandelnet/regionale-wandelnetwerken/wms/v1_0",
#     layers=["wandelknooppunten", "wandelnetwerken"],
#     transparent=True,
#     control=True,
#     fmt="image/png",
#     name="Regionale Wandelnetwerken WMS",
#     overlay=True,
#     show=True,
#     version="1.3.0",
# ).add_to(m)

folium.LayerControl().add_to(m)
folium_static(m)
# st_folium(m)
