import socket  # Import socket module
import _thread, threading
import pickle
from xmlrpc import client
import pyaudio
import wave
import time
import math
import struct 

site_info = {
    "type": 10,
    "site_name_size": 5,
    "site_name": "RadioSite",
    "site_desc_size": 15,
    "site_desc": "This is RadioSite",
    "radio_stn_count": 2,
}

station1 = {
    "radio_stn_number": 1,
    "radio_stn_name_size": 10,
    "radio_stn_name": "Red FM",
    "multicast_address": "239.192.1.1",
    "data_port": 8000,
    "info_port": 8001,
    "bit_rate": 44100,
}

station2 = {
    "radio_stn_number": 2,
    "radio_stn_name_size": 10,
    "radio_stn_name": "Love FM",
    "multicast_address": "239.192.1.2",
    "data_port": 8000,
    "info_port": 8001,
    "bit_rate": 44100,
}

radio_stn_info = {"site_info": site_info, "station1": station1, "station2": station2}

pickled_radio_stn_info = pickle.dumps(radio_stn_info)
# pickled_site_info = pickle.dumps(site_info)



#    x = input()
#    if(x=="a"):
#        s.close()
#        break
# Note it's (addr,) not (addr) because second parameter is a tuple
# Edit: (c,addr)
# that's how you pass arguments to functions when creating new threads using thread module.

#-------------UDP SERVER SOCKET----------------
### STATION 1
MCAST_PORT = 8000
MCAST_GRP = '239.192.1.1'
ttl = struct.pack('b', 2)
IS_ALL_GROUPS = True

def audio_stream_UDP():
    BUFF_SIZE = 65536
    audio_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    audio_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
    CHUNK = 1024
    print("Playing Wav File")
    wf = wave.open("data/10MB.wav")
    p = pyaudio.PyAudio()   
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=True,
                    frames_per_buffer=CHUNK)

    data = None
    sample_rate = wf.getframerate()
    while True:
        audio_server_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        DATA_SIZE = math.ceil(wf.getnframes()/CHUNK)
        DATA_SIZE = str(DATA_SIZE).encode()
        print('[Sending data size]...', wf.getnframes()/sample_rate)
        audio_server_socket.sendto(DATA_SIZE, (MCAST_GRP, MCAST_PORT))
        cnt = 0
        while True:
            data = wf.readframes(CHUNK)
            audio_server_socket.sendto(data, (MCAST_GRP, MCAST_PORT))
            time.sleep(0.001)
            print(cnt)
            if cnt > (wf.getnframes()/CHUNK):
                break
            cnt += 1
        break
    print('SENT...')

# audio_stream_UDP()
t2 = threading.Thread(target=audio_stream_UDP, args=())
t2.start()



def on_new_client(clientsocket, addr, pickled_radio_stn_info):
    # print('Got connection from', addr)
    msg = clientsocket.recv(1024)
    temp = msg.decode()
    # print("----",temp,"----")
    # client_msg = int(temp)
    if temp == "1":
        print("Succesfully Received Handshake from", addr)
        print("Now sending Station List to", addr)
        clientsocket.send(pickled_radio_stn_info)
    print("Sent List")
    clientsocket.close()
    # do some checks and if msg == someWeirdSignal: break:
    # print(addr, ' >> ', msg)
    # msg = raw_input('SERVER >> ')
    # Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
    # num = 1
    # sep = "\0"
    # clientsocket.send((str(num)+sep).encode())


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = socket.gethostname()  # Get local machine name
port = 8095  # Reserve a port for your service.

print("Server started!")
print("Waiting for clients...")
s.bind((host, port))  # Bind to the port
s.listen(5)  # Now wait for client connection.

while True:
    c, addr = s.accept()  # Establish connection with client.
    t1=threading.Thread(target=on_new_client,args=(c, addr, pickled_radio_stn_info))
    t1.start()