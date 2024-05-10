'''
main.py: main robot program
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

from motor import Motor, PWMMotor, motor_test, motor_test_quick, random_walk_update
from time import sleep
from machine import I2C, Pin
import machine
from pcf8574 import PCF8574
from pcf8574pin import PCFPin
from hcsr04 import HCSR04
from rgb import setup_pixels, polis

left = PWMMotor(14,12, False)
right = PWMMotor(13,15, False)

# go fast
#machine.freq(160000000)
#machine.freq(80000000)



# scan I2C bus
scl = Pin(5, mode=machine.Pin.OUT, pull=machine.Pin.PULL_UP)
sda = Pin(4, mode=machine.Pin.OUT, pull=machine.Pin.PULL_UP)
i2c = I2C(scl, sda)


def scan_bus():
    print("Scanning I2C Bus")
    global i2c
    devices = i2c.scan()
    if len(devices) > 0:
        print('{} I2C devices found'.format(len(devices)))

        for device in devices:  
            print("Decimal address: ",device," | Hexa address: ",hex(device))
    else:
        print("No I2C devices found.")

scan_bus() # 56 / 0x38

pcf = PCF8574(i2c, 0x38, direction="01000000", state="00000000") # direction: one char per pin; 0=output, 1=input
trig_pin = PCFPin(pcf, 0)
echo_pin = PCFPin(pcf, 1)



#left_sensor = HCSR04(trig_pin, echo_pin, pcf)
#testpixels()
setup_pixels()
motor_test_quick(left, right)
sleep(1)

while True:
    random_walk_update(left, right)
    polis()
    time.sleep(0.1)

# while True:
#     print("Quick Test")
#     motor_test_quick(left, right)

#     # val = pcf.read_pin(echo_pin)
#     # print("Echo: {}".format(val)) # 0 if short to gnd
#     # dist = left_sensor.get_distance()
#     # print("Distance: {}mm".format(dist) )

#     sleep(5)
    
    
