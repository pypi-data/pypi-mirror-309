# QuizMaster

**QuizMaster** is a library designed to create and manage interactive quizzes in Python. It provides flexible tools to implement different types of questions, calculate scores, and provide detailed feedback to the user. Its modular design allows for easy addition of new functionalities.

## Main Features

- **Support for multiple question types:**

  - Multiple-choice (with several correct answers).
  - Single-choice.
  - True/False.
  - Short answer.

- **Advanced scoring methods(Only in multiple choice):**

  - Partial scoring.
  - All-or-nothing.
  - Proportional with penalty.
  - Full bonus.

- **Question management:**

  - Validation and normalization of answers.
  - Images associated with questions.
  - Automatic feedback based on performance.

- **Customizable feedback:**

  - Detailed scores and specific feedback for each question.
  - Option to display feedback after each question or at the end of the quiz.

## Main Functions

| **Function**             | **Description**                                             |
|--------------------------|-------------------------------------------------------------|
| `start()`                | Starts the quiz and calculates the scores.                  |
| `calculate_score()`      | Calculates the total score based on the answers.            |
| `normalize_text(text)`   | Normalizes text by removing special characters and accents. |
| `display_feedback()`     | Personalized feedback based on correct answers.             |

## Question Management

- **`display()`**  
  Displays a question to the user and interprets their response. Implemented in the specific classes for each question type.

- **`check_answer(answer)`**  
  Verifies if the user's answer is correct. Returns `True` or `False`.

- **`get_correct_answer_text()`**  
  Returns the correct answer in text format.

- **`display_image()`**  
  Displays an image associated with the question (if available).

## Advanced Scoring

- **`partial_scoring`**  
  Grants proportional points based on the correct answers selected. Penalizes errors.

- **`all_or_nothing`**  
  Assigns points only if all correct answers are selected and there are no errors.

- **`proportional_with_penalty`**  
  Calculates the score proportionally, subtracting points for incorrect answers.

- **`full_bonus`**  
  Awards extra points for completely correct answers and partially penalizes errors.

## Answer Normalization

- **`normalize_text(text)`**  
  Converts text to lowercase, removes accents and special characters to perform comparisons insensitive to formatting errors.

## Supported Question Types

### Arguments

- **`text`:** The statement or text of the question to be displayed to the user.
- **`options`:** A list of answer options from which the user can choose, True/False for binary questions, or a string for short answers.
- **`correct_answer`:** A list of indices of the correct answers in the options list (indices start at 0).
- **`score_value`** (optional): Defines the point value awarded if the answer is correct. Default is `1`.
- **`immediate_feedback`** (optional): Indicates whether immediate feedback should be provided after the user's response (`True` or `False`). Default is `False`.

- **`scoring_mode`** (optional only in multiple choice): Defines the scoring method to use (`partial_scoring`, `all_or_nothing`, `proportional_with_penalty`, `full_bonus`). Default is `partial_scoring`.

### Multiple Choice (MultipleChoiceQuestion)

Allows selecting multiple correct answers.

#### Example

```python
        q1 = MultipleChoiceQuestion(text = "Which are planets?", 
                                    options = ["Sun", "Earth", "Moon", "Mars"], 
                                    correct_answers = [1, 3], 
                                    score_value = 3, 
                                    scoring_mode = "partial_scoring", 
                                    immediate_feedback = False)

```

### Single Choice (SingleChoiceQuestion)

Allows selecting only one correct option.

#### Example

```python
        q2 = SingleChoiceQuestion(text = "What is the capital of England?",
                                  options = ["Paris", "London", "Berlin", "Rome"],
                                  correct_answer = 1,
                                  score_value = 2,
                                  immediate_feedback = True)
```

### True/False (TrueFalseQuestion)
Questions with binary responses (True/False).

#### Example

```python
        q3 = TrueFalseQuestion(text = "The Earth is flat.", 
                                correct_answer = False, 
                                score_value = 0.5, 
                                immediate_feedback = False)
```

### Short Answer (ShortAnswerQuestion)
Requires the user to input a text answer.

#### Example

```python
        q4 = ShortAnswerQuestion(text = "What is the capital of France?", 
                                  correct_answer = "Paris", 
                                  score_value = 1, 
                                  immediate_feedback = True)
```

## Usage

```python
    from quizmaster.quiz_en import Quiz
    from quizmaster.quiz_en import MultipleChoiceQuestion
    from quizmaster.quiz_en import SingleChoiceQuestion
    from quizmaster.quiz_en import TrueFalseQuestion
    from quizmaster.quiz_en import ShortAnswerQuestion

    # Create quiz
    quiz = Quiz(questions = [q1, q2, q3, q4])

    # Start quiz
    quiz.start()
```
