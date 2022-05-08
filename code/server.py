import socket 
import _thread, threading
import pickle
from xmlrpc import client
import pyaudio
import wave
import time
import math
import struct 
import os
from tinytag import TinyTag
import numpy as np

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
    "data_port": 5007,
    "info_port": 5432,
    "bit_rate": 44100,
}

station2 = {
    "radio_stn_number": 2,
    "radio_stn_name_size": 10,
    "radio_stn_name": "Blue FM",
    "multicast_address": "239.192.1.2",
    "data_port": 5007,
    "info_port": 5432,
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

#-------------UDP SERVER SOCKET----------------\
global path_Station1
path_Station1 = os.listdir("data/Station_1")
path_Station2 = os.listdir("data/Station_2")
ttl = struct.pack('b', 2)
MCAST_PORT = 5007 #DataPort

IS_ALL_GROUPS = True

def station_1():
    #=========== STATION 1 ================
    MCAST_GRP_STATION1 = '239.192.1.1'

    #---------- MULTIMEDIA MULTICAST-----
    def audio_stream_UDP_Station1():
        BUFF_SIZE = 65536
        audio_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        audio_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
        CHUNK = 10240
        for i in path_Station1:
            wf = wave.open("data/Station_1/" + i)
            p = pyaudio.PyAudio()   
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            input=True,
                            frames_per_buffer=CHUNK)
            data = None
            sample_rate = wf.getframerate()
            print(sample_rate)
            while True:
                audio_server_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
                DATA_SIZE = math.ceil(wf.getnframes()/CHUNK)
                DATA_SIZE = str(DATA_SIZE).encode()
                # DURATION = DATA_SIZE*CHUNK/44100

                # print('[Sending data size]...', wf.getnframes()/sample_rate)
                audio_server_socket.sendto(DATA_SIZE, (MCAST_GRP_STATION1, MCAST_PORT))
                cnt = 0
                while True:
                    data = wf.readframes(CHUNK)
                    audio_server_socket.sendto(data, (MCAST_GRP_STATION1, MCAST_PORT))
                    time.sleep(0.005)
                    print(cnt)
                    if cnt > (wf.getnframes()/CHUNK):
                        break
                    cnt += 1
                break
            print('SENT...')

    #----------INFORMATION MULTICAST-----

    MCAST_INFOPORT_S1 = 5007
    def information_stream_Station1():
        # print("Hello")
        info_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        path_Station1 = os.listdir("data/Station_1")
        n=len(path_Station1)
        path_Station1 = np.array(path_Station1)
        for x in range(len(path_Station1)):
            i= TinyTag.get("data/Station_1/" + path_Station1[x])
            title = path_Station1[x]
            size_title = len(title)        
            filesize = i.filesize
            duration = i.duration
            if(x<(len(path_Station1)-1)) :
                k= TinyTag.get("data/Station_1/" + path_Station1[x+1])
                next_song_title = path_Station1[x+1]
                next_song_size = len(next_song_title)            
                song_info = {"Song Name Size" : size_title, "title": title, "Filesize" : filesize,  "Next Song Size" : next_song_size, "Next Song Title" : next_song_title}
            else:
                song_info = {"Song Name Size" : size_title, "title": title, "Filesize" : filesize }
            while(duration>0):
                song_info.update({'Time Remaining': duration})
                string = pickle.dumps(song_info)
                info_server_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
                info_server_socket.sendto(string, (MCAST_GRP_STATION1, MCAST_INFOPORT_S1))
                time.sleep(1)
                duration = duration-1  
                print("Information sent")        
            

    #-----------THREADING OF STATION 1 PROCESSES-----
    taudio_S1= threading.Thread(target=audio_stream_UDP_Station1, args=())
    tinfo_S1= threading.Thread(target=information_stream_Station1, args=())
    taudio_S1.start()
    tinfo_S1.start()
    print("Station 1 Running")


