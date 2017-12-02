'''
File: config_file.py
Date: November 12, 2017
Designers: Huu Khang Tran, Anderson Phan
Description: This is the config file that both transmitter and receiver will
             be referencing from.
'''

# Max number of packets we want to send over: 15 packets
# Max Window Size: 5
# Max Timeout (ms): 2000
# Sender Port: 7005
# Receiver Port: 7006 

emulator_addr = "192.168.0.3"
emulator_port = "7007"
transmitter_addr = "192.168.0.2"
transmitter_port = "7005"
recv_addr = "192.168.0.1"
recv_port = "7006"
max_pkt_transfers = "500"
max_packet_len = "1024"
dropped_packets = "2"
delayed_packet_time = "2" #2 seconds
window_size = "5" '''Window size --> file size '''
max_timeout = "2000"

