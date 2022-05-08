import socket
import pprint
import pickle
import threading
import wave
import pyaudio
import time
import queue
import os
import struct
import multiprocessing

HOST = '127.0.0.1' # The server's hostname or IP address
PORT = 3004  # The port used by the server

menu_options = {
    "P": "Pause",
    "R": "Restart",
    "C": "Change Station",
    "X": "Exit",
}


def TCP_Socket_Client_to_Server():
    print("++++++++++++++++++++++")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        # s.sendall(b"1")
        num = 1
        # sep = "\0"
        string = str(num)
        s.send(string.encode())
        print("********************")
        data = s.recv(4096)  ##randomly taken 4096
        station_list = pickle.loads(data)
        print(data)
        return station_list


station_list = TCP_Socket_Client_to_Server()
numberOfStation = station_list["site_info"]["radio_stn_count"]


def SiteGreetings():
    print("======================")
    print("Welcome to", station_list["site_info"]["site_name"])
    print("======================")


def StationListGreetings():
    print(
        "We have",
        station_list["site_info"]["radio_stn_count"],
        "station(s) available for you!",
    )
    print(
        station_list["station1"]["radio_stn_number"],
        "-",
        station_list["station1"]["radio_stn_name"],
    )
    print("Address:", station_list["station1"]["multicast_address"])
    print("Data Port:", station_list["station1"]["data_port"])
    print("Info Port:", station_list["station1"]["info_port"])
    print("BitRate:", station_list["station1"]["bit_rate"])
    print("----------------------")
    print(
        station_list["station2"]["radio_stn_number"],
        "-",
        station_list["station2"]["radio_stn_name"],
    )
    print("Address:", station_list["station2"]["multicast_address"])
    print("Data Port:", station_list["station2"]["data_port"])
    print("Info Port:", station_list["station2"]["info_port"])
    print("BitRate:", station_list["station2"]["bit_rate"])


def printMenu():
    for i in menu_options.keys():
        print(i, "-->", menu_options[i])


# ------------- UDP ---------------------

#====== STATION 1 VARIABLES ========
MCAST_GRP_S1 = station_list["station1"]["multicast_address"]
MCAST_PORT_S1 = station_list["station1"]["data_port"]
MCAST_INFO_PORT_S1 = station_list["station1"]["info_port"]

#====== STATION 2 VARIABLES==========
MCAST_GRP_S2 = station_list["station2"]["multicast_address"]
MCAST_PORT_S2 = station_list["station2"]["data_port"]
MCAST_INFO_PORT_S2 = station_list["station2"]["info_port"]

q = queue.Queue(maxsize=20000)

def audio_stream_UDP(MCAST_GRP, MCAST_PORT):
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
            # print(MCAST_GRP,MCAST_PORT)
            frame,_= client_socket.recvfrom(BUFF_SIZE)
            q.put(frame)
            # print('Queue size...',q.qsize())
    ta = threading.Thread(target=getAudioData, args=())
    ta.start()
    time.sleep(0.0175)
    print('Now Playing...')
    while True:
        frame = q.get()
        stream.write(frame)
        # BUFF_SIZE.flush()
    client_socket.close()
    print('Audio closed')
    os._exit(1)

def info_stream_UDP(MCAST_GRP, MCAST_INFO_PORT):
    BUFF_SIZE = 40960
    info_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    group = socket.inet_aton(MCAST_GRP)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    info_client_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    info_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    info_client_socket.bind(('', MCAST_INFO_PORT))
    def getInfo():
        while True:
            # print(MCAST_GRP,MCAST_INFO_PORT)
            frame,_= info_client_socket.recvfrom(BUFF_SIZE)
            new_frame = pickle.loads(frame)
            time.sleep(0)
            print(new_frame)
    ti = threading.Thread(target=getInfo, args=())
    ti.start()
    time.sleep(0.0175)


# taudio_S1= threading.Thread(target=audio_stream_UDP, args=('239.191.1.1', 5432))
# tinfo_S1= threading.Thread(target=info_stream_UDP, args=('239.192.1.1',5007))
# taudio_S1.start()
# tinfo_S1.start()




# def info_stream_UDP(MCAST_GRP, MCAST_INFO_PORT):
#     print("This is Information Stream")
#     print("You are tuned at", MCAST_GRP, "on the port -", MCAST_INFO_PORT)


def Station1_get_audio():
    audio_stream_UDP(MCAST_GRP_S1, MCAST_PORT_S1)
    print("Station 1 working")


def Station1_get_info():
    info_stream_UDP(MCAST_GRP_S1, MCAST_INFO_PORT_S1)


def Station2_get_audio():
    audio_stream_UDP(MCAST_GRP_S2, MCAST_PORT_S2)
    print("Station 2 chalu")


def Station2_get_info():
    info_stream_UDP(MCAST_GRP_S2, MCAST_INFO_PORT_S2)


def UserInputMenu(numberOfStation):
    printMenu()
    while True:
        user_input = input()
        if user_input == "P":
            Station1 = False
            Station2 = False
            print("Pausing Stream")
            if Station1_get_audio_thread.is_alive():
                Station1_get_audio_thread.terminate()
                Station1_get_info_thread.terminate()
                Station1 = True
            elif Station2_get_audio_thread.is_alive():
                Station2_get_audio_thread.terminate()
                Station2_get_info_thread.terminate()
                Station2 = True

        elif user_input == "R":
            print("Restarting Stream")
            if Station1:
                Station1_get_audio_thread.start()
                Station1_get_info_thread.start()
            elif Station2:
                Station2_get_audio_thread.start()
                Station2_get_info_thread.start()

        elif user_input == "C":
            if Station1_get_audio_thread.is_alive():
                print("Station1 is alive, closing it")
                Station1_get_audio_thread.terminate()
                Station1_get_info_thread.terminate()
                Station2_get_audio_thread.start()
                Station2_get_info_thread.start()
            elif Station2_get_audio_thread.is_alive():
                print("Station2 is alive, closing it")
                Station2_get_audio_thread.terminate()
                Station2_get_info_thread.terminate()
                Station1_get_audio_thread.start()
                Station1_get_info_thread.start()
            else:
                ("You are not connected to a Station right Now")
            print("What station do you want to connect to?")
            StationListGreetings()
            UserChooseStation(numberOfStation)

        elif user_input == "X":
            print("Exiting from Program")
            exit(1)
        else:
            print("Invalid Option in Menu")
            

Station1_get_audio_thread = multiprocessing.Process(target=Station1_get_audio())
Station1_get_info_thread = multiprocessing.Process(target=Station1_get_info())
Station2_get_audio_thread = multiprocessing.Process(target=Station2_get_audio())
Station2_get_info_thread = multiprocessing.Process(target=Station2_get_info())

def UserChooseStation(numberOfStation):
    user_input = int(input("Enter your Station Number: "))
    if user_input in range(1, numberOfStation + 1):
        print("You have chosen a valid Station!")
        if user_input == 1:
            Station1_get_audio_thread.start()
            Station1_get_info_thread.start()

        elif user_input == 2:
            Station2_get_audio_thread.start()
            Station2_get_info_thread.start()
    else:
        print("Error: Enter a Valid Number!")


SiteGreetings()
StationListGreetings()
UserChooseStation(numberOfStation)

user_thread = multiprocessing.Process(target=UserInputMenu, args=(numberOfStation))
user_thread.start()
