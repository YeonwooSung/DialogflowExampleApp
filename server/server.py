from flask import Flask
from flask_restx import Api, Resource


from chatbot import Chatbot
from tts import TTS
from test import Test



class FlaskServer:
    def __init__(self, 
        name:str='Dialogflow_CX_API_WebServer', 
        title:str='Dialogflow_CX_API_WebServer', 
        description:str='Dialogflow CX API server', 
        port:int=8080, version='1.0', 
        host='0.0.0.0',
        ip_ban_mode:bool=False,
    ):
        # self.name = name
        self.title = title
        self.description = description
        self.port = port
        self.host = host

        self.endpoints_added = False

        # init Flask application
        self.app = Flask(name)
        self.api = Api(self.app, version=version, title=title, description=description)

        # ip ban
        if ip_ban_mode:
            from flask_limiter import Limiter
            from flask_limiter.util import get_remote_address
            limiter = Limiter(
                self.app,
                key_func=get_remote_address,
                default_limits=["200 per day", "50 per hour"]
            )

    def run(self, debug:bool=True):
        if not self.endpoints_added:
            self.add_routers()
        self.app.run(debug=True, host=self.host, port=self.port)

    def add_routers(self):
        self.endpoints_added = True

        # Define routes
        API = self.api

        @API.route('/chatbot')
        class ChatbotAPI(Chatbot):pass

        @API.route('/tts')
        class TTS_API(TTS):pass

        @API.route('/test')
        class TestAPI(Test):pass
