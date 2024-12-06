from .question_es import Question
from colorama import Fore, Style

class TrueFalseQuestion(Question):
    def __init__(self, text, correct_answer, image=None, score_value=1, immediate_feedback=False):
        super().__init__(text, correct_answer, image=image, score_value=score_value)
        self.immediate_feedback = immediate_feedback  # Nuevo parámetro

    def display(self):
        print("\n" + Fore.CYAN + "✅ Pregunta Verdadero/Falso:" + Style.RESET_ALL)
        print(Fore.CYAN + f"Puntos de la pregunta: {self.score_value} punto(s)" + Style.RESET_ALL)
        print(Fore.YELLOW + self.text + Style.RESET_ALL)
        
        self.display_image()
        
        while True:
            answer = input("Escribe 'True' o 'False': ").strip().lower()
            if answer in ['true', 'false']:
                is_correct = self.check_answer(answer == 'true')
                
                if self.immediate_feedback:
                    if is_correct:
                        print(Fore.GREEN + "¡Correcto!" + Style.RESET_ALL)
                    else:
                        correct_answer_text = "True" if self.correct_answer else "False"
                        print(Fore.RED + f"Incorrecto. La respuesta correcta era: {correct_answer_text}" + Style.RESET_ALL)
                
                return self.score_value if is_correct else 0  # Retorna puntaje según la respuesta
            else:
                print(Fore.RED + "Respuesta no válida. Por favor, responde con 'True' o 'False'." + Style.RESET_ALL)

