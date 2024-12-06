from .question_en import Question
from colorama import Fore, Style
import string

class MultipleChoiceQuestion(Question):
    def __init__(self, text, options, correct_answers, image=None, score_value=1.0, scoring_mode="partial_scoring",  immediate_feedback=False):
        super().__init__(text, correct_answers, image=image, score_value=score_value)
        self.options = options
        self.scoring_mode = scoring_mode  
        self.immediate_feedback = immediate_feedback  

    def display(self):
        print("\n" + Fore.CYAN + "🔢 Multiple Choice Question:" + Style.RESET_ALL)
        print(Fore.CYAN + f"Question points: {self.score_value} point(s)" + Style.RESET_ALL)
        print(Fore.YELLOW + self.text + Style.RESET_ALL)
        
        self.display_image()
        
        option_letters = list(string.ascii_lowercase)[:len(self.options)]
        for letter, option in zip(option_letters, self.options):
            print(f"  {letter}. {option}")

        while True:
            answer = input("Choose one or more options separated by commas (e.g., a,c): ").strip().lower()
            selected_answers = [ans.strip() for ans in answer.split(",")]
            
            if all(ans in option_letters for ans in selected_answers):
                selected_indexes = {option_letters.index(ans) for ans in selected_answers}
                correct_set = set(self.correct_answer)
                
                if self.scoring_mode == "partial_scoring":
                    return self.scoring_mode_puntuacion_parcial(selected_indexes, correct_set, option_letters)
                elif self.scoring_mode == "all_or_nothing":
                    return self.scoring_mode_todo_o_nada(selected_indexes, correct_set, option_letters)
                elif self.scoring_mode == "proportional_with_penalty":
                    return self.scoring_mode_proporcional_con_penalizacion(selected_indexes, correct_set, option_letters)
                elif self.scoring_mode == "full_bonus":
                    return self.scoring_mode_bonificacion_completa(selected_indexes, correct_set, option_letters)
            else:
                print(Fore.RED + "Invalid response. Please answer with valid letters separated by commas." + Style.RESET_ALL)

    def scoring_mode_puntuacion_parcial(self, selected_indexes, correct_set, option_letters):
        """Mode 1: Partial scoring, with 0 points if there are extra or incorrect answers."""
        score_fraction = len(correct_set.intersection(selected_indexes)) / len(correct_set)
        score = self.score_value * score_fraction
        if self.immediate_feedback:
            if score_fraction == 1:
                print(Fore.GREEN + "Correct!" + Style.RESET_ALL)
            elif score_fraction > 0:
                print(Fore.YELLOW + "You answered partially correct." + Style.RESET_ALL)
            else:
                correct_answers_text = ", ".join([f"{option_letters[i]}. {self.options[i]}" for i in correct_set])
                print(Fore.RED + f"Incorrect. The correct answers were: {correct_answers_text}" + Style.RESET_ALL)
        return score

    def scoring_mode_todo_o_nada(self, selected_indexes, correct_set, option_letters):
        """Mode 2: All or nothing. Total accuracy is needed to score points."""
        is_correct = selected_indexes == correct_set
        if self.immediate_feedback:
            if is_correct:
                print(Fore.GREEN + "Correct!" + Style.RESET_ALL)
            else:
                correct_answers_text = ", ".join([f"{option_letters[i]}. {self.options[i]}" for i in correct_set])
                print(Fore.RED + f"Incorrect. The correct answers were: {correct_answers_text}" + Style.RESET_ALL)
        return self.score_value if is_correct else 0

    def scoring_mode_proporcional_con_penalizacion(self, selected_indexes, correct_set, option_letters):
        """
        Mode 3: Proportional points for each correct answer, with a smaller penalty for incorrect answers.
        """
        # Calculate intersections and fractions
        correct_intersections = correct_set.intersection(selected_indexes)
        incorrect_answers = selected_indexes - correct_set
        correct_fraction = len(correct_intersections) / len(correct_set) if correct_set else 0
        incorrect_fraction = len(incorrect_answers) / len(self.options) if self.options else 0
        
        # Calculate score with proportional penalties
        score = (self.score_value * correct_fraction) - (self.score_value * incorrect_fraction * 0.5)
        score = max(score, 0)  # Ensure score is not negative
        
        # Immediate feedback if enabled
        if self.immediate_feedback:
            if score == self.score_value:
                print(Fore.GREEN + "Correct!" + Style.RESET_ALL)
            elif score > 0:
                print(Fore.YELLOW + "You answered partially correct." + Style.RESET_ALL)
            else:
                correct_answers_text = ", ".join([f"{option_letters[i]}. {self.options[i]}" for i in correct_set])
                print(Fore.RED + f"Incorrect. The correct answers were: {correct_answers_text}" + Style.RESET_ALL)
        
        return score


    def scoring_mode_bonificacion_completa(self, selected_indexes, correct_set, option_letters):
        """Mode 4: Bonus for complete correctness with moderate penalty for errors."""
        correct_intersections = correct_set.intersection(selected_indexes)
        incorrect_answers = selected_indexes - correct_set
        total_correct = len(correct_set)
        num_correct_selected = len(correct_intersections)
        
        if num_correct_selected == total_correct and len(incorrect_answers) == 0:
            score = self.score_value * 1.1
            if self.immediate_feedback:
                print(Fore.GREEN + "Perfect! You got all the answers correct." + Style.RESET_ALL)
        elif num_correct_selected > 0 and len(incorrect_answers) < num_correct_selected:
            correct_fraction = num_correct_selected / total_correct
            penalty = len(incorrect_answers) * (self.score_value * 0.2 / total_correct)
            score = (self.score_value * correct_fraction) - penalty
            score = max(score, 0)
            if self.immediate_feedback:
                print(Fore.YELLOW + "You answered partially correct with some errors." + Style.RESET_ALL)
        else:
            score = 0
            if self.immediate_feedback:
                correct_answers_text = ", ".join([f"{option_letters[i]}. {self.options[i]}" for i in correct_set])
                print(Fore.RED + f"Incorrect. The correct answers were: {correct_answers_text}" + Style.RESET_ALL)
        
        return score