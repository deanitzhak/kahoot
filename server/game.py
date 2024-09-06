import json
import time

class QuizGame:
    def __init__(self):
        self.clients = []  # List of client sockets
        self.client_answers = {}  # Dictionary to track client answers
        self.quizzes = self.load_quizzes()
        self.current_question = 0

    def load_quizzes(self):
        # Implement loading quizzes with multiple choices for each question
        return {
            "general": [
                {
                    "question": "What's the capital of France?",
                    "answers": ["Paris", "London", "Berlin", "Madrid"],
                    "correct_answer": "Paris",
                    "time_limit": 10
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
                    "time_limit": 12
                },
                {
                    "question": "What is the chemical symbol for gold?",
                    "answers": ["Au", "Ag", "Pb", "Fe"],
                    "correct_answer": "Au",
                    "time_limit": 10
                },
                {
                    "question": "Who wrote 'To Kill a Mockingbird'?",
                    "answers": ["Harper Lee", "Mark Twain", "Ernest Hemingway", "J.D. Salinger"],
                    "correct_answer": "Harper Lee",
                    "time_limit": 15
                }
            ]
        }

    def broadcast(self, message):
        for client in self.clients:
            try:
                client.send(json.dumps(message).encode('utf-8'))
            except OSError as e:
                print(f"Error sending message to client {client.getpeername()}: {e}")
                self.clients.remove(client)
                client.close()

    def start(self):
        while self.current_question < len(self.quizzes['general']):
            question = self.quizzes['general'][self.current_question]
            self.broadcast({
                'type': 'question',
                'question': question['question'],
                'answers': question['answers'],
                'time_limit': question['time_limit']
            })
            time.sleep(question['time_limit'])  # Wait for the question time limit
            self.current_question += 1
        self.end_game()

    def end_game(self):
        # Calculate scores
        results = {}
        for client, answers in self.client_answers.items():
            score = sum(
                1 for q_index, answer in answers.items()
                if self.quizzes['general'][q_index]['correct_answer'] == answer
            )
            results[client.getpeername()] = score

        # Send results to clients
        for client in self.clients:
            try:
                client.send(json.dumps({
                    'type': 'results',
                    'message': 'Quiz completed',
                    'results': results
                }).encode('utf-8'))
            except OSError as e:
                print(f"Error sending results to client {client.getpeername()}: {e}")
                self.clients.remove(client)
                client.close()

        print("Quiz ended. Final results sent to all clients.")

    def handle_answer(self, client_socket, data):
        # Handle client answer
        client_address = client_socket.getpeername()
        if client_address not in self.client_answers:
            self.client_answers[client_address] = {}

        answer_data = json.loads(data)
        question_index = answer_data.get('question_index')
        answer = answer_data.get('answer')

        if question_index is not None and answer:
            self.client_answers[client_address][question_index] = answer
            print(f"Client {client_address} answered question {question_index} with {answer}")
