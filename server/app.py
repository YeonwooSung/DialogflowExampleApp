
import os

from server.server import FlaskServer


# Constants
PORT = int(os.getenv('PORT', 8080)) # 8080 is the default port

# if __name__ == "__main__":
server = FlaskServer(name=__name__, port=PORT)
server.run()
