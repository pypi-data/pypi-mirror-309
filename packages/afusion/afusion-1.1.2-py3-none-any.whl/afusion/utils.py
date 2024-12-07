import os
import zipfile
import io
from loguru import logger

def compress_output_folder(output_folder_path, job_output_folder_name):
    # Create a ZIP file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=output_folder_path)
                zipf.write(file_path, arcname)
    zip_buffer.seek(0)
    logger.debug(f"Compressed output folder: {output_folder_path}")
    return zip_buffer.getvalue()