def station_2():
    #=========== STATION 2 ============
    MCAST_GRP_STATION2 = '239.192.1.2'

    #-----------AUDIO STREAM OF STATION 2------
    def audio_stream_UDP_Station2():
        BUFF_SIZE = 65536
        audio_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        audio_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
        CHUNK = 10240
        for i in path_Station2:
            wf = wave.open("data/Station_2/" + i)
            p = pyaudio.PyAudio()   
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            input=True,
                            frames_per_buffer=CHUNK)
            data = None
            sample_rate = wf.getframerate()
            print(sample_rate)
            while True:
                audio_server_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
                DATA_SIZE = math.ceil(wf.getnframes()/CHUNK)
                DATA_SIZE = str(DATA_SIZE).encode()

                print('[Sending data size]...', wf.getnframes()/sample_rate)
                audio_server_socket.sendto(DATA_SIZE, (MCAST_GRP_STATION2, MCAST_PORT))
                cnt = 0
                while True:
                    data = wf.readframes(CHUNK)
                    audio_server_socket.sendto(data, (MCAST_GRP_STATION2, MCAST_PORT))
                    time.sleep(0.005)
                    print(cnt)
                    if cnt > (wf.getnframes()/CHUNK):
                        break
                    cnt += 1
                break
            print('SENT...')


    #----------INFORMATION STREAM---------------

    MCAST_INFOPORT_S2 = 5007
    def information_stream_Station2():
        # print("Hello")
        info_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        path_Station2 = os.listdir("data/Station_2")
        n=len(path_Station2)
        path_Station2 = np.array(path_Station2)
        for x in range(len(path_Station2)):
            i= TinyTag.get("data/Station_2/" + path_Station2[x])
            title = path_Station2[x]
            size_title = len(title)        
            filesize = i.filesize
            duration = i.duration
            if(x<(len(path_Station2)-1)) :
                k= TinyTag.get("data/Station_2/" + path_Station2[x+1])
                next_song_title = path_Station2[x+1]
                next_song_size = len(next_song_title)            
                song_info = {"Song Name Size" : size_title, "title": title, "Filesize" : filesize,  "Next Song Size" : next_song_size, "Next Song Title" : next_song_title}
            else:
                song_info = {"Song Name Size" : size_title, "title": title, "Filesize" : filesize }
            while(duration>0):
                song_info.update({'Time Remaining': duration})
                string = pickle.dumps(song_info)
                info_server_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
                info_server_socket.sendto(string, (MCAST_GRP_STATION2, MCAST_INFOPORT_S2))
                time.sleep(1)
                duration = duration-1  
                print("Information sent")        

    #--------THREADING OF STATION 1 PROCESSES-----          
    taudio_S2= threading.Thread(target=audio_stream_UDP_Station2, args=())
    tinfo_S2= threading.Thread(target=information_stream_Station2, args=())
    taudio_S2.start()
    tinfo_S2.start()
    print("Station 2 Running")
    

t_s1=threading.Thread(target=station_1,args=())
t_s2=threading.Thread(target=station_2,args=())

t_s1.start()
t_s2.start()
    

def on_new_client(clientsocket, addr, pickled_radio_stn_info):
    msg = clientsocket.recv(1024)
    temp = msg.decode()
    if temp == "1":
        print("Succesfully Received Handshake from", addr)
        print("Now sending Station List to", addr)
        clientsocket.send(pickled_radio_stn_info)
    print("Sent List")
    clientsocket.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = socket.gethostname()  # Get local machine name
port = 3003  # Reserve a port for your service.

print("Server started!")
print("Waiting for clients...")
s.bind((host, port))  # Bind to the port
s.listen(5)  # Now wait for client connection.

while True:
    c, addr = s.accept()  # Establish connection with client.
    t1=threading.Thread(target=on_new_client,args=(c, addr, pickled_radio_stn_info))
    t1.start()

