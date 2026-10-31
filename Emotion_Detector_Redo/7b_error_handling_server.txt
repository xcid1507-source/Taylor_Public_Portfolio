"""Flask web server for the Watson NLP emotion detector."""

from flask import Flask, render_template, request
import requests

from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")


@app.route("/emotionDetector")
def emotion_detector_function():
    """Analyze input and return the five scores and dominant emotion."""
    text_to_analyze = request.args.get("textToAnalyze")
    if text_to_analyze is None or not text_to_analyze.strip():
        return "Invalid Input! Please try again.", 400

    try:
        response = emotion_detector(text_to_analyze)
    except (requests.RequestException, ValueError):
        app.logger.exception("Emotion analysis request failed")
        return "Emotion analysis is temporarily unavailable.", 502

    if response["dominant_emotion"] is None:
        return "Invalid Input! Please try again.", 400

    response_text = (
        "For the given statement, the system response is "
        f"'anger': {response['anger']}, 'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, 'joy': {response['joy']}, "
        f"'sadness': {response['sadness']}. The dominant emotion is "
        f"{response['dominant_emotion']}."
    )
    return response_text


@app.route("/")
def render_index_page():
    """Render the browser interface."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
