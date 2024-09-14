import socket
import threading
import json
from game import QuizGame
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

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
        self.lock = threading.Lock()

    def handle_client(self, client_socket):
        print("Handling new client connection.")
        player_id = client_socket.getpeername()[0]
        try:
            with self.lock:
                if not self.quiz_game.add_player(player_id):
                    response_body = json.dumps({'error': 'Maximum number of players reached'})
                    response_header = (
                        'HTTP/1.1 403 Forbidden\r\n'
                        f'Content-Length: {len(response_body)}\r\n'
                        'Content-Type: application/json\r\n'
                        'Access-Control-Allow-Origin: *\r\n'
                        'Connection: keep-alive\r\n\r\n'
                    )
                    client_socket.sendall(response_header.encode('utf-8') + response_body.encode('utf-8'))
                    return

            while True:
                request = client_socket.recv(1024).decode('utf-8')
                if not request:
                    print("No data received. Closing connection.")
                    break
                
                print(f"Received request from {player_id}:")
                print(request)
                
                parts = request.split('\r\n\r\n', 1)
                headers = parts[0]
                body = parts[1] if len(parts) > 1 else ''
    
                request_line = headers.split('\r\n')[0]
                method, path, _ = request_line.split(' ')
                
                print(f"Method: {method}, Path: {path}")
                print(f"Body: {body}")
                
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
    
                elif method == 'GET':
                    if path == '/get_question':
                        with self.lock:
                            question = self.quiz_game.get_question(player_id)
                            if question:
                                response = {
                                    'type': 'question',
                                    'question': question['question'],
                                    'answers': question['answers'],
                                    'time_limit': question['time_limit']
                                }
                            else:
                                response = {
                                    'type': 'end',
                                    'message': 'Quiz completed',
                                    'score': self.quiz_game.get_player_score(player_id),
                                    'all_scores': self.quiz_game.get_all_scores()
                                }
                        
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
                            json_start = body.find('{')
                            if json_start != -1:
                                json_data = body[json_start:]
                                print(f"Extracted JSON data: {json_data}")
                                
                                data = json.loads(json_data)
                                answer = data.get('answer')
                                print(f"Received answer from client {player_id}: {answer}")
    
                                with self.lock:
                                    has_next_question = self.quiz_game.handle_answer(player_id, answer)
                                    if has_next_question:
                                        next_question = self.quiz_game.get_question(player_id)
                                        response = {
                                            'type': 'question',
                                            'question': next_question['question'],
                                            'answers': next_question['answers'],
                                            'time_limit': next_question['time_limit']
                                        }
                                    else:
                                        response = {
                                            'type': 'end',
                                            'message': 'Quiz completed',
                                            'score': self.quiz_game.get_player_score(player_id),
                                            'all_scores': self.quiz_game.get_all_scores()
                                        }
    
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
                                print("No JSON data found in the request body")
                                raise ValueError("No JSON data found")
                        
                        except (json.JSONDecodeError, ValueError) as e:
                            print(f"Error processing JSON: {e}")
                            response_body = json.dumps({'error': 'Invalid JSON data'})
                            response_header = (
                                'HTTP/1.1 400 Bad Request\r\n'
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
            with self.lock:
                self.quiz_game.remove_player(player_id)
            try:
                client_socket.shutdown(socket.SHUT_RDWR)
                client_socket.close()
            except OSError as e:
                print(f"Error closing socket: {e}")

    def run_http_server(self):
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

    def start(self):
        print("Server starting...")
        server_thread = threading.Thread(target=self.run_http_server)
        server_thread.start()

        # Start the GUI HTTP server
        gui_server = HTTPServer(('localhost', 5001), GUIRequestHandler)
        gui_server.quiz_server = self
        print("GUI server started on port 5001")
        gui_server.serve_forever()

class GUIRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/get_status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            with self.server.quiz_server.lock:
                status = []
                for player_id, player in self.server.quiz_server.quiz_game.players.items():
                    status.append({
                        'player_id': player_id,
                        'score': self.server.quiz_server.quiz_game.get_player_score(player_id),
                        'current_question': player.current_question,
                        'last_answer': getattr(player, 'last_answer', None)
                    })
            
            self.wfile.write(json.dumps(status).encode())
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == "__main__":
    server = QuizServer()
    server.start()