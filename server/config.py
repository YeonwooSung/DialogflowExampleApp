from google.cloud.dialogflowcx_v3.types import audio_config


class DialogflowConfig:
    project_id='r3test'
    location='asia-northeast1'
    agent_id='254d14dd-3328-4620-ada6-6b7a97bb10da'
    language_code='ko'

class DialogflowConfig_TTS(DialogflowConfig):
    audio_encoding=audio_config.AudioEncoding.AUDIO_ENCODING_LINEAR_16
