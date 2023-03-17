from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from artifact_hub import s3_hub
from artifact_hub.backends.base_backend import BaseBackend

app = FastAPI()

app.mount("/static", StaticFiles(directory="artifact_hub/static"), name="static")

templates = Jinja2Templates(directory="artifact_hub/templates")


async def get_hub():
    return s3_hub("iamr0b0tx-development", "folder", "object_4954fd")


@app.get("/{repo_id}/{version_id}", response_class=HTMLResponse)
async def read_item(request: Request, repo_id: str, version_id: str, hub: BaseBackend = Depends(get_hub)):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "repo_id": repo_id,
            "version_id": version_id,
            "objects": hub.browse()
        }
    )
