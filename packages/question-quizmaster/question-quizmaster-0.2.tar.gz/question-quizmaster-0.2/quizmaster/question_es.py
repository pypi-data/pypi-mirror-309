from colorama import Fore, Style
from PIL import Image

class Question:
    def __init__(self, text, correct_answer, image=None, score_value=1,  immediate_feedback=False):
        self.text = text
        self.correct_answer = correct_answer
        self.image = image  # Ruta de la imagen opcional
        self.score_value = score_value  # Valor en puntos de la pregunta

    def check_answer(self, answer):
        return answer == self.correct_answer

    def display_image(self):
        if self.image:
            try:
                # Intentar abrir la imagen en el visor de imágenes del sistema
                img = Image.open(self.image)
                img.show()  # Abre la imagen en una ventana emergente
            except Exception as e:
                print(Fore.RED + f"Error al cargar la imagen: {e}" + Style.RESET_ALL)

