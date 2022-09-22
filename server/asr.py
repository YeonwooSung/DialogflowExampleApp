from flask import send_file
from flask_restx import Resource
import uuid
import os

from config import DialogflowConfig_ASR, DEFAULT_MEDIA_DIR
from dialogflow_util import detect_intent_stream, detect_intent_audio
from wrapper import as_json


class AutomaticSpeechRecognition(Resource):
    def run_asr(self, input_file_path, text_only=False, debug=False):
        session_id = str(uuid.uuid4())
        output_file_path = f'DEFAULT_MEDIA_DIR/{session_id}.mp3'

        # send API request for automatic speech recognition with text to speech
        transcript, response_text, output_file_path = detect_intent_audio(
            DialogflowConfig_ASR.project_id,
            DialogflowConfig_ASR.location,
            DialogflowConfig_ASR.agent_id,
            session_id,
            input_file_path,
            DialogflowConfig_ASR.language_code,
            DialogflowConfig_ASR.audio_encoding,
            output_file_path,
            debug=debug,
        )

        # generate text_only output
        text_only_output_json = {'입력': transcript, '결과': response_text}

        if text_only:
            return self.genereate_json_with_utf8(text_only_output_json)

        # check if file exists
        if os.path.isfile(output_file_path):
            return self.generate_json_response_with_audio(text_only_output_json, output_file_path)
        else:
            return self.genereate_json_with_utf8(text_only_output_json)

    def generate_json_response_with_audio(self, input_data, output_file_path):
        # genearate multipart/form-data response with audio file
        return {
            'json': input_data,
            'audio': send_file(output_file_path, as_attachment=True),
        }, 200, {'Content-Type': 'multipart/form-data; charset=utf-8'}

    @as_json
    def genereate_json_with_utf8(self, input_json):
        return input_json
