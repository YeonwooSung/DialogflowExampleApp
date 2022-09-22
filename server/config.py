from google.cloud.dialogflowcx_v3.types import audio_config


DEFAULT_MEDIA_DIR = 'media'
INPUT_MEDIA_DIR = 'resources'

class DialogflowConfig:
    project_id='r3test'
    location='asia-northeast1'
    agent_id='254d14dd-3328-4620-ada6-6b7a97bb10da'
    language_code='ko'

class DialogflowConfig_TTS(DialogflowConfig):
    audio_encoding="OUTPUT_AUDIO_ENCODING_MP3_64_KBPS"

class DialogflowConfig_ASR(DialogflowConfig):
    audio_encoding="OUTPUT_AUDIO_ENCODING_MP3_64_KBPS"
    sample_rate_hertz=24000
