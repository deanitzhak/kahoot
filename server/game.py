import json
import time
import random

class PlayerGame:
    def __init__(self, player_id):
        self.player_id = player_id
        self.current_question = 0
        self.score = 0
        self.questions = self.generate_questions()

    def generate_questions(self):
        all_questions = [
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
        return random.sample(all_questions, 5)  # Randomly select 5 questions

    def get_current_question(self):
        if self.current_question < len(self.questions):
            return self.questions[self.current_question]
        return None

    def answer_question(self, answer):
        if self.current_question < len(self.questions):
            correct_answer = self.questions[self.current_question]['correct_answer']
            if answer == correct_answer:
                self.score += 1
            self.current_question += 1
            return self.current_question < len(self.questions)
        return False

    def get_score(self):
        return self.score

class QuizGame:
    def __init__(self):
        self.players = {}
        self.max_players = 5

    def add_player(self, player_id):
        if len(self.players) < self.max_players:
            self.players[player_id] = PlayerGame(player_id)
            return True
        return False

    def remove_player(self, player_id):
        if player_id in self.players:
            del self.players[player_id]

    def get_question(self, player_id):
        if player_id in self.players:
            return self.players[player_id].get_current_question()
        return None

    def handle_answer(self, player_id, answer):
        if player_id in self.players:
            return self.players[player_id].answer_question(answer)
        return False

    def get_player_score(self, player_id):
        if player_id in self.players:
            return self.players[player_id].get_score()
        return 0

    def get_all_scores(self):
        return {player_id: player.get_score() for player_id, player in self.players.items()}