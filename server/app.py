
import os

from server import FlaskServer

from api.chatbot import Chatbot
from api.tts import TTS
from api.test import Test


# Constants
PORT = int(os.getenv('PORT', 8080)) # 8080 is the default port

# Create Flask server
server = FlaskServer(port=PORT)

# Define routes
API = server.api

@API.route('/chatbot')
class ChatbotAPI(Chatbot):
    def is_api(self):
        return True

@API.route('/tts')
class TTS_API(TTS):
    def is_api(self):
        return True

@API.route('/test')
class TestAPI(Test):pass

# run the server
server.run()
