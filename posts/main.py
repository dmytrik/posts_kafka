from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="posts"
)

api_version_prefix = "/api/v1"

app.include_router(router, prefix=f"{api_version_prefix}/posts", tags=["posts"])
