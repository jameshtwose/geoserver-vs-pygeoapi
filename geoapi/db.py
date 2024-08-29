from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

host = "localhost"
host = "docker.for.mac.localhost"
host = "docker.for.mac.host.internal"

engine = create_engine(
    f"postgresql+psycopg2://postgres:postgres@{host}:5434/postgres"
)

Base = declarative_base()


class NlMeters(Base):
    __tablename__ = "nl_meters"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    address = Column(String)
    info = Column(String)
    shape = Column(Geometry("POINT", srid=28992))


class NlHsCables(Base):
    __tablename__ = "nl_hs_cables"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    shape = Column(Geometry("LINESTRING", srid=28992))


class NlMsCables(Base):
    __tablename__ = "nl_ms_cables"
    __table_args__ = {"schema": "public"}
    id = Column(Integer, primary_key=True)
    shape = Column(Geometry("LINESTRING", srid=28992))


class NlLsCables(Base):
    __tablename__ = "nl_ls_cables"
    __table_args__ = {"schema": "public"}
    id = Column(Integer, primary_key=True)
    shape = Column(Geometry("LINESTRING", srid=28992))


Base.metadata.create_all(engine)