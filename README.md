# geoserver-vs-pygeoapi
Comparison of api vs tile server for rendering GIS data

## Useful commands
- `docker-compose up -d` to start the services
- to clear ports `lsof -i tcp:5432` and `kill -9 <PID>`
- `docker cp nyc_data.backup postgis:/var/lib/postgresql/data/nyc_data.backup` to copy the backup file to postgres container
- `docker cp nyc_data.backup pgadmin_container:/home/nyc_data.backup` to copy the backup file to pgadmin container
- `docker cp nyc_data.backup postgis:/home/nyc_data.backup`
- `docker exec -it postgis psql -U postgres` to access postgis
- `CREATE EXTENSION postgis;` to enable postgis extension
- `pg_restore -C -d postgres /var/lib/postgresql/data/nyc_data.backup;` to restore the database
- `pg_restore -C -d postgres /home/nyc_data.backup -U postgres` to restore the database
- `docker exec -it pgadmin_container sh` to access pgadmin
- `streamlit run frontend/dashboard.py` to run the streamlit dashboard
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