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

    def run(self, debug:bool=True):
        if not self.endpoints_added:
            self.add_endpoints()
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
