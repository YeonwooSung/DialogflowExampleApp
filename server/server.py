from flask import Flask, request
from flask_restx import Api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_ipban import IpBan
import os
from werkzeug.utils import secure_filename

from asr import AutomaticSpeechRecognition
from chatbot import Chatbot
from config import INPUT_MEDIA_DIR
from tts import TTS
from test import Test



class FlaskServer:
    def __init__(self, 
        name:str='Dialogflow_CX_API_WebServer', 
        title:str='Dialogflow_CX_API_WebServer', 
        description:str='Dialogflow CX API server', 
        port:int=8080, version='1.0', 
        host='0.0.0.0',
        ip_ban_mode:bool=True,
        limit_mode:bool=True,
        ascii_mode:bool=False,
    ):
        self.name = name
        self.title = title
        self.description = description
        self.port = port
        self.host = host

        self.endpoints_added = False

        # init Flask application
        self.app = Flask(name)
        if not ascii_mode:
            self.app.config['JSON_AS_ASCII'] = False
        self.api = Api(
            self.app, 
            version=version, 
            title=title, 
            description=description,
            terms_url='/'
        )

        self.limit_mode = limit_mode
        self.limiter = None
        # limiter
        if self.limit_mode:
            self.limiter = Limiter(
                self.app,
                key_func=get_remote_address,
                default_limits=["200 per day", "50 per hour"]
            )
        
        # ip ban mode
        self.ip_ban_mode = ip_ban_mode
        if self.ip_ban_mode:
            ip_ban = IpBan(ban_seconds=200)
            ip_ban.init_app(self.app)


    def run(self, debug:bool=True):
        if not self.endpoints_added:
            self.add_routers()
        self.app.run(debug=True, host=self.host, port=self.port)


    def add_routers(self):
        self.endpoints_added = True

        # Define routes
        API = self.api

        @API.route('/asr')
        class ASR(AutomaticSpeechRecognition):
            def post(self):
                if 'file' not in request.files:
                    return 'File is missing', 404
                audio_file = request.files['file']
                try:
                    input_file_path = self.parse_uploaded_file(audio_file)
                    return self.run_asr(input_file_path, from_android=True)
                except Exception as e:
                    return str(e), 400
            
            def parse_uploaded_file(self, audio_file):
                if audio_file.filename == '':
                    raise Exception('File is missing')
                filename = secure_filename(audio_file.filename)
                input_file_path = os.path.join(INPUT_MEDIA_DIR, filename)
                audio_file.save(input_file_path)
                audio_file.close()

                print('input_file_path:', input_file_path)

                if not os.path.exists(input_file_path):
                    raise Exception('File not found')
                return input_file_path

        @API.route('/asr/web')
        class STT(ASR):
            def post(self):
                if 'file' not in request.files:
                    return 'File is missing', 404
                audio_file = request.files['file']
                try:
                    input_file_path = self.parse_uploaded_file(audio_file)
                    return self.run_asr(input_file_path, from_android=False)
                except Exception as e:
                    return str(e), 400


        @API.route('/chatbot')
        class ChatbotAPI(Chatbot):
            def post(self):
                parameter_dict = request.args.to_dict()
                if len(parameter_dict) == 0:
                    # set status code as 400
                    return {'error': 'no parameter'}, 400
                if 'text' not in parameter_dict:
                    # set status code as 400
                    return {'error': 'no text parameter'}, 400
                text = parameter_dict['text']
                return self.run_chatbot(text)

        @API.route('/tts')
        class TTS_API(TTS):
            def post(self):
                parameter_dict = request.args.to_dict()
                if len(parameter_dict) == 0:
                    # set status code as 400
                    return {'error': 'no parameter'}, 400
                if 'text' not in parameter_dict:
                    # set status code as 400
                    return {'error': 'no text parameter'}, 400
                text = parameter_dict['text']
                return self.run_tts(text)

        @API.route('/test')
        class TestAPI(Test):pass
