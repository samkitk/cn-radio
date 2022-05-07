import pickle,pprint
from time import sleep

class site_info:
    type = 10
    site_name = 'Welto Internet Radio'
    site_name_size = len(site_name)
    site_desc = 'Please choose one of the Radio Station: \n 1. RedFM \n 2. LoveFM'
    site_desc_size = len(site_desc)
    radio_stn_count = 2
    class radio_stn1_info:
        radio_stn_number = 1
        radio_stn_name_size = 5
        radio_stn_name = 'RedFM'
        multicast_address = '224.1.1.1' 
        data_port = 5432 
        info_port = 5049 
        bit_rate = 234 
    class radio_stn2_info:
        radio_stn_number = 2
        radio_stn_name_size = 6
        radio_stn_name = 'LoveFM'
        multicast_address = '224.1.1.1' 
        data_port = 5432 
        info_port = 5049 
        bit_rate = 234 

site_info_pickled = pickle.dumps(site_info)

class song_info:
    type = 12
    song_name = 'Tum Hi Ho'
    song_name_size = len(song_name)
    remaining_time_in_sec = 268
    next_song_name = 'Mein Rang Sharbaton Ka'
    next_song_name_size = len(next_song_name)

song_info_pickled = pickle.dumps(song_info)




#while (1):
    ###sendto codes for stn1
 #   sleep(20)
    ###sendto codes for stn2
  #  sleep(20)
    

    
    #print('PICKLE: {!r}'.format(picklestring))

#unpicklestring = pickle.loads(picklestring)
#pprint.pprint(unpicklestring)


#for i in unpicklestring:
 #   print(i,unpicklestring[i])
