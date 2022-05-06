import socket

HOST = socket.gethostname()  # The server's hostname or IP address
PORT = 8081  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"1")
    data = s.recv(1024)

print(f"Server to Client >> {data!r}")