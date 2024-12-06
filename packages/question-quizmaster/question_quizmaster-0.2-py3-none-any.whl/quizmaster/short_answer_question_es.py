from .question_es import Question
from colorama import Fore, Style
import unicodedata


class ShortAnswerQuestion(Question):
    def __init__(self, text, correct_answer, image=None, score_value=1, immediate_feedback=False):
        super().__init__(text, correct_answer, image=image, score_value=score_value)
        self.immediate_feedback = immediate_feedback

    def normalize_text(self, text):
        """Convierte el texto a minúsculas y elimina tildes y caracteres especiales."""
        text = text.lower()  # Convertir a minúsculas
        text = unicodedata.normalize('NFKD', text)  # Normalizar caracteres
        text = "".join([c for c in text if not unicodedata.combining(c)])  # Eliminar tildes
        return text

    def check_answer(self, answer):
        # Normalizar tanto la respuesta correcta como la respuesta del usuario
        return self.normalize_text(answer) == self.normalize_text(self.correct_answer)

    def display(self):
        print("\n" + Fore.CYAN + "✏️ Pregunta de Respuesta Corta:" + Style.RESET_ALL)
        print(Fore.CYAN + f"Puntos de la pregunta: {self.score_value} punto(s)" + Style.RESET_ALL)
        print(Fore.YELLOW + self.text + Style.RESET_ALL)
        
        self.display_image()
        
        answer = input("Escribe tu respuesta: ")
        is_correct = self.check_answer(answer)
        
        if self.immediate_feedback:
            if is_correct:
                print(Fore.GREEN + "¡Correcto!" + Style.RESET_ALL)
            else:
                print(Fore.RED + f"Incorrecto. La respuesta correcta era: {self.correct_answer}" + Style.RESET_ALL)
        
        return self.score_value if is_correct else 0
