from .question_en import Question
from colorama import Fore, Style

class TrueFalseQuestion(Question):
    def __init__(self, text, correct_answer, image=None, score_value=1,  immediate_feedback=False):
        super().__init__(text, correct_answer, image=image, score_value=score_value)
        self.immediate_feedback = immediate_feedback  

    def display(self):
        print("\n" + Fore.CYAN + "✅ True/False Question:" + Style.RESET_ALL)
        print(Fore.CYAN + f"Question points: {self.score_value} point(s)" + Style.RESET_ALL)
        print(Fore.YELLOW + self.text + Style.RESET_ALL)
        
        self.display_image()
        
        while True:
            answer = input("Type 'True' or 'False': ").strip().lower()
            if answer in ['true', 'false']:
                is_correct = self.check_answer(answer == 'true')
                if self.immediate_feedback:
                    if is_correct:
                        print(Fore.GREEN + "Correct!" + Style.RESET_ALL)
                    else:
                        correct_answer_text = "True" if self.correct_answer else "False"
                        print(Fore.RED + f"Incorrect. The correc answer was: {correct_answer_text}" + Style.RESET_ALL)
                
                return self.score_value if is_correct else 0 
            else:
                print(Fore.RED + "Invalid response. Please answer with 'True' or 'False'." + Style.RESET_ALL)
