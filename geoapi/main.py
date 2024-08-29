from api import app
import uvicorn

def run_api():
    uvicorn.run(app, port=8090)

if __name__ == "__main__":
    run_api()
