from datetime import datetime
import json
import os
import io
import discord
from dotenv import load_dotenv
from quart import Response, send_file

from src.services.encryption_service import get_encryptor
from src import _connect_db
from src.discord_client import get_client
from src.models.files.file_model import File, FileChunk
from src.services.logging_service import logger

# Initialize Discord client
client = get_client()

# Establish a database connection
db = _connect_db()

# Load environment variables
load_dotenv()
DISCORD_DATA_CHANNEL_ID = int(os.getenv("DISCORD_DATA_CHANNEL_ID"))
CHUNK_SIZE = 17 * 1024 * 1024  # 17MB chunk size

async def upload_file_chunk(chunk_io, chunk_name):
    """
    Uploads a file chunk to a Discord channel.

    Args:
        chunk_io (io.BytesIO): The file chunk to upload.
        chunk_name (str): The name of the file chunk.

    Returns:
        str: The ID of the sent message containing the file chunk.
    """
    channel = client.get_channel(DISCORD_DATA_CHANNEL_ID)
    file = discord.File(chunk_io, filename=chunk_name)
    sent_message = await channel.send(file=file)
    return sent_message.id

def read_file_chunks(file_id):
    """
    Reads file chunks metadata from the database.

    Args:
        file_id (str): The ID of the file.

    Returns:
        list: A list of file chunk metadata.
    """
    file_chunks = []

    cursor = db.execute("SELECT id, file_id, chunk_number, chunk_size FROM file_chunk WHERE file_id = ? ORDER BY chunk_number", (str(file_id),))
    rows = cursor.fetchall()
    for row in rows:
        chunk = {
            'id': row['id'],
            'file_id': row['file_id'],
            'chunk_number': row['chunk_number'],
            'chunk_size': row['chunk_size'],
        }
        file_chunks.append(chunk)

    return file_chunks

async def retrieve_discord_messages(file_chunks):
    """
    Retrieves Discord messages containing the file chunks.

    Args:
        file_chunks (list): A list of file chunk metadata.

    Returns:
        list: A list of byte arrays containing the file chunk data.
    """
    discord_messages = []
    for item in file_chunks:
        message = await client.get_channel(DISCORD_DATA_CHANNEL_ID).fetch_message(item['id'])
        content = await message.attachments[0].read()
        discord_messages.append(content)

    return discord_messages

async def delete_discord_messages(file_chunks):
    for item in file_chunks:
        message = await client.get_channel(DISCORD_DATA_CHANNEL_ID).fetch_message(item['id'])
        await message.delete()

def join_chunks(file_chunks):
    """
    Joins file chunks into a single byte array.

    Args:
        file_chunks (list): A list of byte arrays representing the file chunks.

    Returns:
        bytes: The concatenated byte array of the complete file.
    """
    file_content = b''.join(file_chunks)
    return file_content

