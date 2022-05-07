import socket
import threading
import wave
import pyaudio
import time
import queue
import os
import struct

MCAST_GRP = '224.1.1.1' 
MCAST_PORT = 5007
IS_ALL_GROUPS = True

q = queue.Queue(maxsize=20000)


def audio_stream_UDP():
    BUFF_SIZE = 40960
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    group = socket.inet_aton(MCAST_GRP)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    client_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.bind(('', MCAST_PORT))
    p = pyaudio.PyAudio()
    CHUNK = 10240
    stream = p.open(format=p.get_format_from_width(2),
					channels=2,
					rate=44100,
					output=True,
					frames_per_buffer=CHUNK)					

    def getAudioData():
        while True:
            print(MCAST_GRP,MCAST_PORT)
            frame,_= client_socket.recvfrom(BUFF_SIZE)
            q.put(frame)
            print('Queue size...',q.qsize())
    t1 = threading.Thread(target=getAudioData, args=())
    t1.start()
    time.sleep(0.0175)
    print('Now Playing...')
    while True:
        frame = q.get()
        stream.write(frame)
        # BUFF_SIZE.flush()
    client_socket.close()
    print('Audio closed')
    os._exit(1)


audio_stream_UDP()
