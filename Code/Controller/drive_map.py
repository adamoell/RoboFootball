# dictionary mapping joystick values onto speeds
SLOW = 100
FAST = 255
STOP = 0

simple_map = {
    "zones": (3,3),
    (-1,1): (SLOW,FAST),
    (0,1): (FAST,FAST),
    (1,1): (FAST,SLOW),
    
    (-1,0): (-SLOW,SLOW),
    (0,0): (STOP,STOP),
    (1,0): (SLOW,-SLOW),
    
    (-1,-1): (-SLOW,-FAST),
    (0,-1): (-FAST,-FAST),
    (1,-1): (-FAST,-SLOW)
}

PSLOW = 80
PFAST = 110

precision_map = {
    "zones": (3,3),
    (-1,1): (PSLOW,PFAST),
    (0,1): (PFAST,PFAST),
    (1,1): (PFAST,PSLOW),
    
    (-1,0): (-PSLOW,PSLOW),
    (0,0): (STOP,STOP),
    (1,0): (PSLOW,-PSLOW),
    
    (-1,-1): (-PSLOW,-PFAST),
    (0,-1): (-PFAST,-PFAST),
    (1,-1): (-PFAST,-PSLOW)
}


default_map = {
    "zones": (7,7),
    (-3,3): (80,255),
    (-2,3): (140,255),
    (-1,3): (200,255),
    (0,3): (255,255),
    (1,3): (255,200),
    (2,3): (255,140),
    (3,3): (255,80),
    
    (-3,2): (0,255),
    (-2,2): (40,220),
    (-1,2): (100,190),
    (0,2): (160,160),
    (1,2): (190,100),
    (2,2): (220,40),
    (3,2): (255,0),
    
    (-3,1): (-100,255),
    (-2,1): (-60,200),
    (-1,1): (10,140),
    (0,1): (80,80),
    (1,1): (140,10),
    (2,1): (200,-60),
    (3,1): (255,-100),
    
    (-3,0): (-255,255),
    (-2,0): (-160,160),
    (-1,0): (-80,80),
    (0,0): (0,0),
    (1,0): (80,-80),
    (2,0): (160,-160),
    (3,0): (255,-255),
    
    (-3,-1): (100,-255),
    (-2,-1): (60,-200),
    (-1,-1): (-10,-140),
    (0,-1): (-80,-80),
    (1,-1): (-140,-10),
    (2,-1): (-200,60),
    (3,-1): (-255,100),
    
    (-3,-2): (0,-255),
    (-2,-2): (-40,-220),
    (-1,-2): (-100,-190),
    (0,-2): (-160,-160),
    (1,-2): (-190,-100),
    (2,-2): (-220,-40),
    (3,-2): (-255,0),
    
    (-3,-3): (-80,-255),
    (-2,-3): (-140,-255),
    (-1,-3): (-200,-255),
    (0,-3): (-255,-255),
    (1,-3): (-255,-200),
    (2,-3): (-255,-140),
    (3,-3): (-255,-80),
}

twitchy_map = {
    "zones": (7,7),
    (-3,3): (160,255),
    (-2,3): (190,255),
    (-1,3): (220,255),
    (0,3): (255,255),
    (1,3): (255,220),
    (2,3): (255,190),
    (3,3): (255,160),
    
    (-3,2): (100,255),
    (-2,2): (100,160),
    (-1,2): (140,160),
    (0,2): (160,160),
    (1,2): (160,140),
    (2,2): (160,100),
    (3,2): (255,100),
    
    (-3,1): (50,255),
    (-2,1): (50,160),
    (-1,1): (50,80),
    (0,1): (80,80),
    (1,1): (80,50),
    (2,1): (160,50),
    (3,1): (255,50),
    
    (-3,0): (-255,255),
    (-2,0): (-160,160),
    (-1,0): (-80,80),
    (0,0): (0,0),
    (1,0): (80,-80),
    (2,0): (160,-160),
    (3,0): (255,-255),
    
    (-3,-1): (-50,-255),
    (-2,-1): (-50,-160),
    (-1,-1): (-50,-80),
    (0,-1): (-80,-80),
    (1,-1): (-80,-50),
    (2,-1): (-160,-50),
    (3,-1): (-255,-50),
    
    (-3,-2): (-100,-255),
    (-2,-2): (-100,-160),
    (-1,-2): (-140,-160),
    (0,-2): (-160,-160),
    (1,-2): (-160,-140),
    (2,-2): (-160,-100),
    (3,-2): (-255,-100),
    
    (-3,-3): (-160,-255),
    (-2,-3): (-190,-255),
    (-1,-3): (-220,-255),
    (0,-3): (-255,-255),
    (1,-3): (-255,-220),
    (2,-3): (-255,-190),
    (3,-3): (-255,-160),
}