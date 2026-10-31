"""Unit tests for the emotion detection package."""

import unittest
from unittest.mock import Mock, patch

from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    """Check result formatting and error handling without network access."""

    def analyze_with_dominant(self, dominant):
        """Return a mocked prediction whose highest score is dominant."""
        scores = {
            emotion: 0.1
            for emotion in ("anger", "disgust", "fear", "joy", "sadness")
        }
        scores[dominant] = 0.9
        response = Mock(
            status_code=200,
            json=lambda: {"emotionPredictions": [{"emotion": scores}]},
        )
        with patch(
            "EmotionDetection.emotion_detection.requests.post",
            return_value=response,
        ) as mock_post:
            result = emotion_detector("A sample sentence")
        mock_post.assert_called_once()
        return result["dominant_emotion"]

    def test_anger(self):
        self.assertEqual(self.analyze_with_dominant("anger"), "anger")

    def test_disgust(self):
        self.assertEqual(self.analyze_with_dominant("disgust"), "disgust")

    def test_fear(self):
        self.assertEqual(self.analyze_with_dominant("fear"), "fear")

    def test_joy(self):
        self.assertEqual(self.analyze_with_dominant("joy"), "joy")

    def test_sadness(self):
        self.assertEqual(self.analyze_with_dominant("sadness"), "sadness")

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

