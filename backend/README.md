# Backend README

This is the backend repository for **DiscordCloud**. It contains the server-side code responsible for handling file uploads, downloads, encryption, and other backend functionalities.

## Technologies Used

- Python
- Quart (ASGI web framework)
- SQLite (Python SQL toolkit and Object-Relational Mapping)
- Discord API (for file storage and retrieval)
- dotenv (for managing environment variables)
- Other Python libraries as required

## Setup Instructions

1. Clone this repository to your local machine.
2. Install Python if not already installed.
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source .venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Set up environment variables by creating a `.env` file and adding necessary configurations. Refer to `.env.example` for required variables.
7. Run the backend server: `python app.py`
8. The backend server should now be running locally.

## Usage

- This backend provides endpoints for file upload, download, deletion, and listing files.
- You can interact with the backend API using HTTP requests from your frontend application or any REST client.

## License

This project is licensed under the Educational Use License. See the LICENSE file for details.
