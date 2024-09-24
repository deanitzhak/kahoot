# math_questions.py
import random

def generate_addition_question():
    num1 = random.randint(1, 100)
    num2 = random.randint(1, 100)
    return {
        "question": f"What is {num1} + {num2}?",
        "answers": [str(num1 + num2), 
                    str(num1 + num2 + random.randint(1, 5)), 
                    str(num1 + num2 - random.randint(1, 5)), 
                    str(num1 + num2 + random.randint(5, 10))],
        "correct_answer": str(num1 + num2),
        "time_limit": 15
    }

def generate_subtraction_question():
    num1 = random.randint(50, 100)
    num2 = random.randint(1, 50)
    return {
        "question": f"What is {num1} - {num2}?",
        "answers": [str(num1 - num2), 
                    str(num1 - num2 + random.randint(1, 5)), 
                    str(num1 - num2 - random.randint(1, 5)), 
                    str(num1 - num2 + random.randint(5, 10))],
        "correct_answer": str(num1 - num2),
        "time_limit": 15
    }

def generate_multiplication_question():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    return {
        "question": f"What is {num1} x {num2}?",
        "answers": [str(num1 * num2), 
                    str(num1 * num2 + random.randint(1, 5)), 
                    str(num1 * num2 - random.randint(1, 5)), 
                    str(num1 * num2 + random.randint(5, 10))],
        "correct_answer": str(num1 * num2),
        "time_limit": 15
    }

def generate_division_question():
    num1 = random.randint(10, 100)
    num2 = random.randint(1, 10)
    correct_answer = num1 // num2  # Ensuring integer division
    return {
        "question": f"What is {num1} ÷ {num2}?",
        "answers": [str(correct_answer), 
                    str(correct_answer + random.randint(1, 3)), 
                    str(correct_answer - random.randint(1, 3)), 
                    str(correct_answer + random.randint(3, 6))],
        "correct_answer": str(correct_answer),
        "time_limit": 15
    }

def get_basic_math_questions(num_questions=150):
    questions = []
    while len(questions) < num_questions:
        question_type = random.choice([
            generate_addition_question, 
            generate_subtraction_question, 
            generate_multiplication_question, 
            generate_division_question
        ])
        questions.append(question_type())
    return questions

# Example usage:
# print(get_basic_math_questions(150))
