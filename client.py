'''
File: tcp_server.py
Date: November 9, 2017
Designers: Huu Khang Tran, Anderson Phan
Description: This is the network transmitter (server)where it will send packets
             across the channel to the emulator, and then relayed back to the client.
             This will also recieve acks sent by the client. For this to work, 
             we will be using UDP since we want an un-reliable channel. 
            This is a build up of assign 1 where file transfer is still ongoing. 
'''

import socket 
import os #check if file exists and if a file is indeed a file
import packetClass #this calls on the CreatePacket class in file: packetClass.py
import pickle
from abc import ABCMeta, abstractmethod
from udp_conn import * #want to import all classes and methods defined in udp_conn.py
import config_file
'''
    "pickle" - Used for serializing and de-serializing python objects, which means
    converting objects into a char stream (used to send bytes of packets across
    the network). 
    
    ABCMeta (Abstract Base Class) - Python's implementation of Abstract classes
    that contains one or more abstract methods but contains no implementation.  
'''

class Client:
    #look into Abstract classes and check to see if it's neccessary 
    __metaclass__ = ABCMeta
    
    '''
    __init__ is considered a constructor just like in Java.
    self represents the instance of that object we declared 
    this constructor will be our base of what a packet should include. Contains 
    no return type, but only called when a new instance of an object is created.
    This initializes the transmitter and sets mode at "Transmitter"
    
    now we include abstract methods since the recv and emulator can extend these
    traits of sending packets across the network channel
    '''
    def __init__(self,mode):
        self.config = config_file
        self.mode = mode
    
    # the main state where the transmitter process occurs(whether in sending 
    # or recieving state).
    @abstractmethod
    def state(self):
        pass
    
    # creates the packets
    @abstractmethod
    def create_packet(self, packet_type):
        pass
    
    #This function is to initialize the UDP server and set it's state to wait and listen
    #for incoming packets/sessions
    def start_udp_connection(self,port):
        self.wait = udp_conn.server(port)
    
    #this function sends the packets to the emulator
    def send_packet(self,pkt):
        s = udp_conn.create_socket()
        udp_conn.send_packet(s,pkt,self.config.recv_addr, self.config.recv_port)
        
    def set_trans_config(self, emulator_addr, emulator_port, transmitter_addr, \
    transmitter_port, recv_addr, recv_port, max_pkt_transfers, window_size, \
    max_timeout, packet_len):
        '''
        Now we use the values from config_file.py and set it to the properties
        defined in set_trans_config (Building the transmitter configurations)
        '''
        self.config.emulator_addr = emulator_addr
        self.config.emulator_port = emulator_port
        self.config.transmitter_addr = transmitter_addr
        self.config.transmitter_port = transmitter_port
        self.config.recv_addr = recv_addr
        self.config.recv_port = recv_port
        self.config.max_pkt_transfers = max_pkt_transfers
        self.config.window_size = window_size
        self.config.max_timeout = max_timeout
        self.config.packet_len = packet_len
    
    #once a class, transmitter/receiver is intialized, this will print their
    #current status and characteristics
    def what_are_you(self):
        print 'Who you are: {0}'.format(self.mode)
        
    def get_entity(self):
        return self.mode
    
    def set_entity(self):
        self.mode = mode
    

