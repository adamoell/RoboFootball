from motor import Motor, PWMMotor, motor_test, motor_test_quick, random_walk_update
from time import sleep
from machine import I2C, Pin
import machine
from pcf8574 import PCF8574
from pcf8574pin import PCFPin
from hcsr04 import HCSR04
from rgb import setup_pixels, polis
from servo import Servo
from comms import Comms



left = PWMMotor(14,12, False)
right = PWMMotor(13,15, True)

print("Hello")
# go fast
#machine.freq(160000000)
machine.freq(80000000)



# scan I2C bus
#scl = Pin(5, mode=machine.Pin.OUT, pull=machine.Pin.PULL_UP)
#sda = Pin(4, mode=machine.Pin.OUT, pull=machine.Pin.PULL_UP)
#i2c = I2C(scl, sda)


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

#scan_bus() # 56 / 0x38

# pcf = PCF8574(i2c, 0x38, direction="01000000", state="00000000") # direction: one char per pin; 0=output, 1=input
# trig_pin = PCFPin(pcf, 0)
# echo_pin = PCFPin(pcf, 1)



# left_sensor = HCSR04(trig_pin, echo_pin, pcf)
#testpixels()

def recv_msg(sender, msg):
    print("Message Received: {} {}".format(sender, msg))
    
setup_pixels()
com = Comms(recv_msg)
print("Mac Address: {}".format(com.get_mac()))
#motor_test_quick(left, right)
#sleep(1)

#left.stop()
#right.stop()

servo_pin = 5 # TX/GPIO1
servo_freq = 50
servo_down_angle = 180 # servo mounted to right facing forward
servo_kick_angle = 90  
servo = Servo(servo_pin, pwm_freq=servo_freq)
sg90_min_duty = 0.025 # 2.5% duty cycle for 0° (according to spec)
sg90_max_duty = 0.125 # 12.5% duty cycle for 180° (according to spec)
servo.auto_calibrate(sg90_min_duty, sg90_max_duty, 0, 180)
servo.goto(servo_down_angle)


while True:
#    random_walk_update(left, right)
    #polis()

    # kicker
    #servo.goto(servo_kick_angle)
    #sleep(0.1)
    #servo.goto(servo_down_angle)
    #sleep(2)
    com.check_messages()

# while True:
#     print("Quick Test")
#     motor_test_quick(left, right)

#     # val = pcf.read_pin(echo_pin)
#     # print("Echo: {}".format(val)) # 0 if short to gnd
#     # dist = left_sensor.get_distance()
#     # print("Distance: {}mm".format(dist) )

#     sleep(5)
    
    