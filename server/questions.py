import random

def get_regular_questions():
    return [
        {
            "question": "What's the capital of France?",
            "answers": ["Paris", "London", "Berlin", "Madrid"],
            "correct_answer": "Paris",
            "time_limit": 15
        },
        {
            "question": "Who painted the Mona Lisa?",
            "answers": ["Leonardo da Vinci", "Vincent van Gogh", "Pablo Picasso", "Claude Monet"],
            "correct_answer": "Leonardo da Vinci",
            "time_limit": 15
        },
        {
            "question": "What's the largest planet in our solar system?",
            "answers": ["Jupiter", "Earth", "Saturn", "Mars"],
            "correct_answer": "Jupiter",
            "time_limit": 15
        },
        {
            "question": "What is the chemical symbol for gold?",
            "answers": ["Au", "Ag", "Pb", "Fe"],
            "correct_answer": "Au",
            "time_limit": 15
        },
        {
            "question": "Who wrote 'To Kill a Mockingbird'?",
            "answers": ["Harper Lee", "Mark Twain", "Ernest Hemingway", "J.D. Salinger"],
            "correct_answer": "Harper Lee",
            "time_limit": 15
        }
    ]

def get_math_questions():
    math_questions = []
    for _ in range(5):  
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        math_questions.append({
            "question": f"What is {num1} x {num2}?",
            "answers": [str(num1 * num2), str(num1 * num2 - 1), str(num1 * num2 + 1), str(num1 * num2 + 2)],
            "correct_answer": str(num1 * num2),
            "time_limit": 15
        })
    return math_questions


def get_science_questions():
    return [
        {
            "question": "What is the symbol for water?",
            "answers": ["H2O", "O2", "CO2", "N2"],
            "correct_answer": "H2O",
            "time_limit": 15
        },
        {
            "question": "What planet is known as the Red Planet?",
            "answers": ["Mars", "Jupiter", "Venus", "Saturn"],
            "correct_answer": "Mars",
            "time_limit": 15
        }
    ]

def get_history_questions():
    return [
        {
            "question": "Who was the first president of the United States?",
            "answers": ["George Washington", "Abraham Lincoln", "Thomas Jefferson", "John Adams"],
            "correct_answer": "George Washington",
            "time_limit": 15
        },
        {
            "question": "In what year did World War II end?",
            "answers": ["1945", "1939", "1918", "1963"],
            "correct_answer": "1945",
            "time_limit": 15
        }
    ]

def get_sports_questions():
    return [
        {
            "question": "How many players are on a football (soccer) team?",
            "answers": ["11", "9", "10", "12"],
            "correct_answer": "11",
            "time_limit": 15
        },
        {
            "question": "In which country were the first Olympic Games held?",
            "answers": ["Greece", "Italy", "France", "Spain"],
            "correct_answer": "Greece",
            "time_limit": 15
        }
    ]

def get_movies_questions():
    return [
        {
            "question": "Who directed the movie 'Inception'?",
            "answers": ["Christopher Nolan", "Steven Spielberg", "James Cameron", "Quentin Tarantino"],
            "correct_answer": "Christopher Nolan",
            "time_limit": 15
        },
        {
            "question": "Which movie won the Best Picture Oscar in 2020?",
            "answers": ["Parasite", "1917", "Joker", "Ford v Ferrari"],
            "correct_answer": "Parasite",
            "time_limit": 15
        }
    ]

def get_geography_questions():
    return [
        {
            "question": "Which is the largest continent by land area?",
            "answers": ["Asia", "Africa", "North America", "Europe"],
            "correct_answer": "Asia",
            "time_limit": 15
        },
        {
            "question": "What is the longest river in the world?",
            "answers": ["Nile", "Amazon", "Yangtze", "Mississippi"],
            "correct_answer": "Nile",
            "time_limit": 15
        }
    ]
