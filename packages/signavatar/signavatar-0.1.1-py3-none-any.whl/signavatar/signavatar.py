import requests
import imageio
from PIL import Image
import time
import io
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SignAvatar:
    def __init__(self, api_key, default_speed='normal', style=None, expression='neutral'):
        self.api_key = api_key
        self.default_speed = default_speed
        self.style = style or {"color": "default", "brightness": 1.0}
        self.expression = expression

    def get_gif_url(self, word):
        """
        Fetch a GIF URL from Giphy for a given word.
        
        Args:
            word (str): The word to fetch the GIF for.
        
        Returns:
            str: The GIF URL if found, or None if not found.
        """
        try:
            response = requests.get(
                f"https://api.giphy.com/v1/gifs/search",
                params={
                    "api_key": self.api_key,
                    "q": word,
                    "limit": 1,
                    "rating": "G"
                }
            )
            data = response.json()
            if data['data']:
                return data['data'][0]['images']['downsized']['url']
            else:
                logger.info(f"No GIF found for '{word}'.")
                return None
        except Exception as e:
            logger.error(f"Error fetching GIF for '{word}': {e}")
            return None

    def sign(self, text, speed=None):
        """
        Convert a sentence into a sequence of gesture animations using Giphy GIFs.
        
        Args:
            text (str): Input text to be converted to ASL gestures.
            speed (str): Speed of the animation.
        
        Returns:
            list: Animation sequence based on the input text.
        """
        speed = speed or self.default_speed
        words = text.split()
        gif_urls = []

        for word in words:
            gif_url = self.get_gif_url(word)
            if gif_url:
                gif_urls.append(gif_url)
            else:
                gif_urls.append(f"[{word}] GIF missing.")

        if gif_urls:
            self.display_gifs(gif_urls)
        else:
            logger.info("No valid GIFs to display.")

    def display_gifs(self, gif_urls):
        """
        Display a sequence of GIFs.
        
        Args:
            gif_urls (list): List of GIF URLs to be displayed.
        """
        try:
            for url in gif_urls:
                if "GIF missing" not in url:
                    response = requests.get(url)
                    gif = Image.open(io.BytesIO(response.content))
                    gif.show()
                    time.sleep(2)  # Display each GIF for 2 seconds
                else:
                    logger.info(url)
            logger.info("Displaying merged animation.")
        except Exception as e:
            logger.error(f"Error displaying GIFs: {e}")

# Usage Example
if __name__ == "__main__":
    api_key = "uvokDksyBRgPVBWtKx5vVxSNuh4As2JA"
    avatar = SignAvatar(api_key, default_speed="normal", style={"color": "blue", "brightness": 0.8}, expression="happy")

    # Test the sign method with a phrase
    avatar.sign("Hello how are you")
