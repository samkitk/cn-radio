import socket
import threading
import wave
from xmlrpc import client
import pyaudio
import time
import math
import struct 

MCAST_PORT = 5007
MCAST_GRP = '224.1.1.1'
ttl = struct.pack('b', 2)
IS_ALL_GROUPS = True

def audio_stream_UDP():

    BUFF_SIZE = 65536
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
    CHUNK = 10240
    wf = wave.open("data/shakira.wav")
    p = pyaudio.PyAudio()   
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=True,
                    frames_per_buffer=CHUNK)

    data = None
    sample_rate = wf.getframerate()
    while True:
        server_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        DATA_SIZE = math.ceil(wf.getnframes()/CHUNK)
        DATA_SIZE = str(DATA_SIZE).encode()
        print('[Sending data size]...', wf.getnframes()/sample_rate)
        server_socket.sendto(DATA_SIZE, (MCAST_GRP, MCAST_PORT))
        cnt = 0
        while True:
            data = wf.readframes(CHUNK)
            server_socket.sendto(data, (MCAST_GRP, MCAST_PORT))
            time.sleep(0.001)
            print(cnt)
            if cnt > (wf.getnframes()/CHUNK):
                break
            cnt += 1
        break
    print('SENT...')

# audio_stream_UDP()
t1 = threading.Thread(target=audio_stream_UDP, args=())
t1.start()
