from __future__ import unicode_literals, print_function
import socket
import threading
import wave
from xmlrpc import client
import pyaudio
import time
import math
import struct 
import argparse
import ffmpeg
import sys
import os
from pprint import pprint
from sqlalchemy import null
from tinytag import TinyTag
import subprocess
import numpy as np

MCAST_PORT = 5007
MCAST_GRP = '224.1.1.1'
ttl = struct.pack('b', 2)
IS_ALL_GROUPS = True

path_Station1 = os.listdir("data/Station_1")
print (path_Station1)

path_Station2 = os.listdir("data/Station_2")
print (path_Station2)

def audio_stream_UDP():
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
            audio_server_socket.sendto(DATA_SIZE, (MCAST_GRP, MCAST_PORT))
            cnt = 0
            while True:
                data = wf.readframes(CHUNK)
                audio_server_socket.sendto(data, (MCAST_GRP, MCAST_PORT))
                time.sleep(0.005)
                print(cnt)
                if cnt > (wf.getnframes()/CHUNK):
                    break
                cnt += 1
            break
        print('SENT...')

path_Station3 = os.listdir("data/Station_3")
print (path_Station3)

def info_stream_UDP():
    n=len(path_Station3)
    print(n)
    path_Station_3 = np.array(path_Station3)
    print("Printing array of songs : ")
    print(path_Station_3)

    for x in range(len(path_Station_3)) :
        i= TinyTag.get("data/Station_3/" + path_Station_3[x])
        #print(i)
        print(len(i.title))
        print(i.title)
        print(str(i.filesize))
        print(i.duration)
        if(x<(len(path_Station_3)-1)) :
            k= TinyTag.get("data/Station_3/" + path_Station_3[x+1])
            print(len(k.title))
            print(k.title)
            
        

        # print(i.artist)
        # print(str(i.filesize))
        # del i

        # BUFF_SIZE = 65536
        # info_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # info_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
        # info_list = []
        # CHUNK = 10240
        # while True:
        #     info_server_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
            
        #     info_server_socket.sendto(DATA_SIZE, (MCAST_GRP, MCAST_PORT))
        #     cnt = 0
        #     while True:
        #         info_server_socket.sendto(data, (MCAST_GRP, MCAST_PORT))
        #         time.sleep(0.0175)
        #         print(cnt)
        #         if cnt > (wf.getnframes()/CHUNK):
        #             break
        #         cnt += 1
        #     break
        # print('SENT...')


# audio_stream_UDP()
# t1 = threading.Thread(target=audio_stream_UDP, args=())
# t1.start()
t2 = threading.Thread(target=info_stream_UDP, args=())
t2.start()
