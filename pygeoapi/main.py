import pygeoapi
from pygeoapi.util import yaml_load
import yaml
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

def run_api():
    with open("pygeoapi-config-pre-update.yaml") as f:
        config = yaml_load(f)
    
    config["server"]["url"] = "http://localhost:5001"
    config["server"]["bind"]["port"] = 5001
    # config["resources"]["homicides"]["providers"][0]["data"]["host"] = os.environ.get(
    #     "POSTGRES_HOST"
    # )
    # config["resources"]["homicides"]["providers"][0]["data"]["dbname"] = os.environ.get(
    #     "POSTGRES_DB"
    # )
    # config["resources"]["homicides"]["providers"][0]["data"]["user"] = os.environ.get(
    #     "POSTGRES_USER"
    # )
    # config["resources"]["homicides"]["providers"][0]["data"]["password"] = os.environ.get(
    #     "POSTGRES_PASSWORD"
    # )
    # config["resources"]["homicides"]["providers"][0]["data"]["port"] = os.environ.get(
    #     "POSTGRES_PORT"
    # )
    # config["resources"]["homicides"]["providers"][0]["data"]["owner"] = os.environ.get(
    #     "POSTGRES_OWNER"
    # )
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
