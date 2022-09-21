
import os

from server import FlaskServer


# Constants
PORT = int(os.getenv('PORT', 8080)) # 8080 is the default port

# Create Flask server
server = FlaskServer(port=PORT)

# run the server
server.run()
