import unittest
from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    def test_joy(self):
        self.assertEqual(emotion_detector('I am glad this happened') ['dominant_emotion'], 'joy')

    def test_anger(self):
        self.assertEqual(emotion_detector('I am furious about this') ['dominant_emotion'], 'anger')

    def test_disgust(self):
        self.assertEqual(emotion_detector('This is disgusting') ['dominant_emotion'], 'disgust')

    def test_sadness(self):
        self.assertEqual(emotion_detector('I am sad about this') ['dominant_emotion'], 'sadness')

    def test_fear(self):
        self.assertEqual(emotion_detector('I am afraid of this') ['dominant_emotion'], 'fear')


if __name__ == '__main__':
    unittest.main()
