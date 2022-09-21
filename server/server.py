from flask import Flask
from flask_restx import Api, Resource


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

        # init Flask application
        self.app = Flask(name)
        self.api = Api(self.app, version=version, title=title, description=description)

    def run(self, debug:bool=True):
        self.app.run(debug=True, host=self, port=self.port)
