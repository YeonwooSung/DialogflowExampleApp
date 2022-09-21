
import os

from server import FlaskServer

from api.tts import TTS


# Constants
PORT = int(os.getenv('PORT', 8080)) # 8080 is the default port

# Create Flask server
server = FlaskServer(port=PORT)

# Define routes
API = server.api

@API.route('/tts')
class TTS_API(TTS):
    def is_api(self):
        return True

# run the server
server.run()
