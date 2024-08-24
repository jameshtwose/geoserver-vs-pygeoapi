import pygeoapi
from pygeoapi.util import yaml_load
import yaml
import os
from dotenv import load_dotenv, find_dotenv
from subprocess import call

_ = load_dotenv(find_dotenv())


def run_api():
    with open("pygeoapi-config-pre-update.yaml") as f:
        config = yaml_load(f)

    config["server"]["url"] = "http://localhost:5001"
    config["server"]["bind"]["port"] = 5001
    config["resources"]["nl_hs_cables"]["providers"][0]["data"]["host"] = (
        os.getenv("POSTGRES_HOST")
    )
    config["resources"]["nl_hs_cables"]["providers"][0]["data"]["dbname"] = (
        os.getenv("POSTGRES_DB")
    )
    config["resources"]["nl_hs_cables"]["providers"][0]["data"]["user"] = (
        os.getenv("POSTGRES_USER")
    )
    config["resources"]["nl_hs_cables"]["providers"][0]["data"][
        "password"
    ] = os.getenv("POSTGRES_PASSWORD")
    config["resources"]["nl_hs_cables"]["providers"][0]["data"]["port"] = (
        os.getenv("POSTGRES_PORT")
    )
    config["resources"]["nl_hs_cables"]["providers"][0]["data"][
        "table"
    ] = "nl_hs_cables"
    pygeoapi.api.SwaggerUI = True
    pygeoapi.api.config = config
    with open("pygeoapi-config.yaml", "w") as f:
        f.write(yaml.dump(config))
    os.system(
        "pygeoapi openapi generate pygeoapi-config.yaml --output-file openapi-config.yaml"
    )
    pygeoapi.serve()


if __name__ == "__main__":
    run_api()
