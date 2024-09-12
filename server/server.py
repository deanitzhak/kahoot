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
        print(f"Server listening on {self.host}:{self.port}")
        self.quiz_game = QuizGame()

    def handle_client(self, client_socket):
        print("Handling new client connection.")
        try:
            while True:
                request = client_socket.recv(1024).decode('utf-8')
                if not request:
                    print("No data received. Closing connection.")
                    break

                headers = request.split('\n')
                method, path, _ = headers[0].split(' ')

                if method == 'OPTIONS':
                    response_header = (
                        'HTTP/1.1 200 OK\r\n'
                        'Access-Control-Allow-Origin: *\r\n'
                        'Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n'
                        'Access-Control-Allow-Headers: Content-Type\r\n'
                        'Content-Length: 0\r\n'
                        'Connection: keep-alive\r\n\r\n'
                    )
                    client_socket.sendall(response_header.encode('utf-8'))
                    continue

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
                            response_header = (
                                'HTTP/1.1 200 OK\r\n'
                                'Content-Type: application/json\r\n'
                                f'Content-Length: {len(response_body)}\r\n'
                                'Access-Control-Allow-Origin: *\r\n'
                                'Connection: keep-alive\r\n\r\n'
                            )
                        else:
                            response = {'type': 'end', 'message': 'Quiz completed'}
                            response_body = json.dumps(response)
                            response_header = (
                                'HTTP/1.1 200 OK\r\n'
                                'Content-Type: application/json\r\n'
                                f'Content-Length: {len(response_body)}\r\n'
                                'Access-Control-Allow-Origin: *\r\n'
                                'Connection: keep-alive\r\n\r\n'
                            )
                        client_socket.sendall(response_header.encode('utf-8') + response_body.encode('utf-8'))
                    
                    else:
                        response_body = '404 Not Found'
                        response_header = (
                            'HTTP/1.1 404 Not Found\r\n'
                            f'Content-Length: {len(response_body)}\r\n'
                            'Access-Control-Allow-Origin: *\r\n'
                            'Connection: keep-alive\r\n\r\n'
                        )
                        client_socket.sendall(response_header.encode('utf-8') + response_body.encode('utf-8'))

                elif method == 'POST':
                    if path == '/submit_answer':
                        try:
                            # Extract the body of the request (after the headers)
                            body_start = request.find('\r\n\r\n') + 4
                            body = request[body_start:]
                            
                            # Parse the JSON data from the body
                            data = json.loads(body)
                            answer = data.get('answer')
                            print(f"Received answer from client: {answer}")

                            # Handle the answer
                            self.quiz_game.handle_answer(client_socket, answer)

                            if self.quiz_game.current_question < len(self.quiz_game.quizzes['general']):
                                next_question = self.quiz_game.quizzes['general'][self.quiz_game.current_question]
                                response = {
                                    'type': 'question',
                                    'question': next_question['question'],
                                    'answers': next_question['answers'],
                                    'time_limit': next_question['time_limit']
                                }
                                response_body = json.dumps(response)
                                response_header = (
                                    'HTTP/1.1 200 OK\r\n'
                                    'Content-Type: application/json\r\n'
                                    f'Content-Length: {len(response_body)}\r\n'
                                    'Access-Control-Allow-Origin: *\r\n'
                                    'Connection: keep-alive\r\n\r\n'
                                )
                            else:
                                response = {'type': 'end', 'message': 'Quiz completed'}
                                response_body = json.dumps(response)
                                response_header = (
                                    'HTTP/1.1 200 OK\r\n'
                                    'Content-Type: application/json\r\n'
                                    f'Content-Length: {len(response_body)}\r\n'
                                    'Access-Control-Allow-Origin: *\r\n'
                                    'Connection: keep-alive\r\n\r\n'
                                )
                            client_socket.sendall(response_header.encode('utf-8') + response_body.encode('utf-8'))
                        
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON: {e}")
                            response_body = '400 Bad Request'
                            response_header = (
                                'HTTP/1.1 400 Bad Request\r\n'
                                f'Content-Length: {len(response_body)}\r\n'
                                'Access-Control-Allow-Origin: *\r\n'
                                'Connection: keep-alive\r\n\r\n'
                            )
                            client_socket.sendall(response_header.encode('utf-8') + response_body.encode('utf-8'))
                    
                    else:
                        response_body = '404 Not Found'
                        response_header = (
                            'HTTP/1.1 404 Not Found\r\n'
                            f'Content-Length: {len(response_body)}\r\n'
                            'Access-Control-Allow-Origin: *\r\n'
                            'Connection: keep-alive\r\n\r\n'
                        )
                        client_socket.sendall(response_header.encode('utf-8') + response_body.encode('utf-8'))
                
                else:
                    response_body = '405 Method Not Allowed'
                    response_header = (
                        'HTTP/1.1 405 Method Not Allowed\r\n'
                        f'Content-Length: {len(response_body)}\r\n'
                        'Access-Control-Allow-Origin: *\r\n'
                        'Connection: keep-alive\r\n\r\n'
                    )
                    client_socket.sendall(response_header.encode('utf-8') + response_body.encode('utf-8'))

        except socket.timeout:
            print("Connection timed out. Closing connection.")
        except Exception as e:
            print(f"Exception handling client: {e}")
        finally:
            try:
                client_socket.shutdown(socket.SHUT_RDWR)
                client_socket.close()
            except OSError as e:
                print(f"Error closing socket: {e}")

    def start(self):
        print("Server starting...")
        while True:
            try:
                client_socket, addr = self.server_socket.accept()
                print(f"New connection from {addr}")
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
            except socket.timeout:
                print("Server accept timeout occurred")
            except Exception as e:
                print(f"Exception accepting connection: {e}")

if __name__ == "__main__":
    server = QuizServer()
    server.start()
