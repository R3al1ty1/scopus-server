import os
import asyncio
from parsing.unzipper import unzip_pngs


async def get_files_auth(folder_id: str):
    files_path = "scopus_files/" + folder_id
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    full_folder_path = os.path.join(parent_dir, files_path)

    pngs = await unzip_pngs(full_folder_path)  # Если требуется распаковка PNG файлов
    await asyncio.sleep(2)
    if pngs:
        png_files = [os.path.join(full_folder_path, f) for f in os.listdir(full_folder_path) if f.endswith(".png")]
        ris_files = [os.path.join(full_folder_path, f) for f in os.listdir(full_folder_path) if f.endswith(".ris")]
        csv_files = [os.path.join(full_folder_path, f) for f in os.listdir(full_folder_path) if f.endswith(".csv")]
    
    return png_files, ris_files, csv_files

async def get_files_pubs(folder_id: str):
    project_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir_pub = os.path.dirname(project_dir)
    folder_path = f"{project_dir_pub}/scopus_files/{folder_id}"
    file_path = f"{folder_path}/scopus.ris"
    
    return file_path
