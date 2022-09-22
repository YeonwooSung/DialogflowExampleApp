
import os

from config import DEFAULT_MEDIA_DIR, INPUT_MEDIA_DIR
from server import FlaskServer


# Check if media directories exist. If not, create them.
if not os.path.exists(DEFAULT_MEDIA_DIR):
    os.makedirs(DEFAULT_MEDIA_DIR)
if not os.path.exists(INPUT_MEDIA_DIR):
    os.makedirs(INPUT_MEDIA_DIR)

# Constants
PORT = int(os.getenv('PORT', 8080)) # 8080 is the default port

# Create Flask server
server = FlaskServer(port=PORT)

# run the server
server.run()
