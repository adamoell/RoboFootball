'''
main.py: servo test program
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
servo_pin = 2 # D4/GPIO2

from servo import Servo
import time

servo_freq = 50

servo = Servo(servo_pin, pwm_freq=servo_freq)
sg90_min_duty = 0.025 # 2.5% duty cycle for 0° (according to spec)
sg90_max_duty = 0.125 # 12.5% duty cycle for 180° (according to spec)
servo.auto_calibrate(sg90_min_duty, sg90_max_duty, 0, 180)
    
while True:
    #angles = [0, 45, 90, 135, 180, 135, 90, 45]
    angles = [0, 180]
    for angle in angles:
        servo.goto(angle)
        time.sleep(0.6)
    time.sleep(0.6)

# #calibration
# while True:
#     for i in range(22,150):
#         print(i)
#         servo.goto_duty(i)
#         time.sleep(0.5)

