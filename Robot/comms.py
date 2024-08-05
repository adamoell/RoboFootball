'''
comms.py: ESP-NOW based network communications
Copyright (C) 2024 by Adam Oellermann (adam@oellermann.com)
--------------------------------------------------------------------------------
This file is part of RoboFootball.

RoboFootball is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

RoboFootball is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
RoboFootball. If not, see <https://www.gnu.org/licenses/>.
'''
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
        network.WLAN(network.AP_IF).active(False)
        self.sta.active(True)
        if self.sta.active():
            mac = self.sta.config("mac")
            self.mac_address = mac2string(mac)
            
        self.sta.disconnect() # for ESP8266
        self.esp = espnow.ESPNow()
        self.esp.active(True)
        
    
    def add_peer(self, peer):
        print("Adding {}".format(peer))
        self.esp.add_peer(string2mac(peer))
    
    def get_mac(self):
        return(self.mac_address)
    
    def check_messages(self, timeout=None):
        sender, msg = self.esp.recv(timeout)
        if msg:
            if self.msg_handler != None:
                self.msg_handler(mac2string(sender), msg.decode("utf-8"))
            else:
                print("msg: {}".format(msg))
        else:
            print("-")
            
    def send(self, dest, msg):
        mac = string2mac(dest)
        try:
            self.esp.send(mac,msg)
        except:
            print("Error sending message {} << [{}]".format(dest, msg))
    
