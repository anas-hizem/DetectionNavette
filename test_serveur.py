import socket
import json

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 65432))
    server_socket.listen(1)
    print("Server is listening on port 65432...")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address} has been established.")
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            print(f"Received message: {message}")
        client_socket.close()

if __name__ == "__main__":
    start_server()
