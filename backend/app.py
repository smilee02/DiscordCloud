import socket
from src import app
from quart_cors import cors
from src.discord_client import load_discord
from src.services.logging_service import logger

# Enable CORS
app = cors(app, allow_origin="*")  # Allow all origins. You can specify origins if needed.

# Reset DB
# init_db()

@app.before_serving
async def before_serving():
    await load_discord()
    logger.info(f"Max content length: {app.config['MAX_CONTENT_LENGTH']}")

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # This doesn't have to be reachable
        s.connect(('10.254.254.254', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

if __name__ == '__main__':
    local_ip = get_local_ip()
    app.run(host=local_ip, port=5000)
