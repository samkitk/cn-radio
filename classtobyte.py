import pickle,pprint

radio_stn_info= {'radio_stn_number' : 1, 'radio_stn_name_size' : 20, 'radio_stn_name' : 'RedFM', 'multicast_address' : '224.1.1.1' , 'data_port' : 5432 , 'info_port' : 5049, 'bit_rate' : 234 }
print('Radio_stn_info: ', end = ' ')
pprint.pprint(radio_stn_info)


picklestring = pickle.dumps(radio_stn_info)
print('PICKLE: {!r}'.format(picklestring))

unpicklestring = pickle.loads(picklestring)
pprint.pprint(unpicklestring)


for i in unpicklestring:
    print(i,unpicklestring[i])