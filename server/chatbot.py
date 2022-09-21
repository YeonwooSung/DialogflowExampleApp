from flask_restx import Resource
import uuid
import os

from config import DialogflowConfig_TTS
from dialogflow_util import detect_intent_texts


class Chatbot(Resource):
    def get(self):
        text = 'hello'
        session_id = str(uuid.uuid4())
        response = detect_intent_texts(
            DialogflowConfig_TTS.project_id,
            DialogflowConfig_TTS.location,
            DialogflowConfig_TTS.agent_id,
            session_id,
            text,
            DialogflowConfig_TTS.language_code,
        )
        return {'response': response}

    def post(self):
        return {'hello': 'world'}
