import unittest
from EmotionDetection.emotion_detection import emotion_detector


class TestDominantEmotions(unittest.TestCase):

    def get_emotion(self, text: str) -> str:
        emotions = emotion_detector(text)
        return emotions.get('dominant_emotion')

    def test_joy(self):
        self.assertEqual(
            self.get_emotion('I am glad this happened'), 'joy'
        )

    def test_anger(self):
        self.assertEqual(
            self.get_emotion('I am really mad about this'), 'anger'
        )

    def test_disgust(self):
        self.assertEqual(
            self.get_emotion(
                'I feel disgusted just hearing about this'
            ),
            'disgust'
        )

    def test_sadness(self):
        self.assertEqual(
            self.get_emotion('I am so sad about this'), 'sadness'
        )

    def test_fear(self):
        self.assertEqual(
            self.get_emotion(
                'I am really afraid that this will happen'
            ),
            'fear'
        )


if __name__ == '__main__':
    unittest.main()
