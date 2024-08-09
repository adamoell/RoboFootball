'''
thumbstick.py: dual-analogue thumbstick library
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
import machine
import time

JOY_BTN_DEBOUNCE = 300
JOY_X_DEBOUNCE = 300
JOY_Y_DEBOUNCE = 300

class Thumbstick:

    def __init__(self, x_pin, y_pin, btn_pin, btn_callback, x_zones=9, y_zones=9):
        self.x = machine.ADC(machine.Pin(x_pin))
        self.y = machine.ADC(machine.Pin(y_pin))
        # set ADC bit width
        self.x.width(machine.ADC.WIDTH_12BIT)
        self.y.width(machine.ADC.WIDTH_12BIT)
        # set attenuation so we don't need the resistor
        self.x.atten(machine.ADC.ATTN_11DB)
        self.y.atten(machine.ADC.ATTN_11DB)
        self.btn = machine.Pin(btn_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        # register button callback if specified
        if not btn_callback is None:
            self.btn_callback = btn_callback
            self.btn.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.handle_button)
        else:
            self.btn_callback = None
        self.last_btn = time.ticks_ms()
        self.btn_debounce = 250
        self.x_zones = x_zones
        self.y_zones = y_zones
        
    def rezone(self, x_zones, y_zones):
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
        
        
    def test(self, disp):
        """Test joystick, display outputs until button clicked."""
        disp.clearscreen()
        time.sleep(0.25)
        print(self.btn.value())
        oldlines = None
        l1 = "Joy Test |"
        l2 = "Move joy |"
        l3 = "Btn exit |"
        while self.btn.value() != 0:
            (x_val, y_val) = self.read_zone()
            if (x_val == -1) and (y_val == 1):
                lines = ["\\  ", " * ", "   "];
            elif (x_val == 0) and (y_val == 1):
                lines = [" | ", " * ", "   "];
            elif (x_val == 1) and (y_val == 1):
                lines = ["  /", " * ", "   "];
            elif (x_val == -1) and (y_val == 0):
                lines = ["   ", "-* ", "   "];
            elif (x_val == 0) and (y_val == 0):
                lines = ["   ", " * ", "   "];
            elif (x_val == 1) and (y_val == 0):
                lines = ["   ", " *-", "   "];
            elif (x_val == -1) and (y_val == -1):
                lines = ["   ", " * ", "/  "];
            elif (x_val == 0) and (y_val == -1):
                lines = ["   ", " * ", " | "];
            elif (x_val == 1) and (y_val == -1):
                lines = ["   ", " * ", "  \\"]
            else:
                lines = ["Joystick out of range."]
            if len(lines) == 3:
                lines[0] = l1 + lines[0] + "|"
                lines[1] = l2 + lines[1] + "|"
                lines[2] = l3 + lines[2] + "|"
            if oldlines != lines:
                disp.clearscreen()
                disp.showtext(lines)
                oldlines = lines
            time.sleep(0.1)
        
    def handle_button(self, pin):
        # debounce
        
        target = time.ticks_add(self.last_btn, self.btn_debounce)
        curr = time.ticks_ms()
        if target < curr:
            self.btn_callback()
            self.last_btn = time.ticks_ms()
            
    def wait_for_button(self):
        # wait for button to be off
        while self.btn.value() == 0:
            time.sleep(0.1)
        while True:
            if self.btn.value() == 0:
                return()
            
    def read_button(self):
        return(self.btn.value())
    
    def read_stick(self):
        '''
        Read the analogue value of X and Y axes on the stick
        (0-4095 on an ESP32)
        '''
        return( (self.x.read(), self.y.read()) )
        #return( (self.x.read_uv(), self.y.read_uv()) )
    
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
        return( (x_avg, y_avg) )

    
    def calibrate_stick(self, disp):
        # TODO safe calibration
        # TODO load calibration on init
        
        self.rezone(3, 3)
        
        disp.clearscreen()
        disp.showtext(["Hold stick", "fully left <", ""])
        (x,y) = self.read_zone()
        print(x,y)
        while (x!=-1) or (y!=0):
            time.sleep(0.1)
            (x,y) = self.read_zone()
        disp.showtext(["Hold stick", "fully left <", "..."])
        time.sleep(1)
        (self.x_min, z) = self.get_avg(100)
        print("x_min: {}".format(self.x_min))
        
        disp.clearscreen()
        disp.showtext(["Hold stick", "centred", ""])
        (x,y) = self.read_zone()
        while (x!=0) or (y!=0):
            time.sleep(0.1)
            (x,y) = self.read_zone()
        disp.showtext(["Hold stick", "centred", "..."])
        time.sleep(1)
        (self.x_mid, self.y_mid) = self.get_avg(100)
        print("x_mid: {} y_mid: {}".format(self.x_mid, self.y_mid))
        
        disp.clearscreen()
        disp.showtext(["Hold stick", "fully right >", ""])
        (x,y) = self.read_zone()
        while (x!=1) or (y!=0):
            time.sleep(0.1)
            (x,y) = self.read_zone()
        disp.showtext(["Hold stick", "fully right >", "..."])
        time.sleep(1)
        (self.x_max, z) = self.get_avg(100)
        print("x_max: {}".format(self.x_max))

        
        disp.clearscreen()
        disp.showtext(["Hold stick", "fully fwd", ""])
        (x,y) = self.read_zone()
        while (x!=0) or (y!=1):
            time.sleep(0.1)
            (x,y) = self.read_zone()
        disp.showtext(["Hold stick", "fully fwd", "..."])
        time.sleep(1)
        (z, self.y_min) = self.get_avg(100)
        print("y_min: {}".format(self.y_min))
        
        disp.clearscreen()
        disp.showtext(["Hold stick", "fully back", ""])
        (x,y) = self.read_zone()
        while (x!=0) or (y!=-1):
            time.sleep(0.1)
            (x,y) = self.read_zone()
        disp.showtext(["Hold stick", "fully back", "..."])
        time.sleep(1)
        (z, self.y_max) = self.get_avg(100)
        print("y_max: {}".format(self.y_max))

    def select(self, menu_display):
        last_btn = time.ticks_ms()
        last_x = time.ticks_ms()
        last_y = time.ticks_ms()
        
        menu_display.show()
        while True:
            (x_val, y_val) = self.read_zone()
            if (y_val != 0) and (time.ticks_diff(time.ticks_ms(), last_y) > JOY_Y_DEBOUNCE):
                if y_val == 1:
                    menu_display.up()
                if y_val == -1:
                    menu_display.down()
                last_y = time.ticks_ms()
                
            btn = self.read_button()
            if (btn == 0):
                if time.ticks_diff(time.ticks_ms(), last_btn) > JOY_BTN_DEBOUNCE:
                    return( (menu_display.selected, menu_display.items[menu_display.selected]) )
                last_btn = time.ticks_ms()
