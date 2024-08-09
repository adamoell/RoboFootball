'''
games.py: minigames for robofootball controller
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
from framebuf import FrameBuffer, MONO_VLSB
from display import MenuDisplay
import time
import random

def getfb_upleft():
    buffer = bytearray(32*32*1)
    fb = FrameBuffer(buffer, 32, 32, MONO_VLSB)
    
    size = 22
    fb.fill(0)
    for y in range(0,size,1):
        for x in range(0,size-y):
            fb.pixel(x, y, 1)
    return fb

def getfb_upright():
    buffer = bytearray(32*32*1)
    fb = FrameBuffer(buffer, 32, 32, MONO_VLSB)
    
    size = 22
    fb.fill(0)
    for y in range(0,size,1):
        for x in range(32-size+y,32):
            fb.pixel(x, y, 1)
    return fb

def getfb_downleft():
    buffer = bytearray(32*32*1)
    fb = FrameBuffer(buffer, 32, 32, MONO_VLSB)
    
    size = 22
    fb.fill(0)
    for y in range(0,size,1):
        for x in range(0,size-y):
            fb.pixel(x, 31-y, 1)
    return fb

def getfb_downright():
    buffer = bytearray(32*32*1)
    fb = FrameBuffer(buffer, 32, 32, MONO_VLSB)
    
    size = 22
    fb.fill(0)
    for y in range(0,size,1):
        for x in range(32-size+y,32):
            fb.pixel(x, 31-y, 1)
    return fb

def getfb_up():
    buffer = bytearray(32*32*1)
    fb = FrameBuffer(buffer, 32, 32, MONO_VLSB)
    
    fb.fill(0)
    mid_x = 16
    for y in range(0,16):
        start_x = mid_x - y
        end_x = start_x + (y*2)+1
        for x in range(start_x,end_x):
            fb.pixel(x, y, 1)
    return fb

def getfb_down():
    buffer = bytearray(32*32*1)
    fb = FrameBuffer(buffer, 32, 32, MONO_VLSB)
    
    fb.fill(0)
    mid_x = 16
    for y in range(0,16):
        start_x = mid_x - y
        end_x = start_x + (y*2)+1
        for x in range(start_x,end_x):
            fb.pixel(x, 31-y, 1)
    return fb
    
def getfb_left():
    buffer = bytearray(32*32*1)
    fb = FrameBuffer(buffer, 32, 32, MONO_VLSB)
    
    fb.fill(0)
    mid_y = 16
    for x in range(0,16):
        start_y = mid_y - x
        end_y = start_y + (x*2)+1
        for y in range(start_y,end_y):
            fb.pixel(x, y, 1)
    return fb

def getfb_right():
    buffer = bytearray(32*32*1)
    fb = FrameBuffer(buffer, 32, 32, MONO_VLSB)
    
    fb.fill(0)
    mid_y = 16
    for x in range(0,16):
        start_y = mid_y - x
        end_y = start_y + (x*2)+1
        for y in range(start_y,end_y):
            fb.pixel(31-x, y, 1)
    return fb

def test_reaction(icon, direction, disp, joy, timeout):
    time_start = time.ticks_ms()
    disp.disp.blit(icon, 96, 0)
    disp.disp.show()
    
    while True:
        time_now = time.ticks_ms()
        # have we timed out yet?
        elapsed = time.ticks_diff(time_now, time_start)
        if (timeout > 0) and (elapsed>timeout):
            return(0) # zero means timeout
        # check joystick
        (x,y) = joy.read_zone()
        if (x != 0) or (y != 0):
            time.sleep(0.05)
            (x,y) = joy.read_zone()
            # joystick has moved
            # clear display
            disp.disp.fill_rect(96, 0, 32, 32, 0)
            disp.disp.show()
            print("Target: {},{} Actual {},{}".format(direction[0], direction[1], x,y))
            if (x == direction[0]) and (y == direction[1]):
                return elapsed
            else:
                return -1 # wrong direction
    # clear screen
    
def reaction(joy, disp):
    """Single-player reaction game"""
    # wait for button off
    while joy.read_button() == 0:
        time.sleep(0.1)
    disp.clearscreen()
    d = disp.disp
    
    d.fill_rect(96, 0, 32, 32, 0)
    
    icons = {
        0: getfb_up(),
        1: getfb_upright(),
        2: getfb_right(),
        3: getfb_downright(),
        4: getfb_down(),
        5: getfb_downleft(),
        6: getfb_left(),
        7: getfb_upleft()
    }
    joyvals = {
        0: (0,1),
        1: (1,1),
        2: (1,0),
        3: (1,-1),
        4: (0,-1),
        5: (-1,-1),
        6: (-1,0),
        7: (-1,1)
    }
    
    rounds = 5
    best = 0
    worst = 0
    total = 0
    
    for i in range(0,rounds):
        disp.clearscreen()
        disp.showtext(["Round {}".format(i+1), "Ready..."])
        rand_dir = random.randint(0,7)
        time.sleep(1)
        r_time = test_reaction(icons[rand_dir], joyvals[rand_dir], disp, joy, 0)
        if r_time == -1:
            disp.clearscreen()
            disp.showtext(["Round {}".format(i), "DISQUALIFIED", "Wrong direction"])
            joy.wait_for_button()
            return()
        else:
            total = total + r_time
            if (best == 0) or (r_time < best):
                best = r_time
            if (worst == 0) or (r_time > worst):
                worst = r_time
                
    disp.clearscreen()
    disp.showtext(["Score: {}ms".format(int(total/rounds)), "Best: {}ms".format(best), "Worst: {}ms".format(worst)])
    joy.wait_for_button()
    
def nethost_getclient(joy, disp, cfg, com):
    """Broadcasts host details and waits for a client"""
    
    # advertise for a client
    disp_mac = cfg.get("CONTROLLER_MAC", "").replace(":", "")
    
    disp.clearscreen()
    print(disp_mac)
    disp.showtext([disp_mac, "Waiting for", "client..."])

    while True:
        com.broadcast("G|H|{}".format(cfg.get("CONTROLLER_MAC", "")))
        sender,msg = com.get_messages(timeout=1000) # wait 2s before readvertising
        print("getclient: {},{}".format(sender, msg))
        if msg:
            # is it a client message?
            bits = msg.split('|')
            if len(bits) == 3 and bits[0]=="G" and bits[1] == "C":
                client_mac = bits[2]
                print("Got client {}".format(client_mac))
                
                return client_mac

def nethost_getclienttime(com, client_mac):
    """Gets the client's time for a round"""
    print("Get Client Time")
    while True:
        sender, msg = com.get_messages()
        print("getclienttime msg {},{}".format(sender, msg))
        if (msg) and (sender==client_mac):
            bits = msg.split("|")
            if len(bits)==4 and bits[1]=="R":
                client_time = int(bits[3])
                print("Client time: {}".format(client_time))
                return client_time
            
def nethost_playgame(joy, disp, cfg, com, client_mac):
    """Play the game with the specified client"""
    my_mac = cfg.get("CONTROLLER_MAC", None)
    com.add_peer(client_mac)
    rounds = 5
    # wait for button off
    while joy.read_button() == 0:
        time.sleep(0.1)
    disp.clearscreen()
    d = disp.disp
    
    d.fill_rect(96, 0, 32, 32, 0)
    
    icons = {
        0: getfb_up(),
        1: getfb_upright(),
        2: getfb_right(),
        3: getfb_downright(),
        4: getfb_down(),
        5: getfb_downleft(),
        6: getfb_left(),
        7: getfb_upleft()
    }
    joyvals = {
        0: (0,1),
        1: (1,1),
        2: (1,0),
        3: (1,-1),
        4: (0,-1),
        5: (-1,-1),
        6: (-1,0),
        7: (-1,1)
    }
    
    
    rounds = 5
    host_score = 0
    client_score = 0
    
    for i in range(0,rounds):
        rand_dir = random.randint(0,7)
        host_time = None
        client_time = None
        
        # send the round to the client
        msg = "G|S|{}|{}".format(i, rand_dir)
        print("sending round: {}".format(msg))
        com.send(client_mac, msg)
        
        
        disp.clearscreen()
        disp.showtext(["Round {}".format(i+1), "Ready..."])
        time.sleep(5)
        # get our time
        host_time = test_reaction(icons[rand_dir], joyvals[rand_dir], disp, joy, 0)
        # get client time
        client_time = nethost_getclienttime(com, client_mac)
        
        if host_time == -1:
            result_h = -1 # wrong direction
        elif host_time < client_time:
            result_h = 1 # won
        else:
            result_h = 0 # lost
            
        if client_time == -1:
            result_c = -1 # wrong direction
        elif client_time < host_time:
            result_c = 1
        else:
            result_c = 0
            
        # update totals
        host_score = host_score + result_h
        client_score = client_score + result_c
        
        # send round result to client
        msg = "G|E|{}|{}|{}|{}|{}".format(i, result_h, host_score, result_c, client_score)
        print("round result: {}".format(msg))
        com.send(client_mac, msg)
        
        # display result
        if result_h > result_c:
            capt = "YOU WIN!"
        elif result_h < result_c:
            capt = "You lose."
        else:
            capt = "Draw!"
        disp.clearscreen()
        disp.showtext(["{}: {}".format(i+1, capt), "Host:   {}|{}".format(result_h, host_score), "Client: {}|{}".format(result_c, client_score)])
        # sleep 5s
        
        time.sleep(5)
        
    
    # send game result
    msg = "G|G|{}|{}".format(host_score, client_score)
    print("round result: {}".format(msg))
    com.send(client_mac, msg)
    
    # show game result
    if host_score > client_score:
        capt = "Fin: YOU WIN!"
    elif host_score < client_score:
        capt = "Fin: You lose."
    else:
        capt = "Fin: Draw!"
    disp.clearscreen()
    disp.showtext([capt, "Host:  {}".format(host_score), "Client:{}".format(client_score)])
    joy.wait_for_button()
    return
        
    
def nethost(joy, disp, cfg, com):
    """Two-player reaction game: host"""
    global game_msg
    
    my_mac = cfg.get("CONTROLLER_MAC", None)
    # wait for button off
    while joy.read_button() == 0:
        time.sleep(0.1)
    disp.clearscreen()
    d = disp.disp
    
    client_mac = None
    
    while client_mac == None:
        client = nethost_getclient(joy, disp, cfg, com)
        disp_client = client.replace(":", "")
    
        disp.clearscreen()
        disp.showtext([disp_client, "> to play", "< to reject"])
        result = 0
        while result == 0:
            (x, y) = joy.read_zone()
            if x == 1: # swiped right
                print("accepted {}".format(client))
                client_mac = client
                result = 1
            elif x == -1: # swiped left - rejected
                print("rejected {}".format(client))
                com.add_peer(client)
                msg = "G|X|{}".format(cfg.get("CONTROLLER_MAC", None))
                com.send(client, msg)
                result = 1
    
    nethost_playgame(joy, disp, cfg, com, client_mac)
    return
    
def netclient_obeyhost(joy, disp, cfg, com, host_mac):
    my_mac = cfg.get("CONTROLLER_MAC", None)
    
    print("netclient_obeyhost {}".format(host_mac))
    disp.clearscreen()
    d = disp.disp
    
    d.fill_rect(96, 0, 32, 32, 0)
    
    icons = {
        0: getfb_up(),
        1: getfb_upright(),
        2: getfb_right(),
        3: getfb_downright(),
        4: getfb_down(),
        5: getfb_downleft(),
        6: getfb_left(),
        7: getfb_upleft()
    }
    joyvals = {
        0: (0,1),
        1: (1,1),
        2: (1,0),
        3: (1,-1),
        4: (0,-1),
        5: (-1,-1),
        6: (-1,0),
        7: (-1,1)
    }
    
    while True:
        (sender, msg) = com.get_messages()
        print("obeyhost msg {},{}".format(sender, msg))
        if (msg) and (sender==host_mac):
            bits = msg.split("|")
            if bits[0] == "G" and bits[1] == "X": # rejected by host
                disp.clearscreen()
                disp.showtext(["Rejected by", "host", "Btn to continue"])
                joy.wait_for_button()
                return
            elif bits[0] == "G" and bits[1] == "S" and len(bits) == 4: # start round
                print("start round")
                disp.clearscreen()
                round_num = int(bits[2])
                host_dir = int(bits[3])
                disp.showtext(["Round {}".format(round_num+1), "Ready..."])
                time.sleep(5)
                client_time = test_reaction(icons[host_dir], joyvals[host_dir], disp, joy, 0)
                print("Client time: {}".format(client_time))
                msg = "G|R|{}|{}".format(round_num, client_time)
                print("Sending result: {}".format(msg))
                com.send(host_mac, msg)
            elif bits[0] == "G" and bits[1] == "E" and len(bits) == 7: # end round result
                # show round result
                print("round result received from host")
                round_num = int(bits[2])
                result_h = int(bits[3])
                host_score = int(bits[4])
                result_c = int(bits[5])
                client_score = int(bits[6])
                if result_h < result_c:
                    capt = "YOU WIN!"
                elif result_h > result_c:
                    capt = "You lose."
                else:
                    capt = "Draw!"
                                
                # display result
                print("Showing Results: r:{} h:{}|{} c:{}|{} capt:{}".format(round_num+1, result_h, host_score, result_c, client_score, capt))
                disp.clearscreen()
                disp.showtext(["{}: {}".format(round_num+1, capt), "Host:   {}|{}".format(result_h, host_score), "Client: {}|{}".format(result_c, client_score)])
                # sleep 4s
                time.sleep(4)
            
            
            elif bits[0] == "G" and bits[1] == "G" and len(bits) == 4: # end of game
                host_score = int(bits[2])
                client_score = int(bits[3])
                # show game result
                if host_score < client_score:
                    capt = "Fin: YOU WIN!"
                elif host_score > client_score:
                    capt = "Fin: You lose."
                else:
                    capt = "Fin: Draw!"
                disp.clearscreen()
                disp.showtext([capt, "Host:  {}".format(host_score), "Client:{}".format(client_score)])
                joy.wait_for_button()
                return
    
    # rejected, start round, result
    
def netclient(joy, disp, cfg, com):
    """Two-player reaction game: client"""
    
    disp.clearscreen()
    disp.showtext(["Net: client", "Searching for", "hosts..."])
    
    search_time = 5000 # search for 5 seconds
    hosts = [] # set of found hosts
    start_time = time.ticks_ms()
    while(time.ticks_diff(time.ticks_ms(), start_time) < search_time):
        sender,msg = com.get_messages(timeout=50) # scan for hosts
        if msg:
            # is it a host message?
            bits = msg.split('|')
            if len(bits) == 3 and bits[0]=="G" and bits[1] == "H":
                host_mac = bits[2]
                if not host_mac in hosts:
                    hosts.append(host_mac)
                
    # time's up
    if len(hosts) == 0:
        disp.clearscreen()
        disp.showtext(["Net: client", "No hosts found.", "Btn to exit"])
        joy.wait_for_button()
        return
    else:
        # choose from hosts
        hosts.append("Exit")
        host_menu = MenuDisplay(disp, hosts, selected=0, offset=0, num_lines=3, num_cols=16)
        (selected_id, selected_name) = joy.select(host_menu)
        print("sel: {},{}".format(selected_id, selected_name))
        if selected_name == "Exit":
            return
        else:
            # send the host the connection message
            host_mac = selected_name
            print("connecting to {}".format(host_mac))
            com.add_peer(host_mac)
            com.send(host_mac, "G|C|{}".format(cfg.get("CONTROLLER_MAC", "")))
            netclient_obeyhost(joy, disp, cfg, com, host_mac)
            return
        