import os
import time
from google.cloud import speech_v1
from google.cloud.speech_v1 import types
import pyaudio

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_your_service_account_key.json"

def transcribe_stream_with_word_level_confidence():
    client = speech_v1.SpeechClient()

    config = types.RecognitionConfig(
        encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_word_confidence=True
    )

    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True
    )

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    stream.start_stream()

    requests = (types.StreamingRecognizeRequest(audio_content=chunk) for chunk in iter(lambda: stream.read(1024), b""))

    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        for result in response.results:
            for word_info in result.alternatives[0].words:
                word = word_info.word.lower()
                confidence = word_info.confidence
                if word in ["hellfire", "recall"] and confidence > 0.9:
                    print(f"Word: {word}, Confidence: {confidence}")

    stream.stop_stream()
    stream.close()
    p.terminate()

transcribe_stream_with_word_level_confidence()
