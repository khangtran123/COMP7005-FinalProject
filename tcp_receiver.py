'''
File: tcp_client.py
Date: November 9, 2017
Designers: Huu Khang Tran, Anderson Phan
Description: This is the client/reciever machine where it will recieve packets
             that were sent from the transmitter. In return, it will send acks
             to the emulator and from there, gets relayed back to the transmitter. 
'''
import config_file
from tcp_transmitter import Client
from packetClass import *
from udp_conn import *

#This class will inherit all the characterisitcs/attributes from the abstract class 
#Client in tcp_transmitter.py --> sole purpose is to recieve packets
class Receiver(Client):
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
        #this inherits the instance of the object declared in Client and sets the mode
        Client.__init__(self,mode)
        self.config = config_file
        self.sequence_num = 0
        self.acked_list = []
        
    def receive(self):
        self.start_udp_connection(self.config.recv_port)
        self.recv_sot() #as a receiver --> listen and wait for SOT pkt
        self.packets_recv = True #this boolean stays true when recv all incoming pkts
        
        packets_recv = 0 #will be referenced as a counter to see total pkts recv
        packets_dup = 0 #will be used when checking for duplicate pkts being sent over to check if it's a retransmission
        
        while packets_recv:
            #now we want to read in each packet recv by calling get_packets in udp_conn
            #self.listen was initallized in Client --> tcp_transmitter.py
            packet_info = udp_conn.get_packet(self.listen)
            packet_type = packet_info.get_packet_type()
            print 'Recieving Packets:'
            print 'Incoming Packet --> ' + packet_info
            
            #check to see if an EOT packet was sent during this transmission
            if packet_type == 3:
                print 'End of incoming packet transmission from Transmitter'
                print 'Packet Diagnostics:'
                print ' '
                print 'Total Packets Received: {0}'.format(packets_recv)
                print 'Total Duplicate Packets Received: {0}'.format(packets_dup)
                
                #now that all packets were recv, packets_recv becomes false
                #this means all client is done receiving all packets
                self.packets_recv = False
                break #now we break out of this while loop
                
            #If regular packet was received    
            elif packet_type == 1:
                #update current sequence num
                self.sequence_num = packet_info.sequence_num
                ack = self.make_packet(2) #State 2 = ACK
                
                #send_packet was defined in abstract class Client as we inherited it
                self.send_packet(ack)
                print 'ACK sent'
                
                #now we want to add a check to see if the packet has an ACK stamp
                if not self.ack_stamped(packet_info.sequence_num):
                    packets_recv +=1
                else:
                    #if duplicated ACK received
                    packets_dup += 1
        
        #now we add all the acked packets sent out to this list/array
        self.acked_list.append(packet_info)
        
    def ack_stamped(self,sequence_num):
        for i in range(0,len(acked_list)):
            #this does the check for each packet in this list to see if the
            #sequence num (pkt in list) matches with given sequence_num
            if self.acked_list[i].sequence_num == sequence_num:
                return True
            else:
                return False
            
    def recv_sot(self):
        data_sot = udp_conn.get_packet(self.listen)
        
        if data_sot.get_packet_type() == 1:
            print 'Received Packet: SOT'
            packet_info = self.make_packet(0)
            self.send_packet(packet_info)
        else:
            #if not SOT then continue on
            self.recv_sot()
            
    #this function passes all config defined packet attributes into packet_information from the packetClass
    def make_packet(self, packet_type):
        return packetClass.CreatePacket.packet_information(self.config.transmitter_addr, \
        self.config.transmitter_port, self.config.recv_addr, self.config.recv_port, \
        self.sequence_num, packet_type, self.sequence_num, self.config.window_size)
'''
def Main():
    
    host = raw_input("Enter the Transmitter IP address: ")
    port = 7005
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    
    option = raw_input("Would you like to begin the packet transfer process (press 'q' to quit, or 'y' to begin)?: ")
    
    if option == 'y' or option == 'Y':
        s.send(option)
        filename = raw_input("What file?: ")
        if filename != 'q':
            s.send(filename)
            data = s.recv(1024)
            if data[:10] == 'File Exist':
                filesize = long(data[10:]) #this takes in the first 10 characters in the data recieved 
                msg = raw_input("File exists: " + str(filesize) + " bytes. Would you like to download it? (y/n): ")
                if msg == 'y' or msg == 'Y':
                    s.send('Send')
                    file = open(filename, 'wb') 
                    fileContent = s.recv(1024)
                    totalLenRecv = len(fileContent)
                    file.write(fileContent)
                    #this while loop represents if total length is more than 1024 bytes
                    #continue to recieve data and then increment/add more to the 
                    #data contents --> then prepare to write it to file
                    #This while condition iterates through entire file byte-to-byte and writes it to a file created in that directory
                    while totalLenRecv < filesize:
                        data = s.recv(1024)
                        totalLenRecv += len(data) 
                        file.write(data)
                        print "{0:.2f}".format((totalLenRecv/float(filesize)))*100 + "% done"
                    print "Download Complete"
                    s.send('Transfer Complete!')
                    s.send("Client is now disconnected")
                    s.close()
                else:
                    print "File Download Cancelled! Disconnecting now"
                    s.close()
            else:
                exist = s.recv(1024)
                print exist
                s.close()
                
    elif option == 'send':
        s.send(option)
        filename = raw_input("What file do you want to send?: ")
        #This condition checks to see if file exists, if it does, sends the file descriptor to server and asks server permission to send file
        #and if server wants to download, it will send a response back to the client and from there, client will proceed to read every byte of the file
        #and sends it off to server to process
        if os.path.isfile(filename):
            s.send(filename)
            s.send("File Ready" + str(os.path.getsize(filename)))
            serverResponse = s.recv(1024)
            if serverResponse == 'Send':
                with open(filename,'rb') as f:
                    bytesToSend = f.read(1024)
                    s.send(bytesToSend)
                    while bytesToSend != "":
                        bytesToSend = f.read(1024) ##binds the bytes together to send
                        s.send(bytesToSend)
            else:
                s.send("File doesn't exist!")
        else:
            #condition is true if file doesn't exist in current directory 
            print "File Transfer Incomplete --> File doesn't exist"
            s.close()
            
    elif option == 'q':
        s.send(option)
        print "Closing the connection now!"
        s.close()
            
        
if __name__ == "__main__":
    Main()'''
    
