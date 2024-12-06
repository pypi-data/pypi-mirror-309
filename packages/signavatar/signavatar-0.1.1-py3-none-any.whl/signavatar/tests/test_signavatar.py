import unittest
import sys
import os

# Ensure the module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from signavatar import SignAvatar

class TestSignAvatar(unittest.TestCase):
    def setUp(self):
        self.api_key = "uvokDksyBRgPVBWtKx5vVxSNuh4As2JA"
        self.avatar = SignAvatar(api_key=self.api_key, default_speed="normal", style={"color": "blue", "brightness": 0.8}, expression="happy")

    def test_get_gif_url(self):
        url = self.avatar.get_gif_url("hello")
        self.assertIsNotNone(url, "URL for 'hello' not found.")

    def test_sign(self):
        # Capture the printed output and validate animation creation
        with self.assertLogs(level="INFO") as cm:
            self.avatar.sign("Hello how are you")
            self.assertGreater(len(cm.output), 0, "Animation sequence should not be empty.")
            self.assertIn("Displaying merged animation", cm.output[0])

    def test_display_gifs(self):
        urls = ["https://media.giphy.com/media/3o6fJaGn56u8Dm6ScE/giphy.gif"]
        with self.assertLogs(level="INFO") as cm:
            self.avatar.display_gifs(urls)
            self.assertGreater(len(cm.output), 0, "GIFs should be displayed.")
            self.assertIn("Displaying merged animation", cm.output[0])

if __name__ == "__main__":
    unittest.main()


from signavatar import SignAvatar

api_key = "uvokDksyBRgPVBWtKx5vVxSNuh4As2JA"
avatar = SignAvatar(api_key, default_speed="normal", style={"color": "blue", "brightness": 0.8}, expression="happy")
avatar.sign("Hello how are you")
