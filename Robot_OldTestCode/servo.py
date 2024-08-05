'''
servo.py: servo motor control library
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
from machine import Pin, PWM

class Servo:
    def __init__(self, pin, pwm_freq):
        '''
        Inititalise the servo.
        --
        pin: the GPIO pin the servo is connected to
        min_duty: the minimum duty cycle the servo moves at (corresponding to min_angle) (26)
        max_duty: the duty cycle corresponding to max_angle (118)
        min_angle: the minimum angle for the servo (0°)
        max_angle: the maximum angle for the servo (180°)
        pwm_freq: the PWM frequency for the servo (50Hz)
        '''
        self.current_duty = None
        self.calibrated = False
        self.servo_pin = pin
        self.servo = PWM(Pin(pin, mode=Pin.OUT))
        self.servo.freq(pwm_freq)

    def auto_calibrate(self, min_duty_spec, max_duty_spec, min_angle, max_angle):
        '''
        Calculate and set calibration values for the servo.
        Manual calibration may yield slightly better results for individual servos.
        --
        min_duty_spec: the duty cycle corresponding to the minimum angle in the spec (0° - 2.5%=0.025 for SG90)
        max_duty_spec: the duty cycle corresponding to the maximum angle in the spec (180° - 12.5%=0.125 for SG90)
        min_angle: the minimum angle for the servo (0°)
        max_angle: the maximum angle for the servo (180°)
        '''
        min_duty = round(min_duty_spec * 1024) # 1024 is the duty cycle range of the ESP
        max_duty = round(max_duty_spec * 1024)
        print("Autocalibration: min_duty={} max_duty={}".format(min_duty, max_duty))
        self.calibrate(min_duty, max_duty, min_angle, max_angle)
        
    def calibrate(self, min_duty, max_duty, min_angle, max_angle):
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.min_duty = min_duty
        self.max_duty = max_duty
        self.calibrated = True
        
    def degrees_to_duty(self, angle):
        '''
        Convert a given angle in degrees to the appropriate duty cycle.
        --
        angle: the angle in degrees
        '''
    
        angle_fraction = (angle-self.min_angle)/(self.max_angle-self.min_angle)
        duty_range = self.max_duty - self.min_duty
        duty = int(self.min_duty + (angle_fraction * duty_range))
        #print("angle: {} duty: {}".format(angle, duty))
        return(duty)

    def goto(self, angle):
        '''
        Move the servo to a specified angle.
        --
        angle: the angle to move the servo to.
        '''
        if self.calibrated:
            self.goto_duty(self.degrees_to_duty(angle))
        else:
            print("Uncalibrated")
        
    def goto_duty(self, duty):
        '''
        Move the servo by specifiying a duty cycle.
        --
        duty: the duty cycle to send to the servo.
        '''
        if duty != self.current_duty:
            self.current_duty = duty
            self.servo.duty(duty)

        
