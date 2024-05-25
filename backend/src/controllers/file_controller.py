from quart import Blueprint, request

from src.services.file_service import list_files, upload_file, download_file, delete_file

file_bp = Blueprint('file_bp', __name__)

# Route to upload the file
@file_bp.route('/upload', methods=['POST'])
async def upload():
    return await upload_file(request=request)
        
# Route to download the file
@file_bp.route('/download',methods=['GET'])
async def download():
    file_id = request.args.get('id')
    return await download_file(file_id=file_id)

# Route to delete the file
@file_bp.route('/delete', methods=['DELETE'])
async def delete():
    file_id = request.args.get('id')
    return await delete_file(file_id=file_id)

# Route to get all file
@file_bp.route('/files', methods=['GET'])
async def get_files():
    return await list_files()
