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
            self.text_to_utf8(text),
            DialogflowConfig_TTS.language_code,
        )
        return self.genereate_json_with_utf8(response)
    
    def genereate_json_with_utf8(self, obj):
        return json.dumps(obj, ensure_ascii=False).encode('utf8')
    
    def text_to_utf8(self, text):
        return text.encode('utf8')
