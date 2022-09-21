
import os

from server import FlaskServer


# Constants
PORT = int(os.getenv('PORT', 8080)) # 8080 is the default port

server = FlaskServer(port=PORT)
server.run()
