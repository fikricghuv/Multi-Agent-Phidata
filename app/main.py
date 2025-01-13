from fastapi import FastAPI
from app.routes.api_routes import router
from app.config.settings import load_environment_variables

app = FastAPI()

env_vars = load_environment_variables()

app.include_router(router, prefix="/multi-agent")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app:app", host="127.0.0.1", port=8003, reload=True)