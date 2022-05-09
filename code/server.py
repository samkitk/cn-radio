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


#--Sending Site Info-----
site_info = {
    "type": 10,
    "site_name_size": 5,
    "site_name": "RadioSite",
    "site_desc_size": 15,
    "site_desc": "This is RadioSite",
    "radio_stn_count": 2,
}

#----Station List-------
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

#Pickle is used to convert object to byte stream
pickled_radio_stn_info = pickle.dumps(radio_stn_info)



#-------------UDP SERVER SOCKET----------------\

global path_Station1
#Paths of the station which consists of ".wav" audio files
path_Station1 = os.listdir("data/Station_1")
path_Station2 = os.listdir("data/Station_2")
#ttl set for MULTICASTING
ttl = struct.pack('b', 2)
#Data Port for both the stations
MCAST_PORT = 5007 

IS_ALL_GROUPS = True

def station_1():
    #=========== STATION 1 ================
    MCAST_GRP_STATION1 = '239.192.1.1'

    #---------- MULTIMEDIA MULTICAST-----
    def audio_stream_UDP_Station1():
        BUFF_SIZE = 65536
        #Creating UDP scoket and setting socket Operations
        audio_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        audio_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
        CHUNK = 10240
        #We use for loop to send all songs on this path
        for i in path_Station1:
            #wave library reads the wav files 
            wf = wave.open("data/Station_1/" + i)
            #pyaudio is used to stream functionalties
            p = pyaudio.PyAudio()   
            #we extract all bitrate and frame rate of the audio via pyaudio
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            input=True,
                            frames_per_buffer=CHUNK)
            data = None            
            #count calculates the number of packets sent
            packet_count = 0
            while True:
                data = wf.readframes(CHUNK)
                #this data is sent to Multicast group of Station 1
                audio_server_socket.sendto(data, (MCAST_GRP_STATION1, MCAST_PORT))
                #this sleep is adjusted according to uniform bitrate
                time.sleep(0.005)
                print(packet_count)
                #this if loop breaks while if we have sent
                if packet_count > (wf.getnframes()/CHUNK):
                    break
                packet_count += 1
            print('Audio Sent')

    #----------INFORMATION MULTICAST-----

    #Information Port of Station 1
    MCAST_INFOPORT_S1 = 5432

    def information_stream_Station1():
        #We set UDP socket on same multicast IP but different port
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
        audio_server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        audio_server_socket2.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
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
            audio_server_socket2.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
            count = 0
            while True:
                data = wf.readframes(CHUNK)
                audio_server_socket2.sendto(data, (MCAST_GRP_STATION2, MCAST_PORT))
                time.sleep(0.01)
                print(count)
                if count > (wf.getnframes()/CHUNK):
                    break
                count += 1
            print('SENT...')


    #----------INFORMATION STREAM---------------

    MCAST_INFOPORT_S2 = 5432
    def information_stream_Station2():
        # print("Hello")
        info_server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
                info_server_socket2.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
                info_server_socket2.sendto(string, (MCAST_GRP_STATION2, MCAST_INFOPORT_S2))
                time.sleep(1)
                duration = duration-1         

    #--------THREADING OF STATION 1 PROCESSES-----          
    taudio_S2= threading.Thread(target=audio_stream_UDP_Station2, args=())
    tinfo_S2= threading.Thread(target=information_stream_Station2, args=())
    taudio_S2.start()
    tinfo_S2.start()
    print("Station 2 Running")
    

    
def tcp_connection():
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
    host = '127.0.0.1'  # Get local machine name
    port = 3004  # Reserve a port for your service.

    print("Server started!")
    print("Waiting for clients...")
    s.bind((host, port))  # Bind to the port
    s.listen(5)  # Now wait for client connection.

    while True:
        c, addr = s.accept()  # Establish connection with client.
        t1=threading.Thread(target=on_new_client,args=(c, addr, pickled_radio_stn_info))
        t1.start()

t_tcp=threading.Thread(target=tcp_connection,args=())
t_s1=threading.Thread(target=station_1,args=())
t_s2=threading.Thread(target=station_2,args=())

t_tcp.start()
t_s1.start()
t_s2.start()
