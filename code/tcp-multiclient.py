import socket

HOST = socket.gethostname()  # The server's hostname or IP address
PORT = 8082  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # s.sendall(b"1")
    num = 1
    # sep = "\0"
    string = str(num) 
    s.send(string.encode())