async def upload_file(request):
    """
    Handles the file upload process by splitting the file into chunks and uploading them to Discord.

    Args:
        request (quart.Request): The HTTP request containing the file data.

    Returns:
        quart.Response: The response indicating the success or failure of the upload process.
    """
    try:
        logger.info("Upload request received")
        file_data = await request.files
        if "file" not in file_data:
            logger.error("No file part in the request")
            return Response(
                response=json.dumps({'status': "failed", "message": "File parameter 'file' is required"}),
                status=400,
                mimetype='application/json'
            )

        file_obj = file_data["file"]
        file_name = file_obj.filename
        logger.info(f"File name received: {file_name}")

        if File.file_exists(file_name=file_name, db=db):
            logger.error("File already exists")
            return Response(
                response=json.dumps({'status': "failed", "message": "File already exists"}),
                status=400,
                mimetype='application/json'
            )

        extension = os.path.splitext(file_name)[1][1:]
        logger.info(f"File extension received: {extension}")
        file_size = request.content_length
        logger.info(f"File size received: {file_size}")

        new_file = File(name=file_name, file_type=extension, total_size=file_size, date=datetime.now().isoformat())

        # Encrypt and upload file chunks
        fernet = get_encryptor()
        chunk_number = 0
        while True:
            chunk_data = file_obj.read(CHUNK_SIZE)
            if not chunk_data:
                break

            # Encrypt Chunk
            logger.info(f"Encrypting chunk number: {chunk_number + 1}")
            encrypted_chunk_data = fernet.encrypt(chunk_data)
            chunk_io = io.BytesIO(encrypted_chunk_data)
            chunk_number += 1
            chunk_filename = f"{new_file.id}_chunk_{chunk_number}"

            # Upload Chunk
            chunk_id = await upload_file_chunk(chunk_io, chunk_filename)

            new_chunk = FileChunk(file_id=new_file.id, chunk_number=chunk_number, chunk_size=len(encrypted_chunk_data), chunk_id=chunk_id)
            new_file.add_chunk(new_chunk)

        new_file.save_to_db(db=db)
        db.commit()  # Commit changes to the database

        logger.info("File upload successful")
        return Response(
            response=json.dumps({'status': "success", "message": "File upload successful"}),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            response=json.dumps({'status': "failed", "message": "Error occurred", "error": str(e)}),
            status=500,
            mimetype='application/json'
        )


async def download_file(file_id):
    """
    Handles the file download process by retrieving and joining file chunks from Discord.

    Args:
        file_id (str): The ID of the file to download.

    Returns:
        quart.Response: The response containing the downloaded file.
    """
    try:
        logger.info("Download request received")
        file_chunks = read_file_chunks(file_id)
        if not file_chunks:
            return Response(
                response=json.dumps({'status': "failed", "message": "File not found"}),
                status=404,
                mimetype='application/json'
            )
        logger.info("Retrieving Discord Messages")
        discord_messages = await retrieve_discord_messages(file_chunks)
        discord_messages_decrypted = []
        #Decrypt
        fernet = get_encryptor()
        chunk_number = 0
        for chunk_io in discord_messages:
            logger.info(f"Decrypting chunk number: {chunk_number + 1}")
            chunk_io = fernet.decrypt(chunk_io)
            discord_messages_decrypted.append(chunk_io)
            chunk_number += 1
        file_content = join_chunks(discord_messages_decrypted)

        file_var = File.load_from_db(file_id=file_id, db=db)
        file_name = f"{file_var.name}"
        # Create a response with the file content
        logger.info("Sending File")
        return Response(
            response=file_content,
            status=200,
            content_type='application/octet-stream',
            headers={
                'Content-Disposition': f'attachment; filename="{file_name}"'
            }
        )

    except Exception as e:
        return Response(
            response=json.dumps({'status': "failed", "message": "Error occurred", "error": str(e)}),
            status=500,
            mimetype='application/json'
        )

async def delete_file(file_id):
    try:
        # Get all chunks of file
        file_chunks = read_file_chunks(file_id)
        if not file_chunks:
            return Response(
                response=json.dumps({'status': "failed", "message": "File not found"}),
                status=404,
                mimetype='application/json'
            )
        # Delete all file chunks from Discord
        await delete_discord_messages(file_chunks)
        
        # Delete file from DB
        File.delete_from_db(file_id,db)
        db.commit()
        
        return Response(
            response=json.dumps({'status': "success", "message": "File deleted successful"}),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            response=json.dumps({'status': "failed", "message": "Error occurred", "error": str(e)}),
            status=500,
            mimetype='application/json'
        )
        
        
async def list_files():
    try:
        # Get all files
        files = File.list_all_files(db)
        
        # Convert list of File objects to list of dictionaries
        files_dict = [file.to_dict() for file in files]

        return Response(
            response=json.dumps(files_dict),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            response=json.dumps({'status': "failed", "message": "Error occurred", "error": str(e)}),
            status=500,
            mimetype='application/json'
        )