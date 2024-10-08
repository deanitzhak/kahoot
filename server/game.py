import json
import time
import random
from questions import get_regular_questions, get_math_questions, get_science_questions, get_history_questions, get_sports_questions, get_movies_questions, get_geography_questions

class PlayerGame:
    def __init__(self, player_id, question_type='both'):
        self.player_id = player_id
        self.current_question = 0
        self.score = 0
        self.last_answer = None  
        self.questions = self.generate_questions(question_type)

    # generate a list of questions based on the specified type
    def generate_questions(self, question_type):
        regular_questions = get_regular_questions()
        math_questions = get_math_questions()
        science_questions = get_science_questions()
        history_questions = get_history_questions()
        sports_questions = get_sports_questions()
        movies_questions = get_movies_questions()
        geography_questions = get_geography_questions()

        if question_type == 'math':
            return random.sample(math_questions, min(len(math_questions), 5))
        elif question_type == 'regular':
            return random.sample(regular_questions, min(len(regular_questions), 5))
        elif question_type == 'science':
            return random.sample(science_questions, min(len(science_questions), 5))
        elif question_type == 'history':
            return random.sample(history_questions, min(len(history_questions), 5))
        elif question_type == 'sports':
            return random.sample(sports_questions, min(len(sports_questions), 5))
        elif question_type == 'movies':
            return random.sample(movies_questions, min(len(movies_questions), 5))
        elif question_type == 'geography':
            return random.sample(geography_questions, min(len(geography_questions), 5))
        else: 
            all_questions = regular_questions + math_questions + science_questions + history_questions + sports_questions + movies_questions + geography_questions
            return random.sample(all_questions, 5)

    # get the current question for the player
    def get_current_question(self):
        if self.current_question < len(self.questions):
            return self.questions[self.current_question]
        return None

    # handle the player's answer and update the score
    def answer_question(self, answer):
        if self.current_question < len(self.questions):
            self.last_answer = answer  
            correct_answer = self.questions[self.current_question]['correct_answer']
            if answer == correct_answer:
                self.score += 1
            self.current_question += 1
            return self.current_question < len(self.questions)
        return False

    def get_last_answer(self):
        return self.last_answer  

    def get_score(self):
        return self.score

class QuizGame:
    def __init__(self):
        self.players = {}
        self.max_players = 5

    # add a new player to the game
    def add_player(self, player_id, question_type='both'):
        if len(self.players) < self.max_players:
            self.players[player_id] = PlayerGame(player_id, question_type)
            return True
        return False

    # remove a player from the game
    def remove_player(self, player_id):
        if player_id in self.players:
            del self.players[player_id]

    # get the current question for a specific player
    def get_question(self, player_id):
        if player_id in self.players:
            return self.players[player_id].get_current_question()
        return None

    # handle the answer for a specific player
    def handle_answer(self, player_id, answer):
        if player_id in self.players:
            return self.players[player_id].answer_question(answer)
        return False

    # get the score for a specific player
    def get_player_score(self, player_id):
        if player_id in self.players:
            return self.players[player_id].get_score()
        return 0

    # get the last answer for a specific player
    def get_player_last_answer(self, player_id):
        if player_id in self.players:
            return self.players[player_id].get_last_answer()
        return None

    # get the scores for all players
    def get_all_scores(self):
        return {player_id: player.get_score() for player_id, player in self.players.items()}
