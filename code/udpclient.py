
import socket
import threading
import wave
import pyaudio
import time
import queue
import os
import struct

MCAST_GRP = '224.1.1.1'  # socket.gethostbyname(host_name)
MCAST_PORT = 5007
# port = 5007
IS_ALL_GROUPS = True
# server_addr = ('',5007)

q = queue.Queue(maxsize=2000)


def audio_stream_UDP():
    BUFF_SIZE = 65536
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    group = socket.inet_aton(MCAST_GRP)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    client_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    client_socket.bind((MCAST_GRP, MCAST_PORT))
    p = pyaudio.PyAudio()
    CHUNK = 1024
    stream = p.open(format=p.get_format_from_width(2),
					channels=2,
					rate=44100,
					output=True,
					frames_per_buffer=CHUNK)
					
	# # create socket
	# message = b'Hello'
	# client_socket.sendto(message,(MCAST_GRP,MCAST_PORT))
	# print("Message sent")
	
    def getAudioData():
        while True:
            print(MCAST_GRP,MCAST_PORT)
            frame,_= client_socket.recvfrom(BUFF_SIZE)
            q.put(frame)
            print('Queue size...',q.qsize())
    t1 = threading.Thread(target=getAudioData, args=())
    t1.start()
    time.sleep(1)
    print('Now Playing...')
    while True:
        frame = q.get()
        stream.write(frame)
    client_socket.close()
    print('Audio closed')
    os._exit(1)


# audio_stream_UDP()
t1 = threading.Thread(target=audio_stream_UDP, args=())
t1.start()