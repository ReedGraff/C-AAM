import os
import time
from google.cloud import speech_v1
from google.cloud.speech_v1 import types
import pyaudio

os.environ["key"] = "AIzaSyAx639c5Nzd4ff3DxtXCwHGmskY4WV8PhE"
print(os.environ['key'])

def levenshtein_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for index2, char2 in enumerate(s2):
        new_distances = [index2 + 1]
        for index1, char1 in enumerate(s1):
            if char1 == char2:
                new_distances.append(distances[index1])
            else:
                new_distances.append(1 + min((distances[index1], distances[index1 + 1], new_distances[-1])))
        distances = new_distances

    return distances[-1]

def most_similar_word(target_word, word_list):
    return min(word_list, key=lambda word: levenshtein_distance(target_word, word))

def transcribe_stream_with_word_level_confidence():
    client = speech_v1.SpeechClient(client_options={"api_key": os.environ['key']})

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
                print(most_similar_word(word_info.word, ["hellfire", "recall"]))

    stream.stop_stream()
    stream.close()
    p.terminate()

transcribe_stream_with_word_level_confidence()
