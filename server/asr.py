from flask import send_file
from flask_restx import Resource
import uuid
import os

from config import DialogflowConfig_TTS
from dialogflow_util import detect_intent_stream
from wrapper import as_json


class AutomaticSpeechRecognition(Resource):
    def run_asr(self, input_file_path, text_only=False, debug=False):
        session_id = str(uuid.uuid4())
        output_file_path = f'{session_id}.mp4'

        # send API request for automatic speech recognition with text to speech
        transcript, response_text, output_file_path = detect_intent_stream(
            DialogflowConfig_TTS.project_id,
            DialogflowConfig_TTS.location,
            DialogflowConfig_TTS.agent_id,
            session_id,
            input_file_path,
            DialogflowConfig_TTS.language_code,
            DialogflowConfig_TTS.audio_encoding,
            output_file_path,
            debug=debug,
        )

        # generate text_only output
        text_only_output_json = {'입력': transcript, '결과': response_text}

        # check if file exists
        if os.path.isfile(output_file_path):
            return send_file(output_file_path, as_attachment=True)
        else:
            return self.genereate_json_with_utf8(text_only_output_json)

    @as_json
    def genereate_json_with_utf8(self, input_json):
        return input_json
