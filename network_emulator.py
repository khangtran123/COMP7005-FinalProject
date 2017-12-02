'''
File: network_emulator.py
Date: November 10, 2017
Designers: Huu Khang Tran, Anderson Phan
Description: This is the network emulator, which will act as an unreliable channel
             over the packets sent. This means that the emulator relays pkts from
             the transmitter to the reciever and vice versa with acks from client
             to the transmitter. 
'''

import random
import config_file
from udp_conn import *


class Emulator:
    
    def __init__(self):
        self.config = config_file
        
    def start_relay(self):
        #this makes sure that the emulator is always running
        emulator_status = True
        
        #These are all the details neccessary 
        incoming_packets = 0
        dropped_packets = 0
        relayed_packets = 0
    
        s = udp_conn.server(self.config.emulator_port)
        
        print 'Network Emulator is now online'
        
        #while emulator server is online
        while emulator_status:
            packet_info = udp_conn.get_packet(s)
            print 'Recieving Packets:'
            print 'Incoming Packet --> ' + packet_info
            incoming_packets += 1
            print 'Total incoming packets: {0}'.format(incoming_packets)
            
            #remember if it's a SOT or EOT packet, no need to analyze
            if packet_info.get_packet_type() == 0 or packet_info.get_packet_type() == 3:
                print 'Packet is either a SOT or EOT and will be forwarded to Destination Address: {0}, Destination Port: {1}'.format(packet_info.get_destination_addr(), get_destination_port())
                udp_conn.send_packet(s, packet_info, packet_info.get_destination_addr(), get_destination_port())
                relayed_packets +=1
            else:
                #if packet drop rate is lower than the threshold, drop the packet
                if self.BER() <= self.config.dropped_packets:
                    print 'Packet will be dropped!'
                    dropped_packets += 1
                else:
                    '''
                    if packet drop rate is greater than the threshold, transmit the packet
                    but this time we will pause the transmission causing a delay 
                    in packet tranmission  
                    '''
                    time.sleep(self.config.delayed_packet_time)
                    udp_conn.send_packet(s, packet_info, packet_info.get_destination_addr(), get_destination_port())
                    relayed_packets +=1
        
        print 'Total Number of packets sent: {0}'.format(relayed_packets)
        print 'Total Number of packets dropped: {0}'.format(dropped_packets)
    
    #this function determines the bit error rate (BER)
    def BER():
        '''
        Use the random generator from python's random lib
        Range: min (1) : max (100)
        random.randint((max-min) + 1) + 1)
        '''
        threshold = random.randint((100 - 1) + 1) + 1
        return threshold
    
    def emulator_info(self):
        print 'Dropped Packet Rate: {0}'.format(self.config.dropped_packets)
        print 'Avg Delay per Packet (sec): {0}'.format(self.config.delayed_packet_time)
        print 'Transmitter: {0}:{1}'.format(self.config.transmitter_addr, self.config.transmitter_port)
        print 'Emulator: {0}:{1}'.format(self.config.emulator_addr, self.config.emulator_port)
        print 'Receiver: {0}:{1}'.format(self.config.recv_addr, self.config.recv_port)
        
                
                    
        
        

