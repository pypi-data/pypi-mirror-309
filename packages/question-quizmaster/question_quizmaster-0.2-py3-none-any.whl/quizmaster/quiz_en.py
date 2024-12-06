from colorama import Fore, Style

class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.score = 0
        self.question_scores = []  # List to store the score of each question

    def start(self):
        
        print(Fore.MAGENTA + Style.BRIGHT + "Welcome to QuizMaster!" + Style.RESET_ALL)

        for i, question in enumerate(self.questions, start=1):
            print("\n" + Fore.CYAN + "-------------------------------" + Style.RESET_ALL)
            score_for_question = question.display()  # This value can be partial or complete
            self.score += score_for_question  # Adds the total partial or complete score
            options = getattr(question, "options", None)  # Devuelve None si no existe
            
            # Manejar respuestas correctas según el tipo de pregunta
            correct_answer = question.correct_answer
            if isinstance(correct_answer, (list, set)):  # Para múltiples respuestas correctas
                correct_set = set(correct_answer)
                correct_answers_text = ", ".join([options[i] for i in correct_set])
            else:  # Para preguntas con una sola respuesta correcta
                correct_answers_text = options[correct_answer] if options else correct_answer

            # Store each question's score along with the question text
            self.question_scores.append((question.text, score_for_question, question.score_value, options, correct_answers_text))

        total_possible_score = sum(q.score_value for q in self.questions)  # Each question has a point value
        percentage_score = (self.score / total_possible_score) * 100

        print("\n")
        print(Fore.MAGENTA + "===============================" + Style.RESET_ALL)
        print(Fore.MAGENTA + f"Your final score is: {self.score:.2f}/{total_possible_score:.2f} ({percentage_score:.1f}%)" + Style.RESET_ALL)
        print(Fore.MAGENTA + "===============================" + Style.RESET_ALL)

        # Display score breakdown by question
        for i, (text, score, total, options, correct_answers_text) in enumerate(self.question_scores, start=1):
            print(f"Question {i}: {text}")
            if options:  # Si hay opciones, imprimir las opciones correctas
                print(f"  Correct answer: {correct_answers_text}")
            else:  # Si no hay opciones, imprimir directamente la respuesta
                print(f"  Correct answer: {correct_answers_text}")
            print(f"  Obtained score: {score}/{total} puntos\n")

        # Custom feedback based on the score
        if percentage_score == 100:
            print(Fore.GREEN + "Excellent work! You master the subject." + Style.RESET_ALL)
        elif percentage_score >= 80:
            print(Fore.YELLOW + "Good job! Keep it up." + Style.RESET_ALL)
        elif percentage_score >= 50:
            print(Fore.YELLOW + "You need to review some concepts." + Style.RESET_ALL)
        else:
            print(Fore.RED + "Don't be discouraged, keep practicing." + Style.RESET_ALL)
