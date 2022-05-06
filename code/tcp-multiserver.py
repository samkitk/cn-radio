# import socket

# HOST = "127.0.0.1"  # The server's hostname or IP address
# PORT = 8080  # The port used by the server


# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print(f"Connected by {addr}")
#         while True:
#             data = conn.recv(1024)
#             if not data:
#                 break
#             conn.sendall(data)


#!/usr/bin/python           # This is server.py file                                                                                                                                                                           

import socket               # Import socket module
import _thread

def on_new_client(clientsocket,addr):
    msg = clientsocket.recv(1024)
    #do some checks and if msg == someWeirdSignal: break:
    print(addr, ' >> ', msg)
    # msg = raw_input('SERVER >> ')
    #Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
    print('Got connection from', addr)
    clientsocket.send(msg)
    clientsocket.close()

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 8081               # Reserve a port for your service.

print('Server started!')
print('Waiting for clients...')

s.bind((host, port))        # Bind to the port
s.listen(5)                 # Now wait for client connection.

while True:
   c, addr = s.accept()     # Establish connection with client.
   _thread.start_new_thread(on_new_client,(c,addr))
   #Note it's (addr,) not (addr) because second parameter is a tuple
   #Edit: (c,addr)
   #that's how you pass arguments to functions when creating new threads using thread module.
s.close()