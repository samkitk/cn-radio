import socket
import pprint
import pickle

HOST = socket.gethostname()  # The server's hostname or IP address
PORT = 8079  # The port used by the server

# def UserInputMenu():
#     user_input = input()
#     if(user_input=="")





with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # s.sendall(b"1")
    num = 1
    # sep = "\0"
    string = str(num) 
    s.send(string.encode())
    data = s.recv(4096) ##randomly taken 4096
    station_list = pickle.loads(data)
    # print(type(station_list))
    print("======================")
    print("Welcome to",station_list['site_info']['site_name'])
    print("======================")
    print("We have",station_list['site_info']['radio_stn_count'],"station(s) available for you!")
    print(station_list['station1']['radio_stn_number'],"-",station_list['station1']['radio_stn_name'])
    print("Address:",station_list['station1']['multicast_address'])
    print("Info Port:",station_list['station1']['info_port'])
    print("Data Port:",station_list['station1']['data_port'])
    print("BitRate:",station_list['station1']['bit_rate'])
    print("----------------------")
    print(station_list['station2']['radio_stn_number'],"-",station_list['station2']['radio_stn_name'])
    print("Address:",station_list['station2']['multicast_address'])
    print("Info Port:",station_list['station2']['info_port'])
    print("Data Port:",station_list['station2']['data_port'])
    print("BitRate:",station_list['station2']['bit_rate'])