# This is server code to send video and audio frames over UDP

# ---------Importing Library --------------
import socket
import _thread
import threading
import wave
import pyaudio
import time
import math
import struct
from collections import namedtuple
import pickle
import pprint

# ----------Declarations-----------
host_name = socket.gethostname()
# host_ip = '127.0.0.1'#  socket.gethostbyname(host_name)
# print(host_ip)
# port = 5432

ttl = struct.pack('b', 2)
multicast_group = ('127.0.0.1', 5432)

# -----------UDP Socket-------------


def audio_stream_UDP(client_addr):
    BUFF_SIZE = 65536
    server_socket = socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl, )
    # server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
    server_socket.bind(multicast_group)
    CHUNK = 1024
    wf = wave.open("data/2o6MB.wav")
    p = pyaudio.PyAudio()
    print('server listening at', (multicast_group), wf.getframerate())
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=True,
                    frames_per_buffer=CHUNK)

    data = None
    sample_rate = wf.getframerate()
    while True:
        msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
        print('[GOT connection from]... ', client_addr, msg)
        DATA_SIZE = math.ceil(wf.getnframes()/CHUNK)
        DATA_SIZE = str(DATA_SIZE).encode()
        print('[Sending data size]...', wf.getnframes()/sample_rate)
        server_socket.sendto(DATA_SIZE, client_addr)
        cnt = 0
        while True:
            data = wf.readframes(CHUNK)
            server_socket.sendto(data, client_addr)
            # Here you can adjust it according to how fast you want to send data keep it > 0
            time.sleep(0.001)
            print(cnt)
            if cnt > (wf.getnframes()/CHUNK):
                break
            cnt += 1
        break
    print('SENT...')

# ----------SEND INFORMATION-----------

def send_info():  # add client addr here too
    radio_stn_info = {'radio_stn_number': 1, 'radio_stn_name_size': 20, 'radio_stn_name': 'RedFM',
                      'multicast_address': '224.1.1.1', 'data_port': 5432, 'info_port': 5049, 'bit_rate': 234}
    print('Radio_stn_info: ', end=' ')
    pprint.pprint(radio_stn_info)
    picklestring = pickle.dumps(radio_stn_info)
    print('PICKLE: {!r}'.format(picklestring))
    unpicklestring = pickle.loads(picklestring)
    pprint.pprint(unpicklestring)
    for i in unpicklestring:
    	print(i, unpicklestring[i])

# ---------STATION----------


def station():
    t1 = threading.Thread(target=audio_stream_UDP, args())
    t2 = threading.Thread(target=send_info, args())
    t1.start()
    t2.join()


#

ts1= threading
# ----------TCP Socket-------------------


def on_new_client(clientsocket, addr):
    msg = clientsocket.recv(1024)
    print(addr, ' >> ', msg)
    print('Got connection from', addr)
    clientsocket.send(msg)
    clientsocket.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Server started!')
print('Waiting for clients...')

s.bind(multicast_group)
s.listen(5)

while True:
    c, addr = s.accept()
    _thread.start_new_thread(on_new_client, (c, addr))
s.close()


# ---------STATION 1-------------
# thread:
# 	#socket 1
# 		thread:
# 		#TMH
# 		30 S
# 		FP

# ---------STATION 2-----------
# thread:
# 	#socket 2
# 		THR
# 		FP
# 		FP PTR


t1 = threading.Thread(target=select_station_TCP, args=())
t1.start()
