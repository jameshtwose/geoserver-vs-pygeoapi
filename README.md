# geoserver-vs-pygeoapi
Comparison of api vs tile server for rendering GIS data

## Useful commands (run on mac)
- `brew install docker` to install docker
- `brew install docker-compose` to install docker-compose
- `brew install postgresql@16` to install postgresql
- `brew install libpq` to install libpq
- `docker-compose up -d` to start the services
- to clear ports `lsof -i tcp:5432` and `kill -9 <PID>` to kill the process (Optional)
- `streamlit run frontend/dashboard.py` to run the streamlit dashboard
- `python geoapi/main.py` to run the pygeoapi server
- `docker build -t geoapi .` to build the geoapi image
- `docker run -p 8081:8080 geoapi` to run the geoapi container

## Pgadmin connection settings
- host: docker.for.mac.host.internal
- port: 5434
- user: postgres
- password: postgres
- database: postgres
- schema: public

## Cable data
- https://service.pdok.nl/liander/elektriciteitsnetten/atom/downloads/liander_elektriciteitsnetten.gpkg