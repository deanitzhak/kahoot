import json
import time

class QuizGame:
    def __init__(self):
        self.clients = []  # List of client sockets
        self.client_answers = {}  # Dictionary to track client answers
        self.quizzes = self.load_quizzes()
        self.current_question = 0
        self.results = {}  # Store final results

    def load_quizzes(self):
        # Implement loading quizzes with multiple choices for each question
        return {
            "general": [
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
        self.results = {}
        for client, answers in self.client_answers.items():
            score = sum(
                1 for q_index, answer in answers.items()
                if self.quizzes['general'][q_index]['correct_answer'] == answer
            )
            self.results[client.getpeername()] = score

        # Send results to clients
        for client in self.clients:
            try:
                client.send(json.dumps({
                    'type': 'results',
                    'message': 'Quiz completed',
                    'results': self.results
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

        try:
            print(f"Received data from client {client_address}: {data}")  # Debug print
            answer_data = json.loads(data)
            question_index = answer_data.get('question_index')
            answer = answer_data.get('answer')

            # Check if the question_index and answer are valid
            if question_index is not None and answer is not None:
                if 0 <= question_index < len(self.quizzes['general']):
                    correct_answer = self.quizzes['general'][question_index]['correct_answer']
                    # Store the answer
                    self.client_answers[client_address][question_index] = answer
                    
                    # Print for debugging
                    if answer == correct_answer:
                        print(f"Client {client_address} answered question {question_index} correctly with {answer}")
                    else:
                        print(f"Client {client_address} answered question {question_index} incorrectly with {answer}")
                else:
                    print(f"Invalid question index {question_index} from client {client_address}")
            else:
                print(f"Invalid answer data from client {client_address}: {data}")

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from client {client_address}: {e}")
        except Exception as e:
            print(f"Exception handling answer from client {client_address}: {e}")

    def get_score(self, player_address):
        # Return the score for a specific player by their address
        return self.results.get(player_address, 0)

    def get_scores(self):
        # Return scores for all players
        return self.results
