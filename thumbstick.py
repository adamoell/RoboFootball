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
    
    def get_avg_x(self, num):
        # TODO integrate
        global x
        
        total = 0
        for i in range(0,num):
            total = total + x.read()
            time.sleep(0.01)
            
        return(int(total/num))

    def get_avg_y(self, num):
        # TODO integrate
        global y
        
        total = 0
        for i in range(0,num):
            total = total + y.read()
            time.sleep(0.01)
            
        return(int(total/num))
    
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
