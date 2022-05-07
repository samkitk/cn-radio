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
import _thread, threading
import pickle


site_info = {
    "type" : 10,
    "site_name_size" : 5,
    "site_name" : "RadioSite",
    "site_desc_size" : 15,
    "site_desc" : "This is RadioSite",
    "radio_stn_count" : 2
}

station1 = {
    "radio_stn_number" : 1,
    "radio_stn_name_size" : 10,
    "radio_stn_name" : "Red FM",
    "multicast_address" : "239.192.1.1",
    "data_port": 8000,
    "info_port" : 8001,
    "bit_rate" : 44100
}

station2 = {
    "radio_stn_number" : 2,
    "radio_stn_name_size" : 10,
    "radio_stn_name" : "Love FM",
    "multicast_address" : "239.192.1.2",
    "data_port" : 8000,
    "info_port" : 8001,
    "bit_rate"  : 44100
}

radio_stn_info = {
    "site_info": site_info,
    "station1" : station1,
    "station2" : station2
}

pickled_radio_stn_info = pickle.dumps(radio_stn_info)
# pickled_site_info = pickle.dumps(site_info)


def on_new_client(clientsocket,addr,pickled_radio_stn_info):
    # print('Got connection from', addr)
    msg = clientsocket.recv(1024)
    temp = msg.decode()
    # print("----",temp,"----")
    # client_msg = int(temp)
    if(temp=="1"):
        print("Succesfully Received Handshake from", addr)
        print("Now sending Station List to", addr)
        clientsocket.send(pickled_radio_stn_info)
    print("Sent List")
    clientsocket.close()
    #do some checks and if msg == someWeirdSignal: break:
    # print(addr, ' >> ', msg)
    # msg = raw_input('SERVER >> ')
    #Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
    # num = 1
    # sep = "\0"
    # clientsocket.send((str(num)+sep).encode())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 8079              # Reserve a port for your service.

print('Server started!')
print('Waiting for clients...')

s.bind((host, port))        # Bind to the port
s.listen(5)                 # Now wait for client connection.

while True:
   c, addr = s.accept()     # Establish connection with client.
   _thread.start_new_thread(on_new_client,(c,addr,pickled_radio_stn_info))
#    x = input()
#    if(x=="a"):
#        s.close()
#        break
   #Note it's (addr,) not (addr) because second parameter is a tuple
   #Edit: (c,addr)
   #that's how you pass arguments to functions when creating new threads using thread module.