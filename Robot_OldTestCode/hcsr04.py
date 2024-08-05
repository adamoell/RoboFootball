from time import sleep_us, ticks_us
import machine

class HCSR04:
    def __init__(self, trig_pin, echo_pin, pcf):
        self.pcf = pcf 
        self.trig_pin = trig_pin 
        self.echo_pin = echo_pin 
        #self.timeout_us = 500*2*30 # TODO - reduce this down to TOF for 1-2 metres
        self.timeout_us = 10000
        # NB: pins must be setup on the PCF8574
        # trigger as output
        # echo as input
        

    def __get_tof(self):
        """
        Sends a pulse and measures the time until echo is received.
        Times out after self.timeout_us microseconds
        """
        # get ready to send a pulse
        #self.pcf.write_pin(self.trig_pin, 0)
        self.trig_pin.value(0)
        sleep_us(5)
        
        # transmit 10us pulse       
        #self.pcf.write_pin(self.trig_pin, 1)
        self.trig_pin.value(1)
        sleep_us(10)
        #self.pcf.write_pin(self.trig_pin, 0)
        self.trig_pin.value(0)
        

        #scan for the echo
        start = ticks_us()
        now = ticks_us()
        elapsed = now - start
        while (elapsed<self.timeout_us):
            val = self.echo_pin.value()
            #val = self.pcf.read_pin(self.echo_pin)
            if val == 0:
                got_echo = True
                return(elapsed)

            now = ticks_us()
            elapsed = now - start
        return -1 # timed out
        



    def get_distance(self):
        tof = self.__get_tof()
        print("tof (us): {}".format(tof))

        if tof == -1:
            # timed out
            dist_mm = 99999
        else:
            # To calculate the distance we get the pulse time-of-flight and divide
            # by 2 (there and back).
            # Speed of sound is 343.2 m/s), which is 
            # 0.34320 mm/us, ie 1mm each 2.91us
            # pulse_time // 2 // 2.91 -> pulse_time // 5.82 -> pulse_time * 100 // 582 
            dist_mm = tof * 100 // 582
        return dist_mm

    # def get_distance(self):     
    #     # average 3 measurements
    #     tof = 0
    #     num_measurements = 5
    #     for i in range(0,5):
    #         measurement = self.__get_tof()
    #         if measurement >= 0:
    #             tof = tof + measurement
    #         else: 
    #             tof = tof + self.timeout_us

    #     tof = tof // 5
    #     print("tof (us): {}".format(tof))

    #     if tof == -1:
    #         # timed out
    #         dist_mm = 99999
    #     else:
    #         # To calculate the distance we get the pulse time-of-flight and divide
    #         # by 2 (there and back).
    #         # Speed of sound is 343.2 m/s), which is 
    #         # 0.34320 mm/us, ie 1mm each 2.91us
    #         # pulse_time // 2 // 2.91 -> pulse_time // 5.82 -> pulse_time * 100 // 582 
    #         dist_mm = tof * 100 // 582
    #     return dist_mm