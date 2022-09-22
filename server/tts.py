from flask import send_file
from flask_restx import Resource
import uuid
import os

from config import DialogflowConfig_TTS, DEFAULT_MEDIA_DIR
from dialogflow_util import detect_intent_synthesize_tts_response


class TTS(Resource):
    def get(self):
        return self.run_tts('오늘 날씨 알려줘!')

    def run_tts(self, text):
        session_id = str(uuid.uuid4())
        output_file_path = f'{DEFAULT_MEDIA_DIR}/{session_id}.mp4'
        detect_intent_synthesize_tts_response(
            DialogflowConfig_TTS.project_id,
            DialogflowConfig_TTS.location,
            DialogflowConfig_TTS.agent_id,
            text,
            DialogflowConfig_TTS.audio_encoding,
            DialogflowConfig_TTS.language_code,
            output_file_path,
            session_id,
        )

        # check if file exists
        if os.path.isfile(output_file_path):
            return send_file(output_file_path, as_attachment=True)
        else:
            return {'output': 'failed'}
