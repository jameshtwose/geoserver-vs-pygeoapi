import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import Fullscreen
from streamlit_js_eval import streamlit_js_eval

# configure the page
st.set_page_config(
    page_title="Dashboard",
    page_icon=":sparkles:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("Dashboard")

host_root = "http://localhost"
# host_root = "docker.for.mac.host.internal"

screen_width = streamlit_js_eval(
    js_expressions="window.screen.width", want_output=True, key="screen_width"
)
screen_height = streamlit_js_eval(
    js_expressions="window.screen.height",
    want_output=True,
    key="screen_height",
)


def create_map():
    """Create a map with the outage data.
    Use the previous state where possible to stop whole app reloading
    when interacting with the map.

    Parameters
    ----------
    None

    Returns
    -------
    folium.Map
        A folium map with the asset and sag data.

    """
    if (
        "map" not in st.session_state
        or "current_data" not in st.session_state
    ):
        m = folium.Map(location=[52.4326, 5.4913], zoom_start=8)
        folium.TileLayer("cartodbpositron", show=True).add_to(m)
        folium.TileLayer("cartodbdark_matter", show=False).add_to(m)
        layer_list = [
            "nl:nl_meters",
            "nl:nl_hs_cables",
            "nl:nl_ms_cables",
            "nl:nl_ls_cables",
        ]

        for layer in layer_list:
            if layer == "nl:nl_hs_cables":
                default_show_layer = True
            else:
                default_show_layer = False
            folium.WmsTileLayer(
                url=f"{host_root}:8080/geoserver/wms",
                name=layer,
                fmt="image/png",
                layers=[layer],
                transparent=True,
                overlay=True,
                control=True,
                show=default_show_layer,
            ).add_to(m)

        Fullscreen().add_to(m)
        folium.LayerControl().add_to(m)

        st.session_state.map = m  # save the map in the session state
        return st.session_state.map


m = create_map()

if screen_width:
    map_screen_width = int(screen_width) - 200
else:
    map_screen_width = 800
if screen_height:
    map_screen_height = int(screen_height) - 200
else:
    map_screen_height = 600
map_render = folium_static(
    m, height=map_screen_height, width=map_screen_width
)
