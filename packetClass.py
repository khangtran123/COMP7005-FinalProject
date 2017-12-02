'''
File: packetClass.py
Date: November 9, 2017
Designers: Huu Khang Tran, Anderson Phan
Description: This is the packet class that contains all of the attributes of 
             a packet structure. 
'''

class PacketStruct():
    '''
    __init__ is considered a constructor just like in Java.
    self represents the instance of that object we declared 
    this constructor will be our base of what a packet should include. Contains 
    no return type, but only called when a new instance of an object is created.
    
    packet_type(0) = SOT (Start-of-Transmission)
    packet_type(1) = Data
    packet_type(2) = ACK
    packet_type(3) = EOT (End-of-Transmission)
    '''
    def __init__(self):
        self.packet_type = 0 
        self.sequence_num = 0
        self.packet_data = '' #this is a char type and must be null
        self.window_size = 0
        self.ack_num = 0
        self.source_addr =''
        self.destination_addr = ''
        self.source_port = 0
        self.destination_port = 0
        self.packet_len = 0
    '''
    Now we're setting up our getters 
    '''
    def get_packet_type(self):
        return self.packet_type
    
    def get_sequence_num(self):
        return self.sequence_num
    
    def get_packet_data(self):
        return self.packet_data
    
    def get_window_size(self):
        return self.window_size
    
    def get_ack_num(self):
        return self.ack_num
    
    def get_source_addr(self):
        return self.source_addr
    
    def get_destination_addr(self):
        return self.destination_addr
    
    def get_source_port(self):
        return self.source_port
    
    def get_destination_port(self):
        return self.destination_port
    
    def get_packet_len(self):
        return self.packet_len
    
    '''
    now we want to set our setters
    '''
    def set_packet_type(self, packet_type):
        self.packet_type = packet_type
    
    def set_sequence_num(self, sequence_num):
        self.sequence_num = sequence_num
    
    def set_packet_data(self, packet_data):
        self.packet_data = packet_data
    
    def set_window_size(self, window_size):
        self.window_size = window_size
    
    def set_ack_num(self, ack_num):
        self.ack_num = ack_num
    
    def set_source_addr(self, source_addr):
        self.source_addr = source_addr
    
    def set_destination_addr(self, destination_addr):
        self.destination_addr = destination_addr
    
    def set_source_port(self, source_port):
        self.source_port = source_port
    
    def set_destination_port(self, destination_port):
        self.destination_port = destination_port
        
    def set_packet_len(self, packet_len):
        self.packet_len = packet_len
    
    #now we set a constructor that returns the string format of the pkt
    #going in order of the getters and setters in terms of pkt_attributes
    def __str__(self):
        pkt_string = ''' Packet [packet_type={0}, sequence_num={1}, packet_data={2}
                                 window_size={3}, ack_num={4}, source_addr={5},
                                 destination_addr={6}, source_port={7},
                                 destination_port={8}, packet_len={9}]'''.format(self.packet_type,  
                                self.sequence_num, self.packet_data, self.window_size,
                                self.ack_num, self.source_addr, self.destination_addr,
                                self.source_port, self.destination_port, self.packet_len)
        
        return pkt_string

'''
Class - create_packet is the main class that handles the function "packet"
'''
class CreatePacket():
    def packet_information(source_addr, source_port, destination_addr, \
    destination_port, sequence_num, pkt_type, ack_num, window_size, packet_len):
        
        pkt = Packet_Struct() #now we call on the class Packet_Struct that we created above
        
        pkt.set_source_addr(source_addr)
        pkt.set_source_port(source_port)
        pkt.set_destination_addr(destination_addr)
        pkt.set_destination_port(destination_port)
        pkt.set_sequence_num(sequence_num)
        pkt.set_ack_num(ack_num)
        pkt.set_window_size(window_size)
        if pkt_type == 0:
            pkt.set_packet_data('SOT')
        elif pkt_type == 1:
            ##that means this is a regular datagram/packet so each pkt needs 
            ## a unique sequence_num
            pkt.set_packet_data('SEQ {0}'.format(sequence_num)) ##needs reconstruction as this will represent the actual data packet
        elif pkt_type == 2:
            pkt.set_packet_data('ACK {0}'.format(ack_num))
            '''
            ACK {0} --> will always increment when client sends it back
            .format is used to customize the {0} into string format and adds
            ack_num as an argument
            '''
        elif pkt_type == 3:
            pkt.set_packet_data('EOT')
        pkt.set_packet_len(packet_len)
        #now we spit back the packet we have just desgned
        return pkt