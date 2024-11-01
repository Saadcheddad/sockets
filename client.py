import socket
import os

# Server configuration
SERVER_HOST = '192.168.112.128'  
SERVER_PORT = 8080
BUFFER_SIZE = 1024

def upload_file(filename):
    file_size = os.path.getsize(filename)
    headers = f"POST / HTTP/1.1\r\nFilename: {filename}\r\nContent-Length: {file_size}\r\n\r\n"
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        client_socket.sendall(headers.encode())

        with open(filename, 'rb') as file:
            data = file.read(BUFFER_SIZE)
            while data:
                client_socket.sendall(data)
                data = file.read(BUFFER_SIZE)
        
        response = client_socket.recv(BUFFER_SIZE)
        print("Response from server:", response.decode())

def download_file(filename):
    request = f"GET /{filename} HTTP/1.1\r\n\r\n"
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        client_socket.sendall(request.encode())
        
        with open(f"downloaded_{filename}", 'wb') as file:
            while True:
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break
                file.write(data)
        
        print(f"File '{filename}' downloaded successfully.")

if __name__ == "__main__":
    # Example usage:
    # upload_file("example.txt")
    # download_file("example.txt")
    pass

