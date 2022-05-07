import socket
import pprint
import pickle
import threading


HOST = socket.gethostname()  # The server's hostname or IP address
PORT = 8072  # The port used by the server

menu_options = {
    "P": 'Pause',
    "R": 'Restart',
    "C": 'Change Station',
    "X": 'Exit',
}

def SiteGreetings(station_list):
    print("======================")
    print("Welcome to",station_list['site_info']['site_name'])
    print("======================")

def StationListGreetings(station_list):
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

def printMenu():
    for i in menu_options.keys():
        print(i,"-->",menu_options[i])

def UserInputMenu(station_list,numberOfStation):
    printMenu()
    while True:
        user_input = input()
        if(user_input=="P"):
            print("Pausing Stream")

        elif(user_input=="R"):
            print("Restarting Stream")

        elif(user_input=="C"):
            print("What station do you want to change to?")
            StationListGreetings(station_list)
            UserChooseStation(numberOfStation)
        
        elif(user_input=="X"):
            print("Exiting from Program")
            exit(1)
        else:
            print("Invalid Option in Menu")

def UserChooseStation(numberOfStation):
    user_input = int(input("Enter your Station Number: "))
    if(user_input in range(1,numberOfStation+1)):
        print("You have chosen a valid Station!")
    else:
        print("Error: Enter a Valid Number!")

def TCP_Socket_Client_to_Server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        # s.sendall(b"1")
        num = 1
        # sep = "\0"
        string = str(num) 
        s.send(string.encode())
        data = s.recv(4096) ##randomly taken 4096
        station_list = pickle.loads(data)
        return station_list

station_list = TCP_Socket_Client_to_Server()
numberOfStation = station_list['site_info']['radio_stn_count']


SiteGreetings(station_list)
StationListGreetings(station_list)
UserChooseStation(numberOfStation)

user_thread = threading.Thread(target=UserInputMenu,args=(station_list,numberOfStation))
user_thread.start()