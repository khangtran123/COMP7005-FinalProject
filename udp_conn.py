import pickle
import socket

from packetClass import PacketStruct #we import this to get the sent packet attributes

class UDP:
    
    #This function is to start up the UDP server
    def server(port):
        #SOCK_STREAM: Connection based protocol for TCP, where two parties are communicating over the channel until one of the parties closes the network.
        #SOCK_DGRAM: Datagram-based protocol for UDP. Send one datagram, connection terminates
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        #host is configured to 0.0.0.0 which is localhost. Server can be run on any machine
        host = '0.0.0.0'
        s.bind((host, port))
        return s
    
    #This function is to create a UDP socket
    def create_socket():
        s = socket.socket(AF_INET, socket.SOCK_DGRAM)
        return s
    
    #This function is to read the incoming packet
    def get_packet(socket):
        data = socket.recv(1024)
        pkt = pickle.loads(data)
        return pkt
    
    #This function is to send out a packet with the fact that it must have a 
    #destination address and destination port specified.
    def send_packet(socket, pkt, destination_addr = None, destination_port = None):
        #None is equivalent to null in Java
        if destination_addr != None:
            '''
                pickle is the library we imported over
                dumps: serialize the object
                loads: de-serializes the object
                socket.sendto(string, flags, address) --> built in library funct that sends data to the socket
            '''
            data = pickle.dumps(pkt)
            socket.sendto(data, (destination_addr,destination_port))
        else:
            data = pickle.dumps(pkt)
            #if destination addr and port is not specified or null, call the getter
            #methods to get the addr and port
            socket.sendto(data, (pkt.get_destination_addr(),pkt.get_destination_port()))


