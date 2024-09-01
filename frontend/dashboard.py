import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import Fullscreen
from streamlit_js_eval import streamlit_js_eval
from utils import load_cables, load_meters
import pandas as pd

# configure the page
st.set_page_config(
    page_title="Dashboard",
    page_icon=":sparkles:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("Dashboard")

tab1, tab2 = st.tabs(["Geoserver", "Pygeoapi"])

host_root = "http://localhost"
# host_root = "docker.for.mac.host.internal"


def create_geoserver_map():
    """Create a map with the liander data.
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
    if "map" not in st.session_state or "current_data" not in st.session_state:
        m = folium.Map(location=[52.4326, 5.4913], zoom_start=8)
        folium.TileLayer("cartodbpositron", show=True).add_to(m)
        folium.TileLayer("cartodbdark_matter", show=False).add_to(m)
        layer_list = [
            "nl:nl_hs_cables",
            "nl:nl_ms_cables",
            "nl:nl_ls_cables",
            "nl:nl_meters",
        ]

        for layer in layer_list:
            if layer == "nl:nl_hs_cables":
                default_show_layer = True
            else:
                default_show_layer = False
            # default_show_layer = True
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


def create_pygeoapi_map(
    meter_data: pd.DataFrame,
    ls_data: pd.DataFrame,
    ms_data: pd.DataFrame,
    hs_data: pd.DataFrame,
):
    """Create a map with the liander data.
    Use the previous state where possible to stop whole app reloading
    when interacting with the map.

    Parameters
    ----------
    meter_data: pd.DataFrame
        The meters data.
    ls_data : pd.DataFrame
        The low-voltage cables data.
    ms_data : pd.DataFrame
        The medium-voltage cables data.
    hs_data : pd.DataFrame
        The high-voltage cables data.

    Returns
    -------
    folium.Map
        A folium map with the asset and sag data.

    """
    if (
        "map" not in st.session_state
        or "current_hs_data" not in st.session_state
        or st.session_state.current_hs_data.shape != hs_data.shape
    ):
        m = folium.Map(
            location=[
                hs_data["latitude"].mean(),
                hs_data["longitude"].mean(),
            ],
            zoom_start=8,
        )
        # m = folium.Map(location=[52.4326, 5.4913], zoom_start=8)
        folium.TileLayer("cartodbpositron", show=True).add_to(m)
        folium.TileLayer("cartodbdark_matter", show=False).add_to(m)
        for cable_type_name, cable_type_data in {
            "Low-voltage cables": ls_data,
            "Medium-voltage cables": ms_data,
            "High-voltage cables": hs_data,
        }.items():
            cable_type_group = folium.FeatureGroup(name=cable_type_name).add_to(m)
            for name, group in cable_type_data.groupby("id"):
                if cable_type_name == "Low-voltage cables":
                    line_color = "green"
                elif cable_type_name == "Medium-voltage cables":
                    line_color = "blue"
                else:
                    line_color = "red"
                folium.PolyLine(
                    locations=group[["latitude", "longitude"]].values.tolist(),
                    color=line_color,
                    tooltip=name,
                ).add_to(cable_type_group)
        meter_data_group = folium.FeatureGroup(name="Meters").add_to(m)
        for row in meter_data.to_dict(orient="records"):
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                # popup=f"Meter ID: {row['id']}<br> Address: {row['address']}<br> Info: {row['info']}",
                popup=folium.Popup(
                    f"Meter ID: {row['id']}<br> Address: {row['address']}<br> Info: {row['info']}",
                    max_width=300,
                ),
                icon=folium.Icon(color="green"),
            ).add_to(meter_data_group)
        Fullscreen().add_to(m)
        folium.LayerControl().add_to(m)

        st.session_state.map = m
        st.session_state.current_hs_data = hs_data

        return st.session_state.map


def specify_map_size():
    """Specify the size of the map.

    Parameters
    ----------
    None

    Returns
    -------
    None

    """
    screen_width = streamlit_js_eval(
        js_expressions="window.screen.width",
        want_output=True,
        key="screen_width",
    )
    screen_height = streamlit_js_eval(
        js_expressions="window.screen.height",
        want_output=True,
        key="screen_height",
    )

    if screen_width:
        map_screen_width = int(screen_width) - 200
    else:
        map_screen_width = 800
    if screen_height:
        map_screen_height = int(screen_height) - 200
    else:
        map_screen_height = 600

    return map_screen_width, map_screen_height


map_screen_width, map_screen_height = specify_map_size()

with tab1:
    st.subheader("Geoserver")
    m = create_geoserver_map()
    map_render = folium_static(m, height=map_screen_height, width=map_screen_width)

with tab2:
    st.subheader("Pygeoapi")
    limit_amount = st.slider(
        label="Limit Amount",
        min_value=100,
        max_value=10000,
        value=100,
        step=10,
    )
    meters_df = load_meters(limit=limit_amount)
    ls_cables_df = load_cables(cable_type="ls_cables", limit=limit_amount)
    ms_cables_df = load_cables(cable_type="ms_cables", limit=limit_amount)
    hs_cables_df = load_cables(cable_type="hs_cables", limit=limit_amount)
    m = create_pygeoapi_map(
        meter_data=meters_df,
        ls_data=ls_cables_df,
        ms_data=ms_cables_df,
        hs_data=hs_cables_df,
    )
    # st.dataframe(hs_cables_df)
    map_render = folium_static(m, height=map_screen_height, width=map_screen_width)
