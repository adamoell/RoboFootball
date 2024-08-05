'''
rgb.py: RGB visual effects for robot
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
import machine, neopixel
from time import sleep
from time import ticks_ms

cycle_start = None
last_pattern = None
np = None

def setup_pixels():
    global np
    print("setting up pixels...")
    #pin d4=gpio2
    np = neopixel.NeoPixel(machine.Pin(2), 4)
    np[0] = (0,0,0)
    np[1] = (0,0,0)
    np[2] = (0,0,0)
    np[3] = (0,0,0)
    np.write()

def testpixels():
    setup_pixels()

    np[0] = (255,255,255)
    np[1] = (255,0,0)
    np[2] = (0,255,0)
    np[3] = (0,0,255)

    np.write()
    print("done.")
    sleep(1)

def polis():
    global cycle_start
    global last_pattern

    passive_time = 150 # was 250
    blink_active = 100 # was 100
    blink_passive = 50 # was 100

    now = ticks_ms()
    if cycle_start is None:
        cycle_start = now 
        last_pattern = 0

    elapsed = now - cycle_start
    # 250ms low blue
    if (elapsed >= 0) and (elapsed < passive_time):
        polis_1() # low blue
    
    # 100ms flash bright blue/red, low blue * 3
    p1 = passive_time
    if (elapsed >= p1) and (elapsed < (p1+blink_active)):
        polis_2() # blue / red
    if (elapsed >= (p1+blink_active)) and (elapsed < (p1+blink_active+blink_passive)):
        polis_1() # low blue
    if (elapsed >= (p1+blink_active+blink_passive)) and (elapsed < (p1+blink_active*2+blink_passive)):
        polis_2() # blue / red
    if (elapsed >= (p1+blink_active*2+blink_passive)) and (elapsed < (p1+blink_active*2+blink_passive*2)):
        polis_1() # low blue
    if (elapsed >= (p1+blink_active*2+blink_passive*2)) and (elapsed < (p1+blink_active*3+blink_passive*2)):
        polis_2() # blue / red
    if (elapsed >= (p1+blink_active*3+blink_passive*2)) and (elapsed < (p1+blink_active*3+blink_passive*3)):
        polis_1() # low blue
    
    # 100ms flash red/bright blue low blue * 3
    p1 = (p1+blink_active*3+blink_passive*3)
    if (elapsed >= p1) and (elapsed < (p1+blink_active)):
        polis_3() # blue / red
    if (elapsed >= (p1+blink_active)) and (elapsed < (p1+blink_active+blink_passive)):
        polis_1() # low blue
    if (elapsed >= (p1+blink_active+blink_passive)) and (elapsed < (p1+blink_active*2+blink_passive)):
        polis_3() # blue / red
    if (elapsed >= (p1+blink_active*2+blink_passive)) and (elapsed < (p1+blink_active*2+blink_passive*2)):
        polis_1() # low blue
    if (elapsed >= (p1+blink_active*2+blink_passive*2)) and (elapsed < (p1+blink_active*3+blink_passive*2)):
        polis_3() # blue / red
    if (elapsed >= (p1+blink_active*3+blink_passive*2)) and (elapsed < (p1+blink_active*3+blink_passive*3)):
        polis_1() # low blue

    if elapsed >= (p1+blink_active*3+blink_passive*3):
        cycle_start = now 
        last_pattern = 0
        polis_1()

def polis_1():
    global last_pattern
    # low blue
    if last_pattern != 1:
        last_pattern = 1
        np[0] = (0,0,127)
        np[1] = (0,0,127)
        np[2] = (0,0,127)
        np[3] = (0,0,127)
        np.write()

def polis_2():
    global last_pattern
    # blue/red
    if last_pattern != 2:
        last_pattern = 2
        np[0] = (0,0,255)
        np[1] = (255,0,0)
        np[2] = (255,0,0)
        np[3] = (0,0,255)
        np.write()

def polis_3():
    global last_pattern
    # red/blue
    if last_pattern != 3:
        last_pattern = 3
        np[0] = (255,0,0)
        np[1] = (0,0,255)
        np[2] = (0,0,255)
        np[3] = (255,0,0)
        np.write()
