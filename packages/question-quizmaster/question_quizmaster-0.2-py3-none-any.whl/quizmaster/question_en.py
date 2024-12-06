from colorama import Fore, Style
from PIL import Image

class Question:
    def __init__(self, text, correct_answer, image=None, score_value=1,  immediate_feedback=False):
        self.text = text
        self.correct_answer = correct_answer
        self.image = image  # Optional image path
        self.score_value = score_value  # Value in points for the question

    def check_answer(self, answer):
        return answer == self.correct_answer

    def display_image(self):
        if self.image:
            try:
                # Attempt to open the image in the system image viewer
                img = Image.open(self.image)
                img.show()  # Opens the image in a popup window
            except Exception as e:
                print(Fore.RED + f"Error loading the image: {e}" + Style.RESET_ALL)
