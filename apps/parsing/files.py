import os
import asyncio
import shutil
import zipfile
from concurrent.futures import ThreadPoolExecutor
from parsing.unzipper import unzip_pngs


async def get_files_auth(folder_id: str):
    files_path = "scopus_files/" + folder_id
    current_dir = os.path.dirname(os.path.abspath(__file__))
    full_folder_path = os.path.join(current_dir, files_path)

    pngs = await unzip_pngs(full_folder_path)
    await asyncio.sleep(2)
    if pngs:
        png_files = [os.path.join(full_folder_path, f) for f in os.listdir(full_folder_path) if f.endswith(".png")]
        ris_files = [os.path.join(full_folder_path, f) for f in os.listdir(full_folder_path) if f.endswith(".ris")]
        csv_files = [os.path.join(full_folder_path, f) for f in os.listdir(full_folder_path) if f.endswith(".csv")]

    return png_files, ris_files, csv_files

async def get_files_pubs(folder_id: str):
    project_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = f"{project_dir}/scopus_files/{folder_id}"
    file_path = f"{folder_path}/scopus.ris"
    
    return file_path


async def pack_files_to_archive(folder_id, archive_name):
    files_path = "scopus_files/" + str(folder_id)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, files_path)

    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        return

    zip_filename = os.path.join(folder_path, f"{archive_name}.zip")
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.islink(file_path):
                    continue

                if file.startswith('.'):
                    continue

                _, ext = os.path.splitext(file)
                if ext.lower() not in ['.png', '.csv', '.ris']:
                    continue
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

    return zip_filename
