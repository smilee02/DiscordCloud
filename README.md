# DiscordCloud

DiscordCloud is a cloud storage application that utilizes Discord's platform for file storage and retrieval. It provides users with a simple and secure way to upload, download, and manage files through a web interface.

## Features

- Upload files to Discord for storage.
- Download files from Discord to your local machine.
- Delete files stored on Discord.
- View a list of files stored on Discord.

## Technologies Used

### Frontend

- React.js
- Next.js

### Backend

- Python
- Quart
- SQLite
- Discord API
- dotenv
- cryptography

## Setup Instructions

### Frontend

1. Clone the frontend repository to your local machine.
2. Navigate to the project directory.
3. Install Node.js and npm if not already installed.
4. Install dependencies: `npm install`
5. Run the frontend server: `npm run dev`
6. Access the application in your web browser at `http://{YOUR_LOCAL_IP_ADDRESS}:3000`.

### Backend

1. Clone the backend repository to your local machine.
2. Install Python if not already installed.
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source .venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Set up environment variables by creating a `.env` file and adding necessary configurations. Refer to `.env.example` for required variables.
7. Run the backend server: `python app.py`

## Usage

- Access the DiscordCloud application in your web browser to interact with the frontend.
- Use the backend API endpoints to perform file upload, download, deletion, and listing functionalities.
- Ensure proper setup of environment variables for the backend to communicate with the Discord API.

## License

This project is licensed under the Educational Use License. See the LICENSE file for details.
