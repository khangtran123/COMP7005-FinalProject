'''
File: running_tcp_receiver.py
Date: November 25, 2017
Designers: Huu Khang Tran, Anderson Phan
Description: This is the main file that will run the receiver by referencing
the receive function in the Receive class --> tcp_receiver.py. 
'''

from tcp_receiver import *

def Main():
    
    #must be in a try-catch block to make sure we handle unhandled exceptions
    try:
        client_receive = Receiver(2) #2 represents the client mode --> 2 => receiver
        client_receive.what_are_you() #function defined in client.py
        print 'Receiver Server is now Online'
        
    except (keyboardInterrupt, SystemExit):
        raise 
        #used for raising unhandled exception errors and is a more efficient way
        #of handling situations where the user wants to stop the receiver
    except:
        print 'Receiver Server is now Offline due to an interruption in session'

        
if __name__ == "__main__":
    Main()