from flask import Response
from flask_restx import Resource
import uuid
import os

from requests_toolbelt import MultipartEncoder

from config import DialogflowConfig_ASR, DEFAULT_MEDIA_DIR
from dialogflow_util import detect_intent_stream, detect_intent_audio
from wrapper import as_json


class AutomaticSpeechRecognition(Resource):
    def run_asr(self, input_file_path, text_only=False, debug=False):
        session_id = str(uuid.uuid4())
        output_file_path = f'{DEFAULT_MEDIA_DIR}/{session_id}.mp3'

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

    def generate_json_response_with_audio(self, input_text, response_text, output_file_path):
        # genearate multipart/form-data response with audio file
        m = MultipartEncoder(
            fields={
                'input': input_text,
                'output': response_text,
                'audio': (output_file_path, open(output_file_path, 'rb'), 'audio/mpeg'),
            }
        )
        return Response(m.fields, mimetype=m.content_type)

    @as_json
    def genereate_json_with_utf8(self, input_json):
        return input_json
