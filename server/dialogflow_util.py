import uuid
import os

from google.cloud.dialogflowcx_v3.services.agents import AgentsClient
from google.cloud.dialogflowcx_v3.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3.types import audio_config
from google.cloud.dialogflowcx_v3.types import session

import pyaudio
from pydub import AudioSegment
from pydub.utils import make_chunks


#--------------------------------------------------------------
# TTS (Text to Speech) response

def detect_intent_synthesize_tts_response(
    project_id,
    location,
    agent_id,
    text,
    audio_encoding,
    language_code,
    output_file,
    session_id_str,
):
    """Returns the result of detect intent with synthesized response."""
    client_options = None
    if location != "global":
        api_endpoint = f"{location}-dialogflow.googleapis.com:443"
        print(f"API Endpoint: {api_endpoint}\n")
        client_options = {"api_endpoint": api_endpoint}
    session_client = SessionsClient(client_options=client_options)
    session_id = str(session_id_str)

    # Constructs the audio query request
    session_path = session_client.session_path(
        project=project_id,
        location=location,
        agent=agent_id,
        session=session_id,
    )
    text_input = session.TextInput(text=text)
    query_input = session.QueryInput(
        text=text_input,
        language_code=language_code
    )
    synthesize_speech_config = audio_config.SynthesizeSpeechConfig(
      speaking_rate=1,
      pitch=0.0,
    )
    output_audio_config = audio_config.OutputAudioConfig(
      synthesize_speech_config=synthesize_speech_config,
      audio_encoding=audio_config.OutputAudioEncoding[
        audio_encoding],
    )
    request = session.DetectIntentRequest(
        session=session_path,
        query_input=query_input,
        output_audio_config=output_audio_config,
    )

    response = session_client.detect_intent(request=request)
    print(
      'Speaking Rate: '
      f'{response.output_audio_config.synthesize_speech_config.speaking_rate}')
    print(
      'Pitch: '
      f'{response.output_audio_config.synthesize_speech_config.pitch}')
    with open(output_file, 'wb') as fout:
        fout.write(response.output_audio)
    print(f'Audio content written to file: {output_file}')


#--------------------------------------------------------------
# Chatbot

def detect_intent_texts(project_id, location_id, agent_id, session_id, text, language_code, debug=False):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation."""
    agent = f"projects/{project_id}/locations/{location_id}/agents/{agent_id}"

    session_path = f"{agent}/sessions/{session_id}"
    client_options = None
    agent_components = AgentsClient.parse_agent_path(agent)
    
    location_id = agent_components["location"]
    if location_id != "global":
        api_endpoint = f"{location_id}-dialogflow.googleapis.com:443"
        if debug:
            print(f"API Endpoint: {api_endpoint}\n")
        client_options = {"api_endpoint": api_endpoint}
    session_client = SessionsClient(client_options=client_options)

    text_input = session.TextInput(text=text)
    query_input = session.QueryInput(text=text_input, language_code=language_code)
    request = session.DetectIntentRequest(
        session=session_path, query_input=query_input
    )
    response = session_client.detect_intent(request=request)

    if debug:
        print("=" * 20)
        print(f"Query text: {response.query_result.text}")
    response_messages = [
        " ".join(msg.text.text) for msg in response.query_result.response_messages
    ]

    response_text = ' '.join(response_messages)
    print(f"Response text: {response_text}\n")
    return response_text


#--------------------------------------------------------------
# Automatic Speech Recognition + TTS

def detect_intent_stream(
    project_id, 
    location_id, 
    agent_id, 
    session_id, 
    audio_file_path, 
    language_code, 
    audio_encoding, 
    output_file, 
    debug=True, 
    voice_selection=False,
    speaking_rate=1,
    pitch=0.0,
):
    """Returns the result of detect intent with streaming audio as input.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    agent = f"projects/{project_id}/locations/{location_id}/agents/{agent_id}"

    session_path = f"{agent}/sessions/{session_id}"
    client_options = None
    if location_id != "global":
        api_endpoint = f"{location_id}-dialogflow.googleapis.com:443"
        print(f"API Endpoint: {api_endpoint}\n")
        client_options = {"api_endpoint": api_endpoint}
    session_client = SessionsClient(client_options=client_options)

    input_audio_config = audio_config.InputAudioConfig(
        audio_encoding=audio_config.AudioEncoding.AUDIO_ENCODING_LINEAR_16,
        sample_rate_hertz=24000,
    )

    def request_generator():
        audio_input = session.AudioInput(config=input_audio_config)
        query_input = session.QueryInput(audio=audio_input, language_code=language_code)

        if voice_selection:
            voice_selection = audio_config.VoiceSelectionParams()
            synthesize_speech_config = audio_config.SynthesizeSpeechConfig()
            # Sets the voice name and gender
            voice_selection.name = "en-GB-Standard-A"
            voice_selection.ssml_gender = (
                audio_config.SsmlVoiceGender.SSML_VOICE_GENDER_FEMALE
            )
            synthesize_speech_config.voice = voice_selection
        else:
            synthesize_speech_config = audio_config.SynthesizeSpeechConfig(
                speaking_rate=speaking_rate,
                pitch=pitch,
            )

        # Sets the audio encoding
        output_audio_config = audio_config.OutputAudioConfig(
            synthesize_speech_config=synthesize_speech_config,
            audio_encoding=audio_config.OutputAudioEncoding[audio_encoding],
        )

        # The first request contains the configuration.
        yield session.StreamingDetectIntentRequest(
            session=session_path,
            query_input=query_input,
            output_audio_config=output_audio_config,
        )


        sound = AudioSegment.from_file(audio_file_path)

        p = pyaudio.PyAudio()
        output = p.open(format=p.get_format_from_width(sound.sample_width),
                        channels=sound.channels,
                        rate=sound.frame_rate,
                        output=True) # frames_per_buffer=CHUNK_SIZE
        
        start = 0
        length = sound.duration_seconds
        end = start + length
        volume = 100
        runtime = start
        keep_loop = True
        playchunk = sound[start*1000.0:(start+length)*1000.0] - (60 - (60 * (volume/100.0)))
        millisecondchunk = 50 / 1000.0
        while keep_loop:
            for chunks in make_chunks(playchunk, millisecondchunk * 1000):
                runtime += millisecondchunk
                # output.write(chunks._data)
                audio_input = session.AudioInput(audio=chunks._data)
                query_input = session.QueryInput(audio=audio_input)
                yield session.StreamingDetectIntentRequest(query_input=query_input)
                if runtime >= end:
                    keep_loop = False
                    break

    responses = session_client.streaming_detect_intent(requests=request_generator())

    print("=" * 20)
    for response in responses:
        print(f'Intermediate transcript: "{response.recognition_result.transcript}".')

    # Note: The result from the last response is the final transcript along
    # with the detected content.
    response = response.detect_intent_response
    response_messages = [
        " ".join(msg.text.text) for msg in response.query_result.response_messages
    ]
    response_text = ' '.join(response_messages)

    if debug:
        print("=" * 20)
        print(f"Query text: {response.query_result.transcript}")
        print(f"Response text: {response_text}\n")
        print(
        'Speaking Rate: '
        f'{response.output_audio_config.synthesize_speech_config.speaking_rate}')
        print(
        'Pitch: '
        f'{response.output_audio_config.synthesize_speech_config.pitch}')
    with open(output_file, 'wb') as fout:
        fout.write(response.output_audio)
    
    return response.query_result.transcript, response_text, output_file
