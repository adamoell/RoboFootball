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



from machine import Pin, SoftI2C
import ssd1306 
from time import sleep
import math
import framebuf

# resolution for 0.91" display
disp_width = 128
disp_height = 32

class Display():
    def __init__(self, scl_pin, sda_pin, display_width=128, display_height=32):
        i2c = SoftI2C(scl=Pin(scl_pin), sda=Pin(sda_pin))
        self.disp = ssd1306.SSD1306_I2C(display_width, display_height, i2c)
        self.display_width = display_width
        self.display_height = display_height
        self.linecount = int(display_height/10)
    
    def clearscreen(self):        
        self.disp.fill(0)
        self.disp.show()
        
    def showtext(self, lines):
        linenum = 0
        for line in lines:
            if linenum < 3:
                self.disp.text(line, 3, 10*linenum)
            linenum = linenum + 1
        self.disp.show()
        
class MenuDisplay():
    def __init__(self, display, items, selected=0, offset=0, num_lines=3, num_cols=14):
        """Initialise the menu.

        Parameters:
        display: the display to render to
        items: the list of items in the menu
        selected: the ordinal value of the selected item
        offset: the ordinal value of the item displayed on line 1
        """
        self.display = display
        self.items = items
        self.selected = selected
        self.offset = offset
        self.num_lines = num_lines
        self.num_cols = num_cols
        self.show()
    
    def additem(self, item):
        pass
    
    def up(self):
        """Move the selected item down one, and scroll if necessary"""
        if self.selected > 0:
            self.selected = self.selected - 1
            self.scroll()
            self.show()
    
    def down(self):
        """Move the selected item down one, and scroll if necessary"""
        if self.selected < (len(self.items)-1):
            self.selected = self.selected + 1
            self.scroll()
            self.show()
            
    def scroll(self):
        if self.selected < self.offset:
            # selected item is ABOVE current window, scroll up
            self.offset = self.selected
        if self.selected >= self.offset+self.num_lines:
            # selected item is BELOW current window, scroll down
            self.offset = self.selected-(self.num_lines-1)
            
    def show(self):
        # show the lines - 24x3
        visible = []
        i = 0
        lines = 0
        selected_num = 0
        print()
        visible = self.items[self.offset:self.offset+self.num_lines]                  
        
        self.display.clearscreen()
        #self.display.showtext(visible)
        i = 0
        char_height = 4
        for line in visible:
            colour = 1
            #print("i:{} offset:{}
            if (i+self.offset) == self.selected:
                x1 = 0
                x2 = 127
                y1 = (10*i)-1
                y2 = y1+char_height+1
                self.display.disp.fill_rect(x1, y1, 128, 10, 1)
                self.display.disp.text(line, 0, 10*i, 0)
            else:
                self.display.disp.text(line, 0, 10*i, 1)
            i = i + 1
        self.display.disp.show()
    
    def get_selected(self):
        # return tuple of ordinal,string
        pass