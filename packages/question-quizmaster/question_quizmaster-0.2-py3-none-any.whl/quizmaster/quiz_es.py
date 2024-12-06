from colorama import Fore, Style

class Quiz:
    def __init__(self, questions, inmediate_feedback=False):
        self.questions = questions
        self.score = 0
        self.question_scores = []  # Lista para almacenar el puntaje de cada pregunta
        self.inmediate_feedback = inmediate_feedback  # Nuevo parámetro para el feedback inmediato

    def start(self):
        print(Fore.MAGENTA + Style.BRIGHT + "¡Bienvenido a QuizMaster!" + Style.RESET_ALL)

        for i, question in enumerate(self.questions, start=1):
            print("\n" + Fore.CYAN + "-------------------------------" + Style.RESET_ALL)
            score_for_question = question.display()  # Este valor puede ser parcial o completo
            self.score += score_for_question  # Suma la puntuación total parcial o completa
            
            # Verificar si la pregunta tiene opciones y obtener la respuesta correcta
            options = getattr(question, "options", None)  # Devuelve None si no existe
            
            # Manejar respuestas correctas según el tipo de pregunta
            correct_answer = question.correct_answer
            if isinstance(correct_answer, (list, set)):  # Para múltiples respuestas correctas
                correct_set = set(correct_answer)
                correct_answers_text = ", ".join([options[i] for i in correct_set])
            else:  # Para preguntas con una sola respuesta correcta
                correct_answers_text = options[correct_answer] if options else correct_answer

            # Guardar la información de cada pregunta
            self.question_scores.append((question.text, score_for_question, question.score_value, options, correct_answers_text))

        total_possible_score = sum(q.score_value for q in self.questions)  # Cada pregunta tiene un valor en puntos
        percentage_score = (self.score / total_possible_score) * 100

        print("\n")
        print(Fore.MAGENTA + "===============================" + Style.RESET_ALL)
        print(Fore.MAGENTA + f"Tu puntuación final es: {self.score:.2f}/{total_possible_score:.2f} ({percentage_score:.1f}%)" + Style.RESET_ALL)
        print(Fore.MAGENTA + "===============================" + Style.RESET_ALL)

        # Mostrar desglose de puntuación por pregunta
        print(Fore.CYAN + "\nDesglose de puntuación por pregunta:" + Style.RESET_ALL)
        for i, (text, score, total, options, correct_answers_text) in enumerate(self.question_scores, start=1):
            print(f"Pregunta {i}: {text}")
            if options:  # Si hay opciones, imprimir las opciones correctas
                print(f"  Respuestas correctas: {correct_answers_text}")
            else:  # Si no hay opciones, imprimir directamente la respuesta
                print(f"  Respuesta correcta: {correct_answers_text}")
            print(f"  Puntuación obtenida: {score}/{total} puntos\n")

        # Retroalimentación personalizada basada en el puntaje
        if percentage_score == 100:
            print(Fore.GREEN + "¡Excelente trabajo! Dominas el tema." + Style.RESET_ALL)
        elif percentage_score >= 80:
            print(Fore.YELLOW + "¡Buen trabajo! Sigue así." + Style.RESET_ALL)
        elif percentage_score >= 50:
            print(Fore.YELLOW + "Necesitas repasar algunos conceptos." + Style.RESET_ALL)
        else:
            print(Fore.RED + "No te desanimes, sigue practicando." + Style.RESET_ALL)
