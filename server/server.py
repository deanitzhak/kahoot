# server.py

import socket
import threading
import json
from game import QuizGame

class QuizServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.quiz_game = QuizGame()
        print(f"Server listening on {self.host}:{self.port}")

    def handle_client(self, client_socket):
        try:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                return

            headers = request.split('\n')
            method, path, _ = headers[0].split(' ')
            
            if method == 'OPTIONS':
                response_header = 'HTTP/1.1 200 OK\r\n'
                response_header += 'Access-Control-Allow-Origin: *\r\n'
                response_header += 'Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n'
                response_header += 'Access-Control-Allow-Headers: Content-Type\r\n'
                response_header += 'Content-Length: 0\r\n\r\n'
                client_socket.sendall(response_header.encode('utf-8'))
                return

            if method == 'GET':
                if path == '/get_question':
                    if self.quiz_game.current_question < len(self.quiz_game.quizzes['general']):
                        question = self.quiz_game.quizzes['general'][self.quiz_game.current_question]
                        response = {
                            'type': 'question',
                            'question': question['question'],
                            'answers': question['answers'],
                            'time_limit': question['time_limit']
                        }
                        response_body = json.dumps(response)
                        response_header = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n'
                        response_header += 'Access-Control-Allow-Origin: *\r\n\r\n'
                        print(f"Sending question to client: {response_body}")
                    else:
                        response = {'type': 'end', 'message': 'Quiz completed'}
                        response_body = json.dumps(response)
                        response_header = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n'
                        response_header += 'Access-Control-Allow-Origin: *\r\n\r\n'
                        print(f"Sending end-of-quiz message to client: {response_body}")
                    
                    client_socket.sendall(response_header.encode('utf-8') + response_body.encode('utf-8'))
                else:
                    response_body = '404 Not Found'
                    response_header = 'HTTP/1.1 404 Not Found\r\n\r\n'
                    response_header += 'Access-Control-Allow-Origin: *\r\n'
                    client_socket.sendall(response_header.encode('utf-8') + response_body.encode('utf-8'))
            elif method == 'POST':
                if path == '/submit_answer':
                    data = json.loads(request.split('\r\n\r\n')[1])
                    answer = data.get('answer')
                    print(f"Received answer from client: {answer}")

                    # Move to the next question after receiving an answer
                    self.quiz_game.current_question += 1

                    # Fetch the next question
                    if self.quiz_game.current_question < len(self.quiz_game.quizzes['general']):
                        next_question = self.quiz_game.quizzes['general'][self.quiz_game.current_question]
                        response = {
                            'type': 'question',
                            'question': next_question['question'],
                            'answers': next_question['answers'],
                            'time_limit': next_question['time_limit']
                        }
                        response_body = json.dumps(response)
                        response_header = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n'
                        response_header += 'Access-Control-Allow-Origin: *\r\n\r\n'
                        print(f"Sending next question to client: {response_body}")
                    else:
                        response = {'type': 'end', 'message': 'Quiz completed'}
                        response_body = json.dumps(response)
                        response_header = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n'
                        response_header += 'Access-Control-Allow-Origin: *\r\n\r\n'
                        print(f"Sending end-of-quiz message to client: {response_body}")

                    client_socket.sendall(response_header.encode('utf-8') + response_body.encode('utf-8'))
                else:
                    response_body = '404 Not Found'
                    response_header = 'HTTP/1.1 404 Not Found\r\n\r\n'
                    response_header += 'Access-Control-Allow-Origin: *\r\n'
                    client_socket.sendall(response_header.encode('utf-8') + response_body.encode('utf-8'))
            else:
                response_body = '405 Method Not Allowed'
                response_header = 'HTTP/1.1 405 Method Not Allowed\r\n\r\n'
                response_header += 'Access-Control-Allow-Origin: *\r\n'
                client_socket.sendall(response_header.encode('utf-8') + response_body.encode('utf-8'))

        except Exception as e:
            print(f"Exception handling client: {e}")
        finally:
            client_socket.close()

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"New connection from {addr}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

if __name__ == "__main__":
    server = QuizServer()
    server.start()
