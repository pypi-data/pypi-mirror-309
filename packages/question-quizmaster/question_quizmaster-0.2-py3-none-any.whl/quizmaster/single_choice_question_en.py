from .question_en import Question
from colorama import Fore, Style
import string



class SingleChoiceQuestion(Question):
    def __init__(self, text, options, correct_answer, image=None, score_value=1, immediate_feedback=False):
        super().__init__(text, correct_answer, image=image, score_value=score_value)
        self.options = options
        self.immediate_feedback = immediate_feedback

    def display(self):
        print("\n" + Fore.CYAN + "📝 Single choice question:" + Style.RESET_ALL)
        print(Fore.CYAN + f"Question points: {self.score_value} point(s)" + Style.RESET_ALL)
        print(Fore.YELLOW + self.text + Style.RESET_ALL)
        
        self.display_image()
        
        option_letters = list(string.ascii_lowercase)[:len(self.options)]
        for letter, option in zip(option_letters, self.options):
            print(f"  {letter}. {option}")

        while True:
            answer = input("Choose one option (a, b, etc.): ").strip().lower()
            if answer in option_letters:
                is_correct = self.check_answer(option_letters.index(answer))
                if self.immediate_feedback:
                    if is_correct:
                        print(Fore.GREEN + "Correct!" + Style.RESET_ALL)
                    else:
                        correct_option = option_letters[self.correct_answer]
                        print(Fore.RED + f"Incorrect. The correct answers was: {correct_option}. {self.options[self.correct_answer]}" + Style.RESET_ALL)
                return self.score_value if is_correct else 0
            else:
                print(Fore.RED + "Invalid response. Please answer with valid letters." + Style.RESET_ALL)
