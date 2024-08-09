'''
drive.py: functions to control driving of the robot
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
import time
from drive_map import *

JOY_BTN_DEBOUNCE = 300
JOY_X_DEBOUNCE = 300
JOY_Y_DEBOUNCE = 300

def calibrate_motors(joy, disp, cfg, com):
    REVERSER_L = int(cfg.get("REVERSER_L", default="1"))
    REVERSER_R = int(cfg.get("REVERSER_R", default="1"))
    ROBOT_MAC = cfg.get("ROBOT_MAC")
    
    calibration_speed = 30
    
    disp.clearscreen()
    disp.showtext(["Calibrate Motors", "< and > chg dir", "Btn when both fwd"])
    # start motors
    msg = "S|{}|{}".format(calibration_speed*REVERSER_L, calibration_speed*REVERSER_R)
    com.send(ROBOT_MAC, msg)
    
    last_btn = time.ticks_ms()
    last_x = time.ticks_ms()
    last_y = time.ticks_ms()
    # wait for button release
#     while joy.read_button == 0:
#         time.sleep(0.1)
        
    while True:
        (x, y) = joy.read_zone()
        btn = joy.read_button()
        
        if (btn == 0) and (time.ticks_diff(time.ticks_ms(), last_btn) > JOY_BTN_DEBOUNCE):
            # update the configuration
            cfg.setval("REVERSER_L", str(REVERSER_L))
            cfg.setval("REVERSER_R", str(REVERSER_R))
            cfg.save()
            # stop the motors
            com.send(ROBOT_MAC, "S|0|0")
            return()
            
        if (x == -1) and (time.ticks_diff(time.ticks_ms(), last_x) > JOY_X_DEBOUNCE):
            last_x = time.ticks_ms()
            REVERSER_L = REVERSER_L * -1
            msg = "S|{}|{}".format(calibration_speed*REVERSER_L, calibration_speed*REVERSER_R)
            com.send(ROBOT_MAC, msg)
        if (x == 1) and (time.ticks_diff(time.ticks_ms(), last_x) > JOY_X_DEBOUNCE):
            last_x = time.ticks_ms()
            REVERSER_R = REVERSER_R * -1
            msg = "S|{}|{}".format(calibration_speed*REVERSER_L, calibration_speed*REVERSER_R)
            com.send(ROBOT_MAC, msg)
        
def drive(joy, disp, cfg, com):
    REVERSER_L = int(cfg.get("REVERSER_L", default="1"))
    REVERSER_R = int(cfg.get("REVERSER_R", default="1"))
    ROBOT_MAC = cfg.get("ROBOT_MAC")
    
    map_name = cfg.get("JOY_MAP", default="simple_map")
    print("Using map: {}".format(map_name))
    if map_name == "Basic":
        drive_map = simple_map
    elif map_name == "Standard":
        drive_map = default_map
    elif map_name == "Twitchy":
        drive_map = twitchy_map
    elif map_name == "Precision":
        drive_map = precision_map
    else:
        drive_map = simple_map
    
    #drive_map = simple_map
    #drive_map = twitchy_map
    (xz, yz) = drive_map["zones"]
    joy.rezone(x_zones=xz, y_zones=yz)
    last_x = 0
    last_y = 0
    last_btn = time.ticks_ms()
    disp.clearscreen()
    disp.showtext(["Drive Mode", "Joystick to move", "Btn to kick"])
    while True:
        (x, y) = joy.read_zone()
        btn = joy.read_button()
        if (btn == 0) and (time.ticks_diff(time.ticks_ms(), last_btn) > JOY_BTN_DEBOUNCE):
            msg = "K|K"
            com.send(ROBOT_MAC, msg)
            last_btn = time.ticks_ms()
        if last_x != x or last_y != y:
            #print("update: {}|{}".format(x, y))
            last_x = x
            last_y = y
            
            (speed_l, speed_r) = drive_map[(x,y)]

            #print("speed: {}|{}".format(speed_l, speed_r))
            
            msg = "S|{}|{}".format(speed_l*REVERSER_L, speed_r*REVERSER_R)
            com.send(ROBOT_MAC, msg)