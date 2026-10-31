"""Call the Watson NLP emotion prediction service."""

from __future__ import annotations

import requests

URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}
EMOTION_LABELS = ("anger", "disgust", "fear", "joy", "sadness")


def _empty_result() -> dict[str, float | None]:
    """Return the stable result shape used when the service rejects input."""
    result: dict[str, float | None] = {
        emotion: None for emotion in EMOTION_LABELS
    }
    result["dominant_emotion"] = None
    return result


def emotion_detector(text_to_analyze: str | None) -> dict[str, float | str | None]:
    """Return five emotion scores and the emotion with the highest score.

    A Watson HTTP 400 is represented by None scores so the Flask layer can
    return a clear client error. Other HTTP and response-format failures raise
    an exception for the caller to handle.
    """
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return _empty_result()

    payload = {"raw_document": {"text": text_to_analyze.strip()}}
    response = requests.post(
        URL,
        headers=HEADERS,
        json=payload,
        timeout=15,
    )

    if response.status_code == 400:
        return _empty_result()

    response.raise_for_status()
    data = response.json()
    predictions = data.get("emotionPredictions")
    if not predictions or not isinstance(predictions[0], dict):
        raise ValueError("Watson returned no emotion predictions.")

    scores = predictions[0].get("emotion")
    if not isinstance(scores, dict):
        raise ValueError("Watson returned an invalid emotion score object.")

    result: dict[str, float | str | None] = {
        label: scores.get(label) for label in EMOTION_LABELS
    }
    available_scores = {
        label: value
        for label, value in result.items()
        if label in EMOTION_LABELS and isinstance(value, (int, float))
    }
    result["dominant_emotion"] = (
        max(available_scores, key=available_scores.get)
        if available_scores
        else None
    )
    return result

