from colorama import Fore, Style, init
from quizmaster.quiz_es import Quiz
from quizmaster.single_choice_question_es import SingleChoiceQuestion
from quizmaster.multiple_choice_question_es import MultipleChoiceQuestion
from quizmaster.true_false_question_es import TrueFalseQuestion
from quizmaster.short_answer_question_es import ShortAnswerQuestion

def main():
    init(autoreset=True)

    # Crear instancias de preguntas
    q1 = SingleChoiceQuestion("¿Cuál es la capital de Inglaterra?", ["París", "Londres", "Berlín", "Roma"], 1, score_value=2, immediate_feedback=True)
    q2 = MultipleChoiceQuestion("¿Cuáles son planetas?", ["Sol", "Tierra", "Luna", "Marte"], [1, 3], score_value=3, scoring_mode="partial_scoring", immediate_feedback=False)
    q3 = TrueFalseQuestion("La Tierra es plana.", False, score_value=0.5, immediate_feedback=False)
    q4 = ShortAnswerQuestion("¿En qué año llegó el hombre a la luna?", "1969", immediate_feedback=False)
    q5 = ShortAnswerQuestion("¿Qué monumento es el que aparece en la imagen?", "Torre Eiffel", image="./images/torre.jpg", immediate_feedback=False)
    q6 = MultipleChoiceQuestion("¿Cuáles son colores primarios?", ["Rojo", "Verde", "Azul", "Amarillo"], [0, 2, 3], score_value=3, scoring_mode="partial_scoring", immediate_feedback=False)
    q7 = TrueFalseQuestion("¿Asierlo tiene barba?", True, score_value=0.5, immediate_feedback=False)
    q8 = SingleChoiceQuestion("¿Cuál es la capital de España?", ["París", "Londres", "Berlín", "Madrid"], 3, score_value=2, immediate_feedback=False)
    q9 = MultipleChoiceQuestion("¿Qúe equipos son vascos?", ["Athletic", "Real Madrid", "Barcelona", "Real Sociedad", "Betis"], [0, 3], score_value=2, scoring_mode="full_bonus", immediate_feedback=False)
    q10 = ShortAnswerQuestion("¿Cuántos equipos hay en la liga española?", "20", immediate_feedback=False)


    # Crear cuestionario
    quiz = Quiz([q1, q2, q3, q4, q5, q6, q7, q8, q9, q10])

    quiz.start()

# Ejecutar main solo si este archivo es el punto de entrada
if __name__ == '__main__':
    main()
