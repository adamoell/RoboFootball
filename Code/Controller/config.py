'''
config.py: configuration management tools
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
import os

def debugprint(message):
    #print(message)
    pass

def exists(filename):
    try:
        os.stat(filename)
        return True
    except OSError:
        return False
    
class Keys:
    def __init__(self, filepath):
        self.data = {}
        self.filepath = filepath
        self.load(filepath)

    def load(self, filepath):
        f = None
        lines = None
        if exists(filepath):
            debugprint("Loading keys: {}".format(filepath))
            f = open(filepath)
            lines = f.readlines()
            f.close()
        
        if lines:
#             try:
                # process the config file
                for line in lines:
                    l = line.strip()
                    debugprint("processing line: {}".format(l))
                    
                    if (len(l) > 0):
                        # key|value
                        bits = l.split("|")
                        debugprint("bits:{}".format(bits))
                        if len(bits) != 2:
                            debugprint("Invalid key line: [{}]".format(line))
                            raise TypeError("Invalid key line: [{}]".format(line))
                        else:
                            key = bits[0].strip()
                            value = bits[1].strip()
                            debugprint("adding dict entry {}|{}".format(key,value))
                            self.setval(key, value)
                            debugprint("Adding key [{}:{}]".format(key, value))
                    else:
                        debugprint("Ignoring blank line")
#             except:
#                 raise OSError("Problem processing the config file")
        else:
            debugprint("No config file present.")

    def save(self):
        # open the file
        with open(self.filepath, 'w') as file:
            for key, value in self.data.items():
                line = "{}|{}\n".format(key, value)
                file.write(line)
        

    def get(self, k, default=None):
        debugprint("get {}".format(k))
        #print(self.data)
        if k in self.data:
            debugprint("found")
            ret = self.data[k]
            debugprint("returning {}".format(ret))
            return ret
        else:
            if default is not None:
                debugprint("Default value returned")
                return(default)
            else:
                debugprint("No value available")
                return None

    def setval(self, key, value):
        self.data[key] = value

    def validate(self, key):
        if key in self.data:
            debugprint("Authorised [{}:{}]".format(key, self.data[key]))
            return True
        else:
            debugprint("Rejected [{}]".format(key))
            return False
        
    def delete(self, filepath):
        os.remove(filepath)
        
    
