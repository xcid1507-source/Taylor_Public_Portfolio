# Final Project: Watson NLP Emotion Detector

A Flask application that sends text to IBM Watson NLP and displays scores for
anger, disgust, fear, joy, and sadness, together with the dominant emotion.

## Requirements

- Python 3.10 or newer
- Network access to the Watson NLP Skills Network endpoint

## Setup

From this directory, create and activate a virtual environment, then install
the dependencies:

~~~bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
~~~

## Run

~~~bash
python server.py
~~~

Open http://127.0.0.1:5000. The JSON endpoint is
GET /emotionDetector?textToAnalyze=your%20text.

Blank input returns HTTP 400. If Watson is unavailable or returns an invalid
response, the API returns a generic HTTP 502 response and logs details on the
server.

## Tests

The unit tests mock the remote service and do not require network access:

~~~bash
python -m unittest -v
~~~

## Project layout

- EmotionDetection/emotion_detection.py — Watson request and result formatting
- server.py — Flask routes and HTTP error handling
- templates/index.html and static/app.js — browser interface
- test_emotion_detection.py — offline unit tests

