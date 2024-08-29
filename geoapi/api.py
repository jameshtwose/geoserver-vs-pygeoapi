from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from geojson_pydantic import Feature, Point, FeatureCollection, LineString
from db import engine, NlMeters, NlHsCables, NlMsCables, NlLsCables
from sqlalchemy import select
from geoalchemy2.shape import to_shape


app = FastAPI(
    title="GEO-API",
    version="0.0.1",
    description="The GeoAPI is a RESTful API that provides access geographical data.",
    contact={
        "name": "James Twose",
        "email": "contact@jamestwose.com",
    },
)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
def read_root():
    """Root endpoint.

    Parameters
    ----------
    None

    Returns:
    -------
    dict
        A dictionary containing a welcome message.

    """
    return {"Hello": "Welcome to the GEO API"}


@app.get("/meters", tags=["Meters"])
def get_meters(limit: int):
    """Get meters endpoint.

    Parameters
    ----------
    limit : int
        The number of meters to return.

    Returns:
    -------
    dict
        A dictionary containing a list of meters.

    """
    with engine.begin() as conn:
        query = select(NlMeters).limit(limit)
        meters = conn.execute(query).fetchall()
        if not meters:
            return HTTPException(status_code=404, detail="No meters found.")
        return FeatureCollection(
            type="FeatureCollection",
            features=[
                Feature(
                    type="Feature",
                    geometry=Point(
                        type="Point",
                        coordinates=(
                            to_shape(meter.shape).coords.xy[0][0],
                            to_shape(meter.shape).coords.xy[1][0],
                        ),
                    ),
                    properties={
                        "id": meter.id,
                        "timestamp": meter.timestamp,
                        "address": meter.address,
                        "info": meter.info,
                    },
                )
                for meter in meters
            ],
        )

@app.get("/ls_cables", tags=["Low Voltage Cables"])
def get_ls_cables(limit: int):
    """Get low voltage cables endpoint.

    Parameters
    ----------
    limit : int
        The number of low voltage cables to return.

    Returns:
    -------
    dict
        A dictionary containing a list of low voltage cables.

    """
    with engine.begin() as conn:
        query = select(NlLsCables).limit(limit)
        ls_cables = conn.execute(query).fetchall()
        if not ls_cables:
            return HTTPException(status_code=404, detail="No low voltage cables found.")
        return FeatureCollection(
            type="FeatureCollection",
            features=[
                Feature(
                    type="Feature",
                    geometry=LineString(
                        type="LineString",
                        coordinates=[
                            [x, y] for x, y in zip(*to_shape(cable.shape).coords.xy)
                        ],
                    ),
                    properties={"id": cable.id},
                )
                for cable in ls_cables
            ],
        )

@app.get("/ms_cables", tags=["Medium Voltage Cables"])
def get_ms_cables(limit: int):
    """Get medium voltage cables endpoint.

    Parameters
    ----------
    limit : int
        The number of medium voltage cables to return.

    Returns:
    -------
    dict
        A dictionary containing a list of medium voltage cables.

    """
    with engine.begin() as conn:
        query = select(NlMsCables).limit(limit)
        ms_cables = conn.execute(query).fetchall()
        if not ms_cables:
            return HTTPException(status_code=404, detail="No medium voltage cables found.")
        return FeatureCollection(
            type="FeatureCollection",
            features=[
                Feature(
                    type="Feature",
                    geometry=LineString(
                        type="LineString",
                        coordinates=[
                            [x, y] for x, y in zip(*to_shape(cable.shape).coords.xy)
                        ],
                    ),
                    properties={"id": cable.id},
                )
                for cable in ms_cables
            ],
        )
        
@app.get("/hs_cables", tags=["High Voltage Cables"])
def get_hs_cables(limit: int):
    """Get high voltage cables endpoint.

    Parameters
    ----------
    limit : int
        The number of high voltage cables to return.

    Returns:
    -------
    dict
        A dictionary containing a list of high voltage cables.

    """
    with engine.begin() as conn:
        query = select(NlHsCables).limit(limit)
        hs_cables = conn.execute(query).fetchall()
        if not hs_cables:
            return HTTPException(status_code=404, detail="No high voltage cables found.")
        return FeatureCollection(
            type="FeatureCollection",
            features=[
                Feature(
                    type="Feature",
                    geometry=LineString(
                        type="LineString",
                        coordinates=[
                            [x, y] for x, y in zip(*to_shape(cable.shape).coords.xy)
                        ],
                    ),
                    properties={"id": cable.id},
                )
                for cable in hs_cables
            ],
        )