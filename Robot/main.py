'''
main.py: robot initialisation and main loop
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
from motor import Motor, PWMMotor
from time import sleep
import time
from machine import I2C, Pin
import machine
from fx import *
from servo import Servo, Kicker
from comms import Comms
from config import *


# Constants
CONFIG_PATH = "robot.cfg"
BROADCAST_MAC = "FF:FF:FF:FF:FF:FF"
#BROADCAST_MAC = "98:F4:AB:D7:74:5D"

# Pin Constants
MOTOR_LEFT_PIN1 = 14
MOTOR_LEFT_PIN2 = 12
MOTOR_LEFT_REVERSE = False
MOTOR_RIGHT_PIN1 = 13
MOTOR_RIGHT_PIN2 = 15
MOTOR_RIGHT_REVERSE = True

KICKER_PIN = 5
KICKER_FREQ = 50
KICKER_REST_ANGLE = 180 # servo mounted to right facing forward
KICKER_KICK_ANGLE = 90

# RGB_PIN = 2
       
def recv_msg(sender, msg):
    """Processes and actions controller message received by ESP_NOW.
    
    Arguments:
    sender -- the sender of the message
    msg -- the message content
    """
    global motor_left, motor_right, kicker, rgb, com, CONTROLLER_MAC
    
    if (sender == CONTROLLER_MAC) or (CONTROLLER_MAC is None): # no hostile traffic!
        print("Received: {}".format(msg))
        bits = msg.split("|")
        if bits[0] == "S": # set speed
            print("speed {}".format(msg))
            speed_l = int(bits[1]) # -255 - 255 from remote
            speed_r = int(bits[2]) # -255 - 255 from remote
            
            if speed_l < 0:
                motor_left.reverse()
            else:
                motor_left.forward()
            if speed_r < 0:
                motor_right.reverse()
            else:
                motor_right.forward()
            
            motor_speed_l = int((abs(speed_l)/255)*1024)
            motor_left.setspeed(motor_speed_l)
            motor_speed_r = int((abs(speed_r)/255)*1024)
            motor_right.setspeed(motor_speed_r)
            print("speed l:{} r:{}".format(motor_speed_l, motor_speed_r))
        elif bits[0] == "K": # kick
            if len(bits) == 2:
                action = bits[1]
                if action == "K":
                    kicker.kick()
                elif action == "U":
                    kicker.up()
                elif action == "D":
                    kicker.down()
            else:
                print("Malformed kick command: {}".format(msg))
        elif bits[0] == "F": # fill LEDs
            # eg F|255|127|0
            if len(bits) == 4:
                r = int(bits[1])
                g = int(bits[2])
                b = int(bits[3])
                rgb.fill( (r,g,b) )
            else:
                print("Malformed fill command: {}".format(msg))
            
        elif bits[0] == "I": # individual LEDs
            pass # TODO
        elif bits[0] == "D": # diplay a pattern
            pass # TODO
        elif bits[0] == "P": # ping received
            print("Ping received")
            msg = "P|1"
            com.send(CONTROLLER_MAC, msg)
        elif bits[0] == "X": # pairing message received
            action = bits[1]
            if action == "1": # pairing
                CONTROLLER_MAC = bits[2]
                com.add_peer(CONTROLLER_MAC)
                msg = "X|2|{}|{}".format(ROBOT_MAC, CONTROLLER_MAC)
                com.send(BROADCAST_MAC, msg)
            # TODO: confirm this is an X|1 pairing message
            # set the controller value
            # send X|2|<robot mac>|<controller mac>

    else:
        print("Invalid sender: {}".format(sender))

def autopair(com):
    global CONTROLLER_MAC
    my_mac = com.get_mac()
    
    #com.add_peer(BROADCAST_MAC) # add broadcast
    last_bcast = 0
    while CONTROLLER_MAC is None:
        # send pairing message every 10 sec
        #if time.ticks_diff(time.ticks_ms(), last_bcast) > 10000:
        msg = "X|0|{}".format(my_mac)
        print("Sending {}".format(msg))
        com.send(BROADCAST_MAC, msg)
        last_bcast = time.ticks_ms()
        com.check_messages(10000)
        
# ------------------------------------------------------------
# Initialise hardware/comms
# ------------------------------------------------------------
# System
machine.freq(80000000)

# Network Comms
com = Comms(recv_msg)
print("Mac Address: {}".format(com.get_mac()))

# Drive Motors
motor_left = PWMMotor(MOTOR_LEFT_PIN1,MOTOR_LEFT_PIN2, MOTOR_LEFT_REVERSE)
motor_right = PWMMotor(MOTOR_RIGHT_PIN1,MOTOR_RIGHT_PIN2, MOTOR_RIGHT_REVERSE)
motor_left.stop()
motor_right.stop()

# RGB    
rgb = RGB()

# Config
cfg = Keys(CONFIG_PATH)
ROBOT_MAC = cfg.get("ROBOT_MAC", None)
if ROBOT_MAC == None:
    ROBOT_MAC = com.get_mac()
    cfg.setval("ROBOT_MAC", ROBOT_MAC)
    cfg.save()
CONTROLLER_MAC = cfg.get("CONTROLLER_MAC", None)
if CONTROLLER_MAC != None:
    com.add_peer(CONTROLLER_MAC)
else:
    # autopairing
    rgb.fill(YELLOW) # yellow leds indicate autopairing
    autopair(com)
    cfg.setval("CONTROLLER_MAC", CONTROLLER_MAC)
    cfg.save()
    
rgb.fill((127,127,127)) # white leds indicate good to go


# Kicker
kicker = Kicker(KICKER_PIN, KICKER_FREQ, KICKER_REST_ANGLE, KICKER_KICK_ANGLE)


while True:
    com.check_messages()


