import os
import json
import uuid
from datetime import datetime

class File:
    def __init__(self, name, file_type, total_size, date):
        """
        Initialize a new File object.

        Args:
            name (str): The name of the file.
            file_type (str): The type of the file.
            total_size (int): The total size of the file.
        """
        self.id = str(uuid.uuid4())  # Generating a unique UUID for the file id
        self.name = name
        self.file_type = file_type
        self.total_size = total_size
        self.date = date  # Setting the current timestamp as the creation date
        self.chunks = []  # Initialize an empty list to hold file chunks

    def add_chunk(self, chunk):
        """
        Add a file chunk to the file.

        Args:
            chunk (FileChunk): The chunk to be added to the file.
        """
        self.chunks.append(chunk)

    def save_to_db(self, db):
        """
        Save the file and its chunks to the database.

        Args:
            db (sqlite3.Connection): The database connection.
        """
        # Insert file metadata into the 'file' table
        db.execute(
            "INSERT INTO file (id, name, file_type, total_size, date) VALUES (?, ?, ?, ?, ?)",
            (self.id, self.name, self.file_type, self.total_size, self.date)
        )
        # Save each chunk associated with the file
        for chunk in self.chunks:
            chunk.save_to_db(db)

    @staticmethod
    def load_from_db(file_id, db):
        """
        Load a file and its chunks from the database.

        Args:
            file_id (str): The ID of the file to be loaded.
            db (sqlite3.Connection): The database connection.

        Returns:
            File: The loaded File object, or None if the file is not found.
        """
        # Retrieve file metadata from the 'file' table
        file_data = db.execute("SELECT id, name, file_type, total_size, date FROM file WHERE id = ?", (str(file_id),)).fetchone()
        if not file_data:
            return None  # Return None if the file is not found

        # Create a new File object with the retrieved data
        file = File(file_data[1], file_data[2], file_data[3], file_data[4])
        file.id = file_data[0]

        # Retrieve all chunks associated with the file from the 'file_chunk' table
        chunks = db.execute("SELECT id, file_id, chunk_number, chunk_size FROM file_chunk WHERE file_id = ?", (file.id,)).fetchall()
        for chunk_data in chunks:
            # Create a FileChunk object for each retrieved chunk and add it to the file
            chunk = FileChunk(chunk_data[1], chunk_data[2], chunk_data[3],chunk_data[0])
            file.add_chunk(chunk)
        return file
    
    @staticmethod
    def list_all_files(db):
        """
        Retrieve the name and ID of all files from the database.

        Args:
            db (sqlite3.Connection): The database connection.

        Returns:
            list: A list of File objects containing the name and ID of the files, or an empty list if no files are found.
        """
        # Retrieve file metadata from the 'file' table
        file_data = db.execute("SELECT id, name, file_type, total_size, date FROM file").fetchall()
        
        # Return an empty list if no files are found
        if not file_data:
            return []

        # Create a list to hold File objects
        files = []

        # Create a new File object for each retrieved row and append it to the list
        for data in file_data:
            file = File(data['name'], data['file_type'], data['total_size'], data['date'])
            file.id = data['id']
            # Retrieve all chunks associated with the file from the 'file_chunk' table
            chunks = db.execute("SELECT id, file_id, chunk_number, chunk_size FROM file_chunk WHERE file_id = ?", (file.id,)).fetchall()
            for chunk_data in chunks:
                # Create a FileChunk object for each retrieved chunk and add it to the file
                chunk = FileChunk(chunk_data[1], chunk_data[2], chunk_data[3], chunk_data[0])
                file.add_chunk(chunk)
            files.append(file)

        return files


    @staticmethod
    def file_exists(file_name, db):
        """
        Check if a file with the given name already exists in the database.

        Args:
            file_name (str): The name of the file to check.
            db (sqlite3.Connection): The database connection.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        # Execute a query to check if a file with the given name exists in the 'file' table
        cursor = db.execute("SELECT 1 FROM file WHERE name = ?", (file_name,))
        return cursor.fetchone() is not None  # Return True if a record is found, otherwise False

    @staticmethod
    def delete_from_db(file_id, db):
        """
        Delete a file and its associated chunks from the database.

        Args:
            file_id (str): The ID of the file to be deleted.
            db (sqlite3.Connection): The database connection.
        """
        # Delete all chunks associated with the file from the 'file_chunk' table
        db.execute("DELETE FROM file_chunk WHERE file_id = ?", (str(file_id),))
        # Delete the file from the 'file' table
        db.execute("DELETE FROM file WHERE id = ?", (str(file_id),))
        
    def to_dict(self):
        """
        Convert the File object to a dictionary.

        Returns:
            dict: A dictionary representation of the File object.
        """
        return {
            'id': self.id,
            'name': self.name,
            'file_type': self.file_type,
            'total_size': self.total_size,
            'date': self.date,
            'chunks': [chunk.to_dict() for chunk in self.chunks]  # Convert each chunk to a dictionary
        }

class FileChunk:
    def __init__(self, file_id, chunk_number, chunk_size, chunk_id):
        """
        Initialize a new FileChunk object.

        Args:
            file_id (str): The ID of the file to which this chunk belongs.
            chunk_number (int): The sequence number of this chunk.
            chunk_size (int): The size of this chunk.
        """
        self.id = chunk_id
        self.file_id = file_id
        self.chunk_number = chunk_number
        self.chunk_size = chunk_size

    def save_to_db(self, db):
        """
        Save the file chunk to the database.

        Args:
            db (sqlite3.Connection): The database connection.
        """
        # Insert chunk metadata into the 'file_chunk' table
        db.execute(
            "INSERT INTO file_chunk (id, file_id, chunk_number, chunk_size) VALUES (?, ?, ?, ?)",
            (self.id, self.file_id, self.chunk_number, self.chunk_size)
        )
    def to_dict(self):
        """
        Convert the FileChunk object to a dictionary.

        Returns:
            dict: A dictionary representation of the FileChunk object.
        """
        return {
            'id': self.id,
            'file_id': self.file_id,
            'chunk_number': self.chunk_number,
            'chunk_size': self.chunk_size
        }