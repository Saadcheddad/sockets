import socket
import os

# Server configuration
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 8080
BUFFER_SIZE = 1024

# Directory where files will be saved
SAVE_DIR = "server_files"
os.makedirs(SAVE_DIR, exist_ok=True)

def handle_get_request(conn, filepath):
    try:
        with open(os.path.join(SAVE_DIR, filepath), 'rb') as file:
            conn.send(b"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\n\r\n")
            data = file.read(BUFFER_SIZE)
            while data:
                conn.send(data)
                data = file.read(BUFFER_SIZE)
        print(f"File '{filepath}' sent to client.")
    except FileNotFoundError:
        conn.send(b"HTTP/1.1 404 Not Found\r\n\r\nFile not found")
        print(f"File '{filepath}' not found.")

def handle_post_request(conn, headers):
    filename = headers.get("Filename")
    file_size = int(headers.get("Content-Length", 0))

    if not filename or not file_size:
        conn.send(b"HTTP/1.1 400 Bad Request\r\n\r\n")
        return

    with open(os.path.join(SAVE_DIR, filename), 'wb') as file:
        received_size = 0
        while received_size < file_size:
            data = conn.recv(min(BUFFER_SIZE, file_size - received_size))
            if not data:
                break
            file.write(data)
            received_size += len(data)

    conn.send(b"HTTP/1.1 200 OK\r\n\r\nFile uploaded successfully")
    print(f"File '{filename}' uploaded successfully.")

def parse_headers(header_data):
    headers = {}
    for line in header_data.splitlines():
        parts = line.split(": ", 1)
        if len(parts) == 2:
            headers[parts[0]] = parts[1]
    return headers

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server running on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                request = conn.recv(BUFFER_SIZE).decode()
                request_line, header_data = request.split("\r\n", 1)
                headers = parse_headers(header_data)

                method, path, _ = request_line.split(" ")

                if method == "GET":
                    filepath = path.strip("/")
                    handle_get_request(conn, filepath)
                elif method == "POST":
                    handle_post_request(conn, headers)
                else:
                    conn.send(b"HTTP/1.1 405 Method Not Allowed\r\n\r\n")

if __name__ == "__main__":
    start_server()


	
