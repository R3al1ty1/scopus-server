from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import asyncio

from parsing.parse import get_author_info, download_scopus_file, search_for_author_cred
from database.models import SAuth, SPub, SAuthInfo
from parsing.files import get_files_auth, get_files_pubs
from database.db import get_status, get_result_db


app = FastAPI()


@app.post("/pub/search")
async def start_pub_search(pub_req: SPub):
    try:
        asyncio.create_task(download_scopus_file(pub_req.filters_dct, pub_req.folder_id))
        return {"response": "200 OK"}
    except:
        return {"response": "404 NOT FOUND"}


@app.post("/auth/search")
async def start_auth_search(auth_req: SAuth):
    try:
        asyncio.create_task(search_for_author_cred(auth_req.filters_dct, auth_req.folder_id, auth_req.search_type))
        return {"response": "200 OK"}
    except:
        return {"response": "404 NOT FOUND"}


@app.post("/auth/search/specific")
async def search_for_author(auth_req: SAuthInfo):
    try:
        asyncio.create_task(get_author_info(auth_req.author_id, auth_req.folder_id))
        return {"response": "200 OK"}
    except:
        return {"response": "404 NOT FOUND"}


@app.get("/pub/get/files/{folder_id}")
async def get_pub_files(folder_id: str):
    ris_file = await get_pub_files(folder_id=folder_id)
    return {
        "ris_file": FileResponse(ris_file)
    }


@app.get("/auth/get/files/{folder_id}")
async def get_auth_files(folder_id: str):
    png_files, ris_files, csv_files = await get_auth_files(folder_id=folder_id)
    return {
        "files": {
            "png_files": [FileResponse(file) for file in png_files],
            "csv_file": FileResponse(csv_files),
            "ris_file": FileResponse(ris_files)
        }
    }


@app.get("/result/{folder_id}")
async def get_result(folder_id: str):
    result = get_result_db(folder_id=folder_id)
    return {"result": result}


@app.get("/status/{folder_id}/{status_number}")
async def get_operation_status(folder_id: str, status_number: str):
    status = get_status(folder_id=folder_id, status_number=status_number)
    return {"status": status}


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
