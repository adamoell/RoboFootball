# thumbstick library
import machine
import time

class Thumbstick:

    def __init__(self, x_pin, y_pin, btn_pin, btn_callback, x_zones=9, y_zones=9):
        self.x = machine.ADC(machine.Pin(x_pin))
        self.y = machine.ADC(machine.Pin(y_pin))
        self.btn = machine.Pin(btn_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.btn_callback = btn_callback
        self.btn.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.handle_button)
        self.last_btn = time.ticks_ms()
        self.btn_debounce = 250
        self.x_zones = x_zones
        self.y_zones = y_zones
        
    def set_calibration(self, x_min, x_mid, x_max, y_min, y_mid, y_max):
        self.x_min = x_min
        self.x_mid = x_mid
        self.x_max = x_max
        self.y_min = y_min
        self.y_mid = y_mid
        self.y_max = y_max
        
    def save_calibration(self):
        cal = "{}|{}|{}|{}|{}|{}".format(self.x_min, self.x_mid, self.x_max, self.y_min, self.y_mid, self.y_max)
        with open("calibration.cfg", "w") as f:
            f.write(cal)
    
    def load_calibration(self):
        try:
            f = open("calibration.cfg", "r")
            cal = f.read()
            items = cal.split("|")
            if len(items) != 6:
                print("Invalid calibration.")
                return False
            else:
                self.x_min = int(items[0])
                self.x_mid = int(items[1])
                self.x_max = int(items[2])
                self.y_min = int(items[3])
                self.y_mid = int(items[4])
                self.y_max = int(items[5])
                return True
        except:
            return False
            
            
        cal = "{}|{}|{}|{}|{}|{}".format(self.x_min, self.x_mid, self.x_max, self.y_min, self.y_mid, self.y_max)
        print(cal)
        
        
    def handle_button(self, pin):
        # debounce
        
        target = time.ticks_add(self.last_btn, self.btn_debounce)
        curr = time.ticks_ms()
        if target < curr:
            self.btn_callback()
            self.last_btn = time.ticks_ms()
            
    def read_stick(self):
        '''
        Read the analogue value of X and Y axes on the stick
        (0-4095 on an ESP32)
        '''
        return( (self.x.read(), self.y.read()) )
    
    def read_zone(self):
        (x_val, y_val) = self.read_stick()
        
        # work out x zone
        x_zone_range = (self.x_max-self.x_min)/self.x_zones
        x_zero_min = (self.x_mid - x_zone_range/2)
        x_zero_max = (self.x_mid + x_zone_range/2)
        
        if (x_val > x_zero_min) and (x_val < x_zero_max):
            x_zone = 0
        elif (x_val < x_zero_min):
            # calc left zones
            num_left = int(self.x_zones/2)
            x_zone = -num_left + (int((x_val/x_zero_min) * num_left))
        else:
            # calc right zones
            num_right = int(self.x_zones/2)
            x_zone = int((x_val-x_zero_max)/(self.x_max-x_zero_max) * num_right)
            
        # work out y zone
        y_zone_range = (self.y_max-self.y_min)/self.y_zones
        y_zero_min = (self.y_mid - y_zone_range/2)
        y_zero_max = (self.y_mid + y_zone_range/2)
        
        if (y_val > y_zero_min) and (y_val < y_zero_max):
            y_zone = 0
        elif (y_val < y_zero_min):
            # calc up zones
            num_up = int(self.y_zones/2)
            y_zone = -num_up + (int((y_val/y_zero_min) * num_up))
        else:
            # calc down zones
            num_down = int(self.y_zones/2)
            y_zone = int((y_val-y_zero_max)/(self.y_max-y_zero_max) * num_down)
        
        return ( (x_zone, y_zone*-1) )
    
    def get_avg(self, num):
        '''
        Gets the average value of a given number of samples.
        Parameters:
        num: (int) the number of samples to take.
        '''
        # TODO integrate
        x_total = 0
        y_total = 0
        for i in range(0,num):
            (x_val, y_val) = self.read_stick()

            x_total = x_total + x_val
            y_total = y_total + y_val
            time.sleep(0.01)
            
        x_avg = int(x_total/num)
        y_avg = int(y_total/num)
        print(x_avg, y_avg)
        return( (x_avg, y_avg) )

    
    def calibrate_stick(self):
        # TODO safe calibration
        # TODO load calibration on init
        global x_min, x_mid, x_max
        
        input("Hold stick fully left and press Enter")
        x_min = get_avg_x(100)
        input("Center stick and press Enter")
        x_mid = get_avg_x(100)
        input("Hold stick fully right and press Enter")
        x_max = get_avg_x(100)
        
        input("Hold stick fully up and press Enter")
        y_min = get_avg_y(100)
        input("Center stick and press Enter")
        y_mid = get_avg_y(100)
        input("Hold stick fully down and press Enter")
        y_max = get_avg_y(100)
        
        print("X Calibration:")
        print("<<{}<< ||{}|| >>{}>>".format(x_min, x_mid, x_max))
        print("Y Calibration:")
        print("<<{}<< ||{}|| >>{}>>".format(y_min, y_mid, y_max))
