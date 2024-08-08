'''
main.py: controller initialisation and main loop
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
import machine
import time
import games
from thumbstick import Thumbstick
from display import Display, MenuDisplay
from comms import Comms
import drive
from config import *

# Connections
# - Red Y-conn from ESP 3.3 to Disp VCC, thumbstick +5V
# - Black triple Y-conn from ESP G to Disp GND, thumbstick GND and bare end to charge board output
# - Orange from ESP GPIO10 to thumbstick SW
# - White from ESP GPIO0 to thumbstick VRx
# - Brown from ESP GPIO1 to thumbstick VRy
# - Blue from ESP GPIO8 to display SDA
# - Purple from ESP GPIO9 to display SCL

# Power: (NB ensure 5V output on step-up board)
# - Black from batt to B1
# - Red from batt to B+
# - Black from Y-conn to -
# - Red from + to Switch
# - Red from Switch to ESP 5V

# Comms Constants
# TODO ROBOT_MAC and CONTROLLER_MAC should be in config
#ROBOT_MAC = "98:F4:AB:D7:74:5D"
#CONTROLLER_MAC = "48:CA:43:C9:BB:B0"
PING_TIMEOUT = 10

SCL_PIN = 9
SDA_PIN = 8
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 32

JOY_X_PIN = 0 # ESP32-C3: GPIO0/A0
JOY_Y_PIN = 1 # ESP32-C3: GPIO1/A1
JOY_BTN_PIN = 10 # ESP32-C3: GPIO10

PAIRING_MODE = False

CONFIG_PATH = "controller.cfg"

def handle_button():
    pass
    
def recv_msg(sender, msg):
    """ Processes a message received by ESP_NOW.
    
    Arguments:
    sender -- the sender of the message
    msg -- the message content
    """
    global motor_left, motor_right, kicker, rgb, PAIRING_MODE, ROBOT_MAC, game_msg
    if PAIRING_MODE or (ROBOT_MAC is None):
        print("Pairing Req: {}-{}".format(sender, msg))
        bits = msg.split("|")
        if len(bits) == 3:
            if bits[1] == "0":                
                ROBOT_MAC = bits[2]
                print("Pairing with {}".format(ROBOT_MAC))
                PAIRING_MODE = False
        else:
            print("Invalid pairing request received")
        # TODO save robot MAC address
        # TODO send X|1|<mac> to confirm claim of robot pairing
    elif sender[2:] == ROBOT_MAC[2:]: # check message is from our robot
        bits = msg.split("|")
        if msg == "P|1":
            global ponged
            ponged = True
        elif bits[0] == "G":
            # game-related message
            game_msg = msg
        else:
            print("Unknown message received: {}".format(msg))
    else:
        print("Msg from unexpected sender: {} [{}]".format(sender, msg))

cfg = Keys(CONFIG_PATH)
com = Comms(recv_msg)
CONTROLLER_MAC = cfg.get("CONTROLLER_MAC", None)
actual_mac = com.get_mac()
if actual_mac != CONTROLLER_MAC:
    CONTROLLER_MAC = actual_mac
    cfg.setval("CONTROLLER_MAC", CONTROLLER_MAC)
    cfg.save()
ROBOT_MAC = cfg.get("ROBOT_MAC", None)


if not ROBOT_MAC is None:
    com.add_peer(ROBOT_MAC)

print("Mac Address: {}".format(com.get_mac().replace(":", "")))

joy = Thumbstick(JOY_X_PIN, JOY_Y_PIN, JOY_BTN_PIN, handle_button, x_zones=3,y_zones=3)
disp = Display(SCL_PIN, SDA_PIN, DISPLAY_WIDTH, DISPLAY_HEIGHT)
disp.showtext([
    "RoboFootball 0.1",
    com.get_mac().replace(":", ""),
    "Btn to start"
])
joy.wait_for_button()

main_menu_items = [
    "Drive",
    "Set Colour",
    "Cal Motors",
    "Cal Joy",
    "Test Joy",
    "Ping Bot",
    "Kicker",
    "Reaction Game",
    "Autopair"
]
kicker_menu_items = [
    "Up",
    "Down",
    "Kick",
    "Exit"
]
colour_menu_items = [
    "Red",
    "Orange",
    "Yellow",
    "Green",
    "Aqua",
    "Blue",
    "Pink",
    "Purple",
    "White",
    "Black"
]
game_menu_items = [
    "Single Player",
    "Net: Host",
    "Net: Client"
]
colour_rgb_values = {
    "Red": (255,0,0),
    "Orange": (255,63,0),
    "Yellow": (255,160,0),
    "Green": (0,255,0),
    "Aqua": (0,255,255),
    "Blue": (0,0,255),
    "Pink": (255,63,200),
    "Purple": (255,0,255),
    "White": (255,255,255),
    "Black": (0,0,0)
}


main_menu = MenuDisplay(disp, main_menu_items, selected=0, offset=0, num_lines=3, num_cols=16)
colour_menu = MenuDisplay(disp, colour_menu_items, selected=0, offset=0, num_lines=3, num_cols=16)
kicker_menu = MenuDisplay(disp, kicker_menu_items, selected=0, offset=0, num_lines=3, num_cols=16)
game_menu = MenuDisplay(disp, game_menu_items, selected=0, offset=0, num_lines=3, num_cols=16)


if not joy.load_calibration():
    joy.calibrate_stick()
    joy.save_calibration()

ping_start = 0
ponged = False

game_msg = ""

while True:
    (selected_id, selected_name) = joy.select(main_menu)
    if selected_name == "Drive":
        # TODO
        fn = "Drive Mode"
        #joy = Thumbstick(JOY_X_PIN, JOY_Y_PIN, JOY_BTN_PIN, handle_button, x_zones=7,y_zones=7)
        #joy.load_calibration()
        drive.drive(joy, disp, cfg, com)
        joy.wait_for_button()
    elif selected_name == "Set Colour":
        (id, sel_colour) = joy.select(colour_menu)
        disp.clearscreen()
        disp.showtext(["Selected Colour:", "--------------", sel_colour])
        clr = colour_rgb_values[sel_colour]
        msg = "F|{}|{}|{}".format(clr[0], clr[1], clr[2])
        com.send(ROBOT_MAC, msg)
    elif selected_name == "Cal Motors":
        drive.calibrate_motors(joy, disp, cfg, com)    
    elif selected_name == "Cal Joy":
        # TODO
        fn = "Cal Joystick"
        disp.clearscreen()
        disp.showtext([fn, "--TODO--", "Btn to exit"])
        joy.wait_for_button()
    elif selected_name == "Test Joy":    
        joy.test(disp)
    elif selected_name == "Ping Bot":
        ping_start = time.ticks_ms()
        ponged = False
        
        # send ping
        msg = "P|0"
        disp.clearscreen()
        disp.showtext(["Ping...", "-- {}s timeout".format(PING_TIMEOUT), ""])
        com.send(ROBOT_MAC, msg)
        # wait for pong
        pong_time = time.ticks_diff(time.ticks_ms(), ping_start)
        com.check_messages(timeout=PING_TIMEOUT*1000)
        
        if ponged:
            disp.clearscreen()
            disp.showtext(["Ping...", "PONG! {}ms".format(pong_time), "Btn to exit"])
        else:
            disp.clearscreen()
            disp.showtext(["Ping...", "Timed out", "Btn to exit"])
            
        time.sleep(0.2)
        joy.wait_for_button()
    elif selected_name == "Kicker":
        (id, sel_action) = joy.select(kicker_menu)
        while (sel_action != "Exit"):
            if sel_action == "Up":
                msg = "K|U"
            elif sel_action == "Down":
                msg = "K|D"
            else:
                msg = "K|K"
                
            com.send(ROBOT_MAC, msg)
                
            (id, sel_action) = joy.select(kicker_menu)
    elif selected_name == "Reaction Game":
        (id, sel_game) = joy.select(game_menu)
        if sel_game == "Single Player":
            games.reaction(joy, disp)
        elif sel_game == "Net: Host":
            games.nethost(joy, disp, cfg, com)
        elif sel_game == "Net: Client":
            games.netclient(joy, disp, cfg, com)
        else:
            print("Invalid reaction game option ({}:P{}.".format(id, sel_game))
    elif selected_name == "Autopair":
        PAIRING_MODE = True
        ROBOT_MAC = None
        disp.clearscreen()
        disp.showtext(["Pairing", "> Switch on", "> unpaired robot"])
        while ROBOT_MAC == None:
            com.check_messages(50)
        # save the robot's mac address
        print("Saving Robot Mac {}".format(ROBOT_MAC))
        cfg.setval("ROBOT_MAC", ROBOT_MAC)
        cfg.save()
        # claim the robot
        com.add_peer(ROBOT_MAC)
        msg = "X|1|{}".format(CONTROLLER_MAC)
        com.send(ROBOT_MAC, msg)
