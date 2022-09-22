from flask_restx import Resource
import uuid
import json

from config import DialogflowConfig_TTS
from dialogflow_util import detect_intent_texts


class Chatbot(Resource):
    def get(self):
        text = '안녕하세요!'
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
    
    def genereate_json_with_utf8(self, input_data):
        #return (json.dumps(input_data, ensure_ascii=False)).encode('utf8'), {'Content-Type': 'application/json; charset=utf-8'}
        return {"결과": input_data}, {'Content-Type': 'application/json; charset=utf-8'}
