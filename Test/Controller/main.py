import time
from comms import Comms

def mac_to_int(mac):
    return int(mac.replace(":", ""), 16)

# Setup ESPNOW
com = Comms(None) # parameter is message handler - we are only sending
print("Mac Address: {}".format(com.get_mac()))
bot_addr = '98:F4:AB:D7:74:5D'

while True:
    print("sending L")
    com.send(bot_addr, 'L')
    time.sleep(1)
    print("sending R")
    com.send(bot_addr, 'R')
    time.sleep(1)
           
