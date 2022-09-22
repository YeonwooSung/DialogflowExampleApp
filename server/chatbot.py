from flask import Response
from functools import wraps
from flask_restx import Resource
import uuid
import json

from config import DialogflowConfig_TTS
from dialogflow_util import detect_intent_texts


def as_json(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        data = f(*args, **kwargs)
        return Response(json.dumps(data), mimetype='application/json; charset=utf-8')
    return wrapper


class Chatbot(Resource):
    def get(self):
        text = '안녕!'
        return self.run_chatbot(text)

    def run_chatbot(self, text):
        session_id = str(uuid.uuid4())
        response = detect_intent_texts(
            DialogflowConfig_TTS.project_id,
            DialogflowConfig_TTS.location,
            DialogflowConfig_TTS.agent_id,
            session_id,
            text,
            DialogflowConfig_TTS.language_code,
        )
        return self.genereate_json_with_utf8(response)
    
    @as_json
    def genereate_json_with_utf8(self, input_data):
        return {"결과": input_data}
