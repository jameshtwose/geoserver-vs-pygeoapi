import streamlit as st
import requests
import pandas as pd
from pyproj import Transformer

# RD new to WGS84
transformer = Transformer.from_crs("epsg:28992", "epsg:4326")


def get_cable_data(
    data_type: str = "nl_hs_cables",
    limit: int = 100,
) -> requests.models.Response:
    """Get the cable data.

    Parameters
    ----------
    data_type : str
        The type of data to get (e.g., "nl_hs_cables").
    limit : int
        The number of items to get.

    Returns
    -------
    requests.models.Response
        The cable data.

    """
    url = f"http://localhost:5001/collections/{data_type}/items?f=json&limit={limit}"
    return requests.get(url)


@st.cache_data(ttl=600)
def load_hs_cables(limit: int = 100) -> pd.DataFrame:
    """Load the high-voltage cables data.

    Parameters
    ----------
    limit : int
        The number of items to get.

    Returns
    -------
    pd.DataFrame
        The high-voltage cables data.

    """
    response = get_cable_data(data_type="nl_hs_cables", limit=limit)
    data = response.json()
    df = (
        pd.json_normalize(data["features"])
        .explode("geometry.coordinates")
        .assign(
            **{
                "latitude": lambda x: x["geometry.coordinates"].apply(
                    lambda y: y[1]
                ),
                "longitude": lambda x: x["geometry.coordinates"].apply(
                    lambda y: y[0]
                ),
            }
        )
    )
    df["latitude"], df["longitude"] = transformer.transform(
        df["latitude"], df["longitude"]
    )
    # df["geometry.coordinates"] = str(transformer.transform(
    #     df["geometry.coordinates"].str[1], df["geometry.coordinates"].str[0]
    # ))
    return df
