import csv
import cv2
import urllib.request
import numpy as np

class SignAvatar:
    def __init__(self, language="ASL", default_speed='normal', style=None, expression='neutral'):
        self.language = language
        self.default_speed = default_speed
        self.style = style or {"color": "default", "brightness": 1.0}
        self.expression = expression
        self.gestures = self.load_gestures()

    def load_gestures(self):
        gestures = {}
        try:
            with open('ASLLVD_videos.csv', mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    sign_word = row['sign_word'].lower()
                    video_url = row['video_url']
                    gestures[sign_word] = video_url
            print(f"Loaded gestures for {self.language}")
        except FileNotFoundError:
            print(f"Gesture file for {self.language} not found.")
        return gestures

    def get_video_url(self, sign_word):
        sign_word = sign_word.lower()
        gesture_url = self.gestures.get(sign_word)
        if gesture_url:
            return gesture_url
        else:
            print(f"Gesture for '{sign_word}' not found.")
            return None

    def sign(self, text, speed=None):
        speed = speed or self.default_speed
        words = text.split()
        video_paths = []

        for word in words:
            gesture_url = self.get_video_url(word)
            if gesture_url:
                video_path = self.download_video(gesture_url, word)
                if video_path:
                    video_paths.append(video_path)
            else:
                print(f"[{word}] sign missing.")
        
        if video_paths:
            self.combine_videos(video_paths, output_path="output_video.mp4", speed=speed)
        else:
            print("No valid gesture videos to combine.")

    def download_video(self, url, word):
        try:
            video_path = f"{word}.mp4"
            urllib.request.urlretrieve(url, video_path)
            return video_path
        except urllib.error.HTTPError as e:
            print(f"Error downloading video for {word}: {e}")
            return None
        except Exception as e:
            print(f"Error downloading video for {word}: {e}")
            return None

    def combine_videos(self, video_paths, output_path, speed):
        try:
            video_clips = [cv2.VideoCapture(path) for path in video_paths]
            frame_width = int(video_clips[0].get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(video_clips[0].get(cv2.CAP_PROP_FRAME_HEIGHT))
            frame_rate = int(video_clips[0].get(cv2.CAP_PROP_FPS))

            out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (frame_width, frame_height))

            for clip in video_clips:
                while clip.isOpened():
                    ret, frame = clip.read()
                    if not ret:
                        break
                    out.write(frame)
                clip.release()

            out.release()
            print(f"Combined video saved as {output_path}")

            # Play the combined video
            self.play_video(output_path)
        except Exception as e:
            print(f"Error combining videos: {e}")

    def play_video(self, video_path):
        try:
            cap = cv2.VideoCapture(video_path)
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                cv2.imshow("Combined Gesture Video", frame)
                if cv2.waitKey(int(1000 / 30)) & 0xFF == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            print(f"Error playing video: {e}")

# Usage Example
if __name__ == "__main__":
    avatar = SignAvatar(language="ASL", default_speed="normal", style={"color": "blue", "brightness": 0.8}, expression="happy")

    # Test the sign method with a phrase
    avatar.sign("Hello how are you?")
