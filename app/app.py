from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse

import service

app = FastAPI(docs_url=None, redoc_url=None)


@app.post("/rewrite")
def rewrite(r: service.Req, request: Request, response: Response):
    response.headers["Cache-Control"] = "no-store"
    try:
        # behind a reverse proxy this is the proxy's address; forward the real client IP if rate limits matter
        return service.run(r, request.client.host if request.client else "?")
    except service.ApiError as e:
        raise HTTPException(e.status, e.msg)


@app.get("/config")
def config():
    return service.config()


@app.get("/")
def index():
    return FileResponse(Path(__file__).parent / "index.html")
