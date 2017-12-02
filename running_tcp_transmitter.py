'''
File: running_tcp_receiver.py
Date: November 25, 2017
Designers: Huu Khang Tran, Anderson Phan
Description: This is the main file that will run the transmitter server by referencing
the receive function in the Receive class --> tcp_receiver.py.
'''

def Main():
    #This is where you initialize the transmitter object by referencing the 
    #Transmitter class in client.py
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #host is configured to 0.0.0.0 which is localhost. Server can be run on any machine
    host = '0.0.0.0'
    port = 7005
    s.bind((host, port))

    s.listen(5) #listens up to 5 connections

    print "Server Started"
    while True:

            # we add a condition to compare strings with user argument: 
            # if user typed "y" or "Y", then create_packet is called
            # if user typed "send" then you use a another function to recieve the text file and save it locally
            connectionSocket, clientAddress = s.accept() #accept() starts the connection
            print "The client machine is now connected with an ip address of: " + str(clientAddress)

            #userOption is the data recieved from the client: client is to send data in a string of either 
            #"get", "send", or "q"
            userOption = connectionSocket.recv(1024) 
            if userOption == 'y' or userOption == 'Y': 
                    retrieve_file(connectionSocket)
            elif userOption == 'q':
                    print "Client Disconnected from you!"

    s.close()'''

if __name__ == "__main__":
    Main()
