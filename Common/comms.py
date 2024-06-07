# comms.py
import network
import espnow
import binascii

def mac2string(mac):
    macstr = ":".join(["{:02X}".format(byte) for byte in mac])
    return(macstr)

def string2mac(addr):
    macbytes = binascii.unhexlify(addr.replace(':', ''))
    return(macbytes)

class Comms:
    def __init__(self, msg_handler=None):
        # activate wlan
        self.sta = None
        self.msg_handler = msg_handler
        self.activate()

    def activate(self):
        # Setup ESPNOW
        self.sta = network.WLAN(network.STA_IF)
        self.sta.active(True)
        if self.sta.active():
            mac = self.sta.config("mac")
            self.mac_address = mac2string(mac)
            
        self.sta.disconnect() # for ESP8266
        self.esp = espnow.ESPNow()
        self.esp.active(True)
    
    def get_mac(self):
        return(self.mac_address)
    
    def check_messages(self):
        sender, msg = self.esp.recv()
        if msg:
            print(sender)
            print(mac2string(sender))
            if self.msg_handler != None:
                self.msg_handler(mac2string(sender), msg.decode("utf-8"))
            else:
                print("msg: {}".format(msg))
        else:
            print("-")
            
    def send(self, dest, msg):
        mac = string2mac(dest)
        self.esp.send(mac,msg)
        print("sent: {} {}".format(dest,msg))
        
    