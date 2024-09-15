# Multiplayer Quiz Game (Kahoot-like)

    This is a multiplayer quiz game similar to Kahoot that supports up to 5 players. 
    The backend is built with Python using a TCP server, and the frontend is created with Svelte. 
    The server handles HTTP-like requests over a TCP connection, 
    responds with custom headers and JSON-encoded data, and manages multiple clients via threads.

## Features
    .   Max Players: 5 players per session
    .   Answer Timer: 15 seconds to submit an answer
    .   Reconnect Logic: After the quiz ends, the socket automatically closes and reopens for new players if needed. 
        If no response is received, the socket closes automatically.
    
## Running the Application
    There are two ways to run the application: locally or using Docker and Docker Compose.
    1.  Running Locally
        To run the app locally, use the <start.sh> bash script. Here's how:
        1.  Configure the IP Address:
            .   Modify the IP address in the front-end located in client/svelte-client/API.
            .   svelte to match your device’s local IP address.
            .   You can find your local IP by running ip a in your terminal.
        2.  Run the Application
            .   <./start.sh>
            .   The server (backend) will run on port 5000.
            .   The Svelte front-end will be accessible at http://<your_ip_address>:8000.
            .   The Tkinter GUI for the server will automatically open.

    2.  Running with Docker and Docker Compose
        To run the app using Docker, follow these steps:
            1. Stop any previous instances:
                .   docker-compose down
            2.  Build the Docker containers:
                .   docker-compose build
            3.  Start the application:
                .   docker-compose up
        The Flask app (which holds the server GUI) will be running at http://localhost:5002 or your local IP.
        The Svelte front-end will be available at http://localhost:5003.
        The TCP server will be running on port 5000.

## Components Overview
    1.  Backend (Python TCP Server)
        The backend is a TCP server that listens for incoming connections using socket.
        AF_INET (IPv4) and socket.SOCK_STREAM (TCP). 
        It manages multiple clients using threads and handles custom HTTP-like requests over a TCP connection. 
        It uses the following ports:
            .   Port 5000: TCP connection for player requests
            .   Port 5001: For server status (when running with Docker)
    
    2.  Frontend (Svelte)
            .   Port 8000 when running locally
            .   Port 5003 when running via Docker

## Server GUI
    The Tkinter-based GUI for the server opens automatically when running the app via the bash script,
    or it is hosted on Flask when running with Docker at port 5002.



## Additional Information
    After each quiz round, players can reconnect if they wish to start a new game.
    If no response is received from a player, the socket connection will automatically close after the timeout period

## License
    This project is licensed under the MIT License.