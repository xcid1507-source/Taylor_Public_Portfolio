"""Flask web application for Watson NLP emotion detection."""

from flask import Flask, jsonify, render_template, request
import requests

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.get("/")
def root():
    """Render the application interface."""
    return render_template("index.html")


@app.get("/emotionDetector")
def emotion_detector_route():
    """Validate input and return the emotion prediction as JSON."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    if not text_to_analyze.strip():
        return jsonify({"error": "Please enter text to analyze."}), 400

    try:
        result = emotion_detector(text_to_analyze)
    except (requests.RequestException, ValueError):
        app.logger.exception("Emotion analysis request failed")
        return jsonify({"error": "Emotion analysis is temporarily unavailable."}), 502

    if result.get("dominant_emotion") is None:
        return jsonify({"error": "Watson could not analyze the supplied text."}), 400

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

