import asyncio
import zipfile

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from parsing.parse import get_author_info, download_scopus_file, search_for_author_cred
from database.models import SAuth, SPub, SAuthInfo
from parsing.files import get_files_auth, get_files_pubs, pack_files_to_archive
from database.db import get_status, get_result_db
from io import BytesIO



app = FastAPI()


@app.post("/pub/search", status_code=status.HTTP_200_OK)
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
    ris_file = await get_files_pubs(folder_id=folder_id)
    
    return FileResponse(ris_file)


@app.get("/auth/get/files/{folder_id}")
async def get_auth_files(folder_id: str):
    png_files, ris_files, csv_files = await get_files_auth(folder_id)

    all_files = png_files + ris_files + csv_files

    if not all_files:
        raise HTTPException(status_code=404, detail="No files found in the specified folder")

    zip_arc_path = await pack_files_to_archive(folder_id, "files_archive")

    if zip_arc_path:
        return FileResponse(zip_arc_path)
    else:
        return {"message": "false"}


@app.get("/result/{folder_id}")
async def get_result(folder_id: str):
    result = get_result_db(folder_id=folder_id)
    return {"result": result}


@app.get("/status/{folder_id}/{status_number}")
async def get_operation_status(folder_id: str, status_number: str):
    status = get_status(folder_id=folder_id, status_number=status_number)
    return {"status": status}


@app.get("/ping")
def read_root():
    return {"message": "pong"}


@app.get("/file")
async def get_a_file():
    path = "/Users/user/scopus-server/apps/parsing/scopus_files/dd23a8a5-d7ca-4036-9f35-bdddd2008dd9/arc.zip"
    return FileResponse(path)
