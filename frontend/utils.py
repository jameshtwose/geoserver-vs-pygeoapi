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
        The type of data to get (e.g., "hs_cables").
    limit : int
        The number of items to get.

    Returns
    -------
    requests.models.Response
        The cable data.

    """
    url = f"http://localhost:8090/{data_type}?limit={limit}"
    return requests.get(url)


@st.cache_data(ttl=600)
def load_cables(cable_type="hs_cables", limit: int = 100) -> pd.DataFrame:
    """Load the high-voltage cables data.

    Parameters
    ----------
    cable_type: str
        The type of cable to load.
    limit : int
        The number of items to get.

    Returns
    -------
    pd.DataFrame
        The cable data.

    """
    response = get_cable_data(data_type=cable_type, limit=limit)
    data = response.json()
    df = (
        pd.json_normalize(data["features"])
        .explode("geometry.coordinates")
        .assign(
            **{
                "latitude": lambda x: x["geometry.coordinates"].apply(lambda y: y[1]),
                "longitude": lambda x: x["geometry.coordinates"].apply(lambda y: y[0]),
            }
        )
    ).rename(columns={"properties.id": "id"})
    df["latitude"], df["longitude"] = transformer.transform(
        df["longitude"], df["latitude"]
    )
    return df


@st.cache_data(ttl=600)
def load_meters(limit: int = 100) -> pd.DataFrame:
    """Load the meters data.

    Parameters
    ----------
    limit : int
        The number of items to get.

    Returns
    -------
    pd.DataFrame
        The meters data.

    """
    response = get_cable_data(data_type="meters", limit=limit)
    data = response.json()
    df = (
        pd.json_normalize(data["features"])
        .assign(
            **{
                "latitude": lambda x: x["geometry.coordinates"].apply(lambda y: y[1]),
                "longitude": lambda x: x["geometry.coordinates"].apply(lambda y: y[0]),
            }
        )
        .rename(
            columns={
                "properties.id": "id",
                "properties.address": "address",
                "properties.info": "info",
            }
        )
    )
    df["latitude"], df["longitude"] = transformer.transform(
        df["longitude"], df["latitude"]
    )
    return df
