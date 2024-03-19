# Roboats: control system for robot paddleboats
# Copyright (C) 2021 Adam Oellermann
# adam@oellermann.com
# ----------------------------------------------------------------------
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------
# display.py
# code to control the display
# ----------------------------------------------------------------------
# Connections: 
# OLED <--> ESP8266
# GND  <--> GND
# VCC  <--> 3V
# SCL  <--> D1
# SDA  <--> D2
# ----------------------------------------------------------------------
# See tutorial:
# https://randomnerdtutorials.com/micropython-oled-display-esp32-esp8266/


from machine import Pin, SoftI2C
import ssd1306 
from time import sleep
import math
import framebuf

# resolution for 0.91" display
disp_width = 128
disp_height = 32

def getdisplay():
    global disp_width
    global disp_height

    # for ESP32
    i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
    # for ESP8266
    #i2c = SoftI2C(scl=Pin(5), sda=Pin(4))
    
    disp = ssd1306.SSD1306_I2C(disp_width, disp_height, i2c)
    return disp

def getframebuffer():
    global disp_width
    global disp_height

    fbuf = framebuf.FrameBuffer(bytearray(disp_width*disp_height*1), disp_width, disp_height, framebuf.MONO_VLSB)
    return fbuf 

def showtext(line1, line2, line3):
    disp = getdisplay()

    disp.text(line1, 0, 0)
    disp.text(line2, 0, 10)
    disp.text(line3, 0, 20)

    disp.show()

def showspeed(leftspeed, rightspeed):
    disp = getdisplay()

    #print("Speed:")
    #print("L: " + str(leftspeed))
    #print("R: " + str(rightspeed))
    max = 3
    min = -3
    # make sure we have sensible values
    if leftspeed > max:
        leftspeed = max
    if rightspeed > max:
        rightspeed = max
    if leftspeed < min:
        leftspeed = min
    if rightspeed < min:
        rightspeed = min

    if leftspeed > 0:
        # forward
        offset = math.floor((leftspeed / max) * 64)
        l_x1 = 64-offset
        l_x2 = 64
        l_width = 64 - l_x1
    elif leftspeed < 0:
        # reverse
        offset = math.floor((leftspeed / min) * 64)
        l_x1 = 64
        l_x2 = 64+offset
        l_width = offset
    else:
        #idle
        l_x1 = 64
        l_x2 = 65
        l_width = 1
    if rightspeed > 0:
        offset = math.floor((rightspeed / max) * 64)
        r_x1 = 64-offset
        r_x2 = 64
        r_width = 64 - r_x1
    elif rightspeed < 0:
        offset = math.floor((rightspeed / min) * 64)
        r_x1 = 64
        r_x2 = 64+offset
        r_width = offset
    else:
        #idle
        r_x1 = 64
        r_x2 = 65
        r_width = 1
    
    #print("l_x1: " + str(l_x1))
    #print("l_x2: " + str(l_x2))

    fbuf = getframebuffer()
    fbuf.fill(0)
    fbuf.fill_rect(l_x1, 24, l_width, 8, 1)
    fbuf.fill_rect(r_x1, 0, r_width, 8, 1)
    disp.blit(fbuf, 0, 0, 0)
    disp.show()

def fillscreen():
    disp = getdisplay()
    disp.fill(1)
    disp.show()

def clearscreen():
    disp = getdisplay()
    disp.fill(0)
    disp.show()