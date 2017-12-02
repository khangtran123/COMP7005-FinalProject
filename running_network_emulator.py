'''
File: running_tcp_receiver.py
Date: November 25, 2017
Designers: Huu Khang Tran, Anderson Phan
Description: This is the main file that will run the network emulator server by referencing
the receive function in the Receive class --> tcp_receiver.py. 
'''

from network_emulator import *

def Main():
    
    #must be in a try-catch block to make sure we handle unhandled exceptions
    try:
        emulator = Emulator()
        emulator.start_relay()
        print 'Network Emulator Server is now Online'
        emulator.emulator_info()
    except (keyboardInterrupt, SystemExit):
        raise 
        #used for raising unhandled exception errors and is a more efficient way
        #of handling situations where the user wants to stop the receiver
    except:
        print 'Network Emulator Server is now Offline due to an interruption in session'

        
if __name__ == "__main__":
    Main()