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
    # Randomly choose how many terms (2 or 3 terms for multiplication)
    num_terms = random.choice([2, 3])
    
    # Generate random integers between -10 and 10, including -1 for negative numbers
    numbers = [random.randint(-10, 10) for _ in range(num_terms)]

    # Ensure no zeroes in the numbers
    numbers = [n if n != 0 else 1 for n in numbers]

    # Generate the multiplication question string
    question = " * ".join(map(str, numbers))
    
    # Calculate the correct answer
    correct_answer = 1
    for num in numbers:
        correct_answer *= num

    return {
        "question": f"What is {question}?",
        "answers": [str(correct_answer), 
                    str(correct_answer + random.randint(1, 5)), 
                    str(correct_answer - random.randint(1, 5)), 
                    str(correct_answer + random.randint(5, 10))],
        "correct_answer": str(correct_answer),
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
    question_types = [
        generate_addition_question, 
        generate_subtraction_question, 
        generate_multiplication_question, 
        generate_division_question
    ]
    
    # Weights for how frequently each question type should appear
    weights = [1, 1, 5, 1]  # Multiplication has a higher weight (5x more likely)
    
    while len(questions) < num_questions:
        question_type = random.choices(question_types, weights=weights)[0]
        questions.append(question_type())
    return questions
