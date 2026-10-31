"""Unit tests for the emotion detection package."""

import unittest
from unittest.mock import Mock, patch

from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    """Check result formatting and error handling without network access."""

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_returns_all_scores_and_dominant_emotion(self, mock_post):
        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: {
                "emotionPredictions": [
                    {
                        "emotion": {
                            "anger": 0.1,
                            "disgust": 0.05,
                            "fear": 0.2,
                            "joy": 0.6,
                            "sadness": 0.05,
                        }
                    }
                ]
            },
        )
        result = emotion_detector("I am glad this happened")
        self.assertEqual(
            result,
            {
                "anger": 0.1,
                "disgust": 0.05,
                "fear": 0.2,
                "joy": 0.6,
                "sadness": 0.05,
                "dominant_emotion": "joy",
            },
        )
        mock_post.assert_called_once()

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_http_400_returns_empty_result(self, mock_post):
        mock_post.return_value = Mock(status_code=400)
        result = emotion_detector("")
        self.assertIsNone(result["dominant_emotion"])
        self.assertTrue(
            all(
                result[label] is None
                for label in ("anger", "disgust", "fear", "joy", "sadness")
            )
        )

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_blank_input_does_not_call_watson(self, mock_post):
        result = emotion_detector("   ")
        self.assertIsNone(result["dominant_emotion"])
        mock_post.assert_not_called()


if __name__ == "__main__":
    unittest.main()

