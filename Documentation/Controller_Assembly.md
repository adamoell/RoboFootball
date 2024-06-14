# TODO:

- pics (labelled) of bare chassis)
- pics (labelled) of completed
- wire up batts/boards
- extra displays
- extra thumbsticks 
- switches
- wiring instructions
- copyright notice

# TO TAKE

- extra displays
- extra thumbsticks 
- extra 10KΩ resistors
- switches
- batts/boards
- F/F connectors 
- insulation tape
- M3x8 ST screws
- Soldering Iron Tips

# Wiring Harness
- Black bare ends 10cm battery-charge board
- Red bare ends 10cm battery-charge board
- Black bare-F 10cm charge board-ESP32
- Red bare ends 10cm charge board-switch 
- Red bare-F 10cm switch-ESP32

# Assembly Instructions

## Display

1. Dab a small amount of hot glue on the inside of the chassis to the left and right of the display cutout. Before the glue hardens, press the display into the glue, positioned so that the screen faces out through the cutout, with pins pointing inward and on the right (nearest the battery slot).
2. Connect an F-F jump lead to the top pin (SDA, nearest the switch cutout).
3. Connect an F-F jump lead to the second-from-top pin (SCL).
4. Make up the 3.3V wiring harness. Take two wires F to bare end. Twist together the bare ends of the two wires with one end of a 10KΩ resistor. Solder the joint together and wrap with insulating tape. Solder a third wire to the other end of the 10KΩ resistor and wrap the joint with insulating tape. Connect one of the two twisted-together wires to the third-from-top pin on the display (VCC).
5. Connect an F-F jump lead to the bottom pin (GND).


## Power Supply

1. Solder 13400 battery to B+ and B- terminals of the charge board. 
2. Adjust output to 5V. NB: if no output, put on charge briefly.
3. Solder a black wire with F connector to the - terminal of the board.
4. Solder a red wire (bare ends) to the + terminal of the board. 
5. Press the battery into its slot. Use a small amount of hot glue to secure it in place.
6. Hot glue the charge board onto its plinth, ensure the USB charge board is accessible from outside. Squeeze a dab of glue onto the plint, then press the board into it and position before glue sets. A small dab of glue on the edges of the board touching the raised edges of the plinth will hold it in place. Be careful to avoid gluing the USB port or the voltage adjustment screw.

## Switch

1. Solder a red wire with F connector to either lug of the switch.
2. Thread the red wire through the switch hole on the back side of the controller body, from outside to inside. Carefully press-fit the switch into the slot, with the "on" side toward the thumbstick. NB: the thin wall is liable to split; be gentle!
3. Switch the switch off.
4. Solder the red wire from the + terminal of the charge board to the empty lug of the switch.

## ESP32

1. Hot glue the ESP32 onto the raised plinth just below the battery. Place a generous dollop of glue centrally onto the plinth, and press the ESP32 board into it. The board should be oriented with legs up ("dead bug" mode), and the USB port toward the centre to allow for programming.
2. With the switch off, connect the black wire from the charge board to a GND pin on the board. Connect the red wire from the switch to the 5V pin on the board. NB: the CMD pin next to 5the 5V is NOT a GND pin!
3. Connect the remaining one of the two twisted-together wires from the 3.3V wiring harness (refer to point 4 under 'Display') to the 3V3 pin.
4. Connect the F-F jump lead from the top pin of the display (SDA) to pin 21.
5. Connect the F-F jump lead from the second-from-top pin of the display (SCL) to pin 22.
6. Connect the F-F jump lead from the bottom pin of the display (GND) to one of the GND pins.

## Thumbstick

1. Connect 4 F-F jump leads to each of the pins, skipping the +5V pin (from top to botton: GND, +5V, VRx, VRy, SW). 
2. Position the thumbstick with the stick going through the large circular hole, from inside to outside, with the pins to the right (facing toward the ESP32). The pins should fit into the channel and the screwholes line up with screwholes on the chassis.
3. Connect the remaining F jump lead from the 3V3 harness to the empty +5V pin.
4. Fasten the thumbstick board in place with M3x8 self-tapping screws.
5. Connect the top (nearest the switch cutout) pin (GND) to a GND pin on the ESP32.
6. Connect the third-from-top pin (VRx) to the VP pin on the ESP32 (ADC1_0/GPIO36).
7. Connect the fourth-from-top pin (VRy) to the VN pin on the ESP32 (ADC1_3/GPIO39).
8. Connect the bottom pin (SW) to the 23 pin on the ESP32 (GPIO23)

Flip the switch and test!
