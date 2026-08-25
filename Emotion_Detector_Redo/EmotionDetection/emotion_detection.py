import requests

URL = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
HEADERS = {'grpc-metadata-mm-model-id': 'emotion_aggregated-workflow_lang_en_stock'}


def emotion_detector(text_to_analyze):
    payload = {'raw_document': {'text': text_to_analyze}}
    response = requests.post(url=URL, headers=HEADERS, json=payload)

    if response.status_code == 400:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    response_dict = response.json()
    emotions = response_dict['emotionPredictions'][0]['emotion']

    dominant_emotion = max(emotions, key=emotions.get)
    emotions['dominant_emotion'] = dominant_emotion
    return emotions
