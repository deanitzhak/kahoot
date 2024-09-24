import random
from math_questions import get_basic_math_questions

class MathPlayerGame:
    def __init__(self, player_id):
        self.player_id = player_id
        self.current_question = 0
        self.score = 0
        self.questions = self.generate_questions()

    def generate_questions(self):
        return get_basic_math_questions(5)  # Generate 5 questions

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

    def start_new_game(self):
        self.questions = self.generate_questions()  # Reload new questions
        self.current_question = 0  # Reset the question index
        self.score = 0  # Reset score


class MathQuizGame:
    def __init__(self):
        self.players = {}
        self.max_players = 5

    def add_player(self, player_id):
        if len(self.players) < self.max_players:
            self.players[player_id] = MathPlayerGame(player_id)
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

# Example usage
if __name__ == "__main__":
    game = MathQuizGame()
    
    # Adding players
    game.add_player("Player1")
    game.add_player("Player2")
    
    # Game loop for 5 rounds of questions
    for round in range(5):  # 5 rounds
        for player_id in game.players.keys():
            question = game.get_question(player_id)
            if question:
                print(f"{player_id}, {question['question']}")
                print("Options:", ', '.join(question['answers']))
                answer = input("Your answer: ")
                game.handle_answer(player_id, answer)

    # Display scores
    scores = game.get_all_scores()
    for player_id, score in scores.items():
        print(f"{player_id} scored {score} points.")
