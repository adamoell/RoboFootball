'''
motor.py: DRV8833-based motor drivers
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
from machine import Pin
from machine import PWM
from time import sleep
from time import ticks_ms
#import random

# https://www.ti.com/lit/ds/symlink/drv8833.pdf?ts=1658764957819&ref_url=https%253A%252F%252Fwww.google.com%252F
from urandom import *

_getrandbits32 = getrandbits

lastupdate = 0
duration = 0

def getrandbits(bits: int) -> int:
    n = bits // 32
    d = 0
    for i in range(n):
        d |= _getrandbits32(32) << (i * 32)

    r = bits % 32
    if r >= 1:
        d |= _getrandbits32(r) << (n * 32)

    return d

def randrange(start, stop=None):
    if stop is None:
        stop = start
        start = 0
    upper = stop - start
    bits = 0
    pwr2 = 1
    while upper > pwr2:
        pwr2 <<= 1
        bits += 1
    while True:
        r = getrandbits(bits)
        if r < upper:
            break
    return r + start


def randint(start, stop):
    return randrange(start, stop + 1)

class Motor:
    def __init__(self, pin1, pin2, inverted=False):
        self.inverted = inverted
        self.motora = Pin(pin1, Pin.OUT)
        self.motorb = Pin(pin2, Pin.OUT)
        self.stop()

    def stop(self):
        self.motora.value(0)
        self.motorb.value(0)

    def forward(self):
        if self.inverted:
            self.motora.value(0)
            self.motorb.value(1)
        else:
            self.motora.value(1)
            self.motorb.value(0)

    def reverse(self):
        if self.inverted:
            self.motora.value(1)
            self.motorb.value(0)
        else:
            self.motora.value(0)
            self.motorb.value(1)


class PWMMotor(Motor):
    def __init__(self, pin1, pin2, inverted):
        self.pin1 = pin1
        self.pin2 = pin2
        self.motora = Pin(self.pin1, Pin.OUT)
        self.motorb = Pin(self.pin2, Pin.OUT)
        self.pwm1 = None 
        self.pwm2 = None
        self.speed = 1024
        self.freq = 1024
        self.inverted = inverted
        self.stop()

    # TODO change thist so we set speed and direction in one, with a val from -255 to 255
    def setspeed(self, speed):
        #print("Setting speed to {}".format(speed))
        # store speed
        self.speed = speed
        # if any PWMs, change them
        if self.pwm1:
            self.pwm1.duty(self.speed)
        if self.pwm2:
            self.pwm2.duty(self.speed)

    def stop(self):
        if self.pwm1:
            self.pwm1.deinit()
            self.pwm1 = None
        if self.pwm2:
            self.pwm2.deinit()
            self.pwm2 = None
        
        self.motora.value(0)
        self.motorb.value(0)

    def forward(self):
        if self.inverted:
            self._reverse()
        else:
            self._forward()

    def reverse(self):
        if self.inverted:
            self._forward()
        else:
            self._reverse()

    def _forward(self):
        # pin 1 gets PWM, pin 2 gets low
        self.pwm1 = PWM(self.motora)
        self.pwm1.freq(self.freq)
        self.pwm1.duty(self.speed)

        if self.pwm2:
            self.pwm2.deinit()
            self.pwm2 = None
        self.motorb.value(0)

    def _reverse(self):
        # pin 2 gets PWM, pin 1 gets low
        self.pwm2 = PWM(self.motorb)
        self.pwm2.freq(self.freq)
        self.pwm2.duty(self.speed)

        if self.pwm1:
            self.pwm1.deinit()
            self.pwm1 = None
        self.motora.value(0)

