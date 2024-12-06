from .question_en import Question
from colorama import Fore, Style
import unicodedata

class ShortAnswerQuestion(Question):
    def __init__(self, text, correct_answer, image=None, score_value=1, immediate_feedback=False):
        super().__init__(text, correct_answer, image=image, score_value=score_value)
        self.immediate_feedback = immediate_feedback  # Nuevo parámetro

    def normalize_text(self, text):
        """Converts text to lowercase and removes accents and special characters."""
        text = text.lower()  # Convert to lowercase
        text = unicodedata.normalize('NFKD', text)  # Normalize characters
        text = "".join([c for c in text if not unicodedata.combining(c)])  # Remove accents
        return text

    def check_answer(self, answer):
        # Normalize both the correct answer and the user's answer
        return self.normalize_text(answer) == self.normalize_text(self.correct_answer)

    def display(self):
        print("\n" + Fore.CYAN + "✏️ Short Answer Question:" + Style.RESET_ALL)
        print(Fore.CYAN + f"Question points: {self.score_value} point(s)" + Style.RESET_ALL)
        print(Fore.YELLOW + self.text + Style.RESET_ALL)
        
        self.display_image()
        
        answer = input("Enter your answer: ")
        is_correct = self.check_answer(answer)
        if self.immediate_feedback:
            if is_correct:
                print(Fore.GREEN + "Correct!" + Style.RESET_ALL)
            else:
                print(Fore.RED + f"Incorrect. The correct answer was: {self.correct_answer}" + Style.RESET_ALL)
        
        return self.score_value if is_correct else 0