#This class will inherit all the characterisitcs/attributes from the abstract class 
#Client --> sole purpose is to transmit/send packets
class Transmitter(Client):
    
    # __init__ passes parameters in the second an object gets initialized
    def __init__(self):
        self.sequence_num = 0
        self.window = [] #we declare an array variable "window" which represents the sliding window
        
    #retrieves the file when client makes the request to get a file 
    def create_packet(self):
        self.start_udp_connection(self.config.transmitter_port)
        self.send_sot() #invoke this function
        self.sent_packets = 0 #to keep track of the packets that were sent
        self.unsent_packets = 0 #to keep track of the packets that weren't sent
        
        '''
        Now we create a while loop to make sure we get all ack's back according 
        to the assigned sequence # of the pkt sent out. If the ack,seq matches
        the lowest pkt seq # sent out, we empty the window and shift it to the
        right
        '''
        
        while self.sent_packets < self.config.max_pkt_transfers:
            #now we call on load_window() function to load the window with packets
            self.load_window()
            #wait timer on acks recieved 
            self.ack_recieved = True
            self.set_timeout_time()
            
            #check for acks recieved accoring to the packet sent out
            while len(self.packet_window) != 0:
                if not self.ack_recieved:
                    self.set_timeout_time()
                    print 'Window Status: {0}'.format(len(self.window))
        
        self.sent_packets += self.config.window_size
        #now we need to find out how many packets weren't sent
        self.unsent_packets = self.config.window_size - self.sent_packets
        print 'Sent Packets: {0}'.format(self.sent_packets)
        print 'Unsent Packets: {0}'.format(self.unsent_packets)
        
    def send_sot(self):
        pkt = self.make_packet(0) #State 0 = SOT - Start-of-Transmission
        self.send_packet(pkt)
        recv_response = udp_conn.get_packet(self.wait)
        
        #since we imported the Packet_Struct class from packetClass.py in udp_conn.py
        #we can get all the attributes associated with the packet sent out
        if recv_response.get_packet_type() == 0:
            print "Packet Type: SOT was successfully sent. Ready for data transmission."
            
    def send_eot(self):
        pkt = self.make_packet(3) #State 3 = EOT - End-of_Transmission
        self.send_packet(pkt)
        recv_response = udp_conn.get_packet(self.wait)
        
        if recv_response.get_packet_type() == 3:
            print "Packet Type: EOT was successfully sent. Data transmission terminated."
    
    #this function passes all config defined packet attributes into packet_information from the packetClass
    def make_packet(self, packet_type):
        return packetClass.CreatePacket.packet_information(self.config.transmitter_addr, \
        self.config.transmitter_port, self.config.recv_addr, self.config.recv_port, \
        self.sequence_num, packet_type, self.sequence_num, self.config.window_size, \
        self.config.packet_len)
        
    #this function will now load up the window based on the max window size
    def load_window(self):
        #range() will generate a sequence of numbers from a specific range
        #in this case, we want packets from 1-5 (max window size)
        for i in range(1, self.config.window_size):
            pkt = self.make_packet(1) #State 1 = Data transmission
            self.window.append(pkt) #append is equivalent to array.add() in Java
            #once we load pkt into window, we send it off
            self.send_packet(pkt)
            print "Packet sent"
            #now we increment the sequence num and repeat
            self.sequence_num += 1
    
    #this function checks to see if the acks were recieved accordingly based on 
    #defined packets in the window that was sent out earlier
    def recv_ack_check(self):
        self.stop_timeout_time()
        #we check to see if the window is empty, if not then we resend those packets and wait for ack
        #we get the length of the window size array and see if it's != 0
        if len(self.window_size != 0):
            self.incoming_ack = True
            for i in range(1, len(self.window_size)):
                pkt = self.make_packet(i)
                self.send_packet(pkt)
                print "Packet retransmitted"
                
    def set_timeout_time(self):
        self.timer = True
        
    def stop_timeout_time(self):
        self.timer = False
        self.incoming_ack = False
        
    #function means client wants to send file to another client
    def retrieve_file():
        #newSocket --> we get new connection socket that we passed as an argument to this function from main function.
        filename = newSocket.recv(1024) #takes 1024 bytes

        #this if statement basically checks to see if the filename provided from user exists in the file structure, 
        #if it does, sends the file descriptor to server and asks client permission to send file and if client wants
        #to download, it will send a response back to the server and from there, server will read in every byte of the file
        #and sends it off to the client to process
        if os.path.isfile(filename):
                newSocket.send("File Exist" + str(os.path.getsize(filename))) #get the size of the file
                clientResponse = newSocket.recv(1024)
                if clientResponse[:4] == 'Send':
                        print "Transferring file: " + filename
                        with open(filename,'rb') as f:
                            '''
                            This is where you packetize the file content --> max-len = 1024 Bytes
                            -- call on function create_packet
                            '''
                            bytesToSend = f.read(1024)
                            newSocket.send(bytesToSend)
                            while bytesToSend != "":
                                    bytesToSend = f.read(1024)
                                    newSocket.send(bytesToSend)
                        completed = newSocket.recv(1024)
                        print completed
                        closingReply = newSocket.recv(1024)
                        print closingReply
        else:
                newSocket.send("File doesn't exist!")

    '''
    #this function is called when client wants to send a file to the server
    def get_file(newSocket):
            filename = newSocket.recv(1024)
            data = newSocket.recv(1024)

            if data[:10] == 'File Ready':
                    filesize = long(data[10:])
                    msg = raw_input("Incoming File size:" + str(filesize) + " bytes. Would you like to download it? (y/n): ")
                    if msg == 'y' or msg == 'Y':
                            newSocket.send('Send')
                            #filesizeData = long(newSocket.recv(1024))
                            #filesize = filesizeData
                            print "Client is sending you a file --> Filename: " + filename + ". File size: " + str(filesize) + " 				Bytes!"

                            #print filesize
                            file = open(filename, 'wb')
                            fileContent = newSocket.recv(1024)
                            totalLenRecv = len(fileContent)
                            file.write(fileContent)

                            #this while loop represents if total length is more than 1024 bytes
                            #continue to recieve data and then increment/add more to the 
                            #data contents --> then prepare to write it to file
                            #This while condition iterates through entire file byte-to-byte and writes it to a file created
                            #in that directory
                            while totalLenRecv < filesize:
                                data = newSocket.recv(1024)
                                totalLenRecv += len(data) 
                                file.write(data)
                                print "{0:.2f}".format((totalLenRecv/float(filesize)))*100 + "% done"

                            print "Download Complete"
                    else:
                            print "Did not recieve file!" '''

