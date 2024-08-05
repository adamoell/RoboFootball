# https://github.com/psolyca/micropython-pcf8574
# https://micropython-pcf8574.readthedocs.io/en/latest/
"""PCF8574/A library

Micropython 1.10

This library aims to control PCF8574/A device through I2C.

Damien "psolyca" Gaignon <damien.gaignon@gmail.com>

Based on https://git.cryhost.de/crycode/node-pcf8574
"""

import utime

import machine
import micropython 

micropython.alloc_emergency_exception_buf(100)

class DirectionException(Exception):
    pass


class PCF8574():

    INPUT = 1
    OUTPUT = 0
    UNDEF = 2

    def __init__(self, i2c, address, direction=None, state=None, inverted=None):
        self._i2c = i2c
        self._address = address
        # Direction of pins
        self._directions = bytearray([self.UNDEF] * 8)
        # Input pins bitmask
        self._input = bytearray(1)
        # Inverted pins bitmask
        self._inverted = bytearray(1)
        # Logical state of pins (inverted)
        self._lstate = bytearray(1)
        # Digital state of pins (non inverted)
        self._dstate = bytearray(1)
        # Flag to avoid one/multiple use of read and/or write from/to IC
        self._dstatef = False
        # Pre-allocate interrupt handler
        self._alloc_poll = self._poll
        # Interruption counter
        self.interrupt = 0
        # Array of changed pins for interruption ([pin\value] * 8)
        self.changed_pins = bytearray(16)

        if direction is not None:
            direction = list(direction)
            self._directions = bytearray(int(x) for x in direction)
            self._input[0] = int(''.join(reversed(direction)),2)
        if inverted is not None:
            self._inverted[0] = int(''.join(reversed(list(inverted))),2)
        if state is not None:
            self._lstate[0] = int(''.join(reversed(list(state))),2)
            self._dstate[0] = self._lstate[0] ^ self._inverted[0]
            self._dstate[0] = self._dstate[0] | self._input[0]
            self._i2c.writeto(self._address, self._dstate)

    def __repr__(self):
        """Bit representation of pin states"""
        return "{:08b}".format(self._lstate[0])

    def _alter_bitmask(self, bitmask, pin, value=True):
        if value:
            return bytearray([bitmask[0] | (1 << pin)])
        else:
            return bytearray([bitmask[0] & ~(1 << pin)])

    def _write_state(self):
        if not self._dstatef:
            self._dstatef = True
            # Inverted pins
            self._dstate[0] = self._lstate[0] ^ self._inverted[0]
            # Input pins to high
            self._dstate[0] = self._dstate[0] | self._input[0]
            self._i2c.writeto(self._address, self._dstate)
            self._dstatef = False

    def _read_state(self):
        if not self._dstatef:
            self._dstatef = True
            self._dstate = bytearray(self._i2c.readfrom(self._address, 1))
            # Inverted pins
            self._lstate[0] = self._dstate[0] ^ self._inverted[0]
            self._dstatef = False

    def read_pin(self, pin):
        # Update self._lstate
        self._read_state()
        return self._lstate[0] >> pin & 1

    def write_pin(self, pin, value):
        if self._directions[pin] == self.OUTPUT:
            self._lstate = self._alter_bitmask(self._lstate, pin, value)
            self._write_state()

    def input_pin(self, pin, invert=False):
        if type(pin) == list:
            for p in pin:
                self._inverted = self._alter_bitmask(self._inverted, pin, invert)
                self._input = self._alter_bitmask(self._input, pin, True)
                self._directions[pin] = self._input
        else:
            self._inverted = self._alter_bitmask(self._inverted, pin, invert)
            self._input = self._alter_bitmask(self._input, pin, True)
            self._directions[pin] = self._input
        self._lstate[0] = self._dstate[0] ^ self._inverted[0]

        self._write_state()

    def output_pin(self, pin, invert=False):
        if type(pin) == list:
            for p in pin:
                self._inverted = self._alter_bitmask(self._inverted, pin, invert)
                self._input = self._alter_bitmask(self._input, pin, False)
                self._directions[pin] = self.OUTPUT
        else:
            self._inverted = self._alter_bitmask(self._inverted, pin, invert)
            self._input = self._alter_bitmask(self._input, pin, False)
            self._directions[pin] = self.OUTPUT
        self._lstate[0] = self._dstate[0] ^ self._inverted[0]

        self._write_state()

    def invert_pin(self, pin, invert=False):
        if type(pin) == list:
            for p in pin:
                self._inverted = self._alter_bitmask(self._inverted, pin, invert)
        else:
            self._inverted = self._alter_bitmask(self._inverted, pin, invert)
        self._lstate[0] = self._dstate[0] ^ self._inverted[0]

        self._write_state()

    def _poll(self, _):
        self._dstate[0] = self._i2c.readfrom(self._address, 1)[0]

        readstate = bytearray([self._dstate[0] ^ self._inverted[0]])
        for pin in range(8):
            if self._directions[pin] == self._input:
                # Check if the pin has changed
                if (self._lstate[0] >> pin & 1) != (readstate[0] >> pin & 1):
                    # Changed the state of the pin
                    self._lstate = self._alter_bitmask(
                        self._lstate,
                        pin,
                        readstate[0] >> pin & 1)
                    self.changed_pins[pin * 2] = 1
                    self.changed_pins[pin * 2 + 1] = readstate[0] >> pin & 1
        self.interrupt +=1

    def enable_int(self, pin):
        # Initialize changed_pins default value
        for p in range(8):
            self.changed_pins[p * 2 + 1] = self._lstate[0] >> p & 1
        self._int_pin = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self._int_pin.irq(trigger = machine.Pin.IRQ_FALLING,
                        handler = self._alloc_poll
                        )

    def reset_int(self):
        state = machine.disable_irq()
        for pin in range(8):
            self.changed_pins[pin * 2 ] = 0
        self.interrupt -= 1
        machine.enable_irq(state)
    
    def disable_int(self):
        machine.disable_irq()
        self.changed_pins = bytearray(16)
        self.interrupt = 0

    def inverted(self, pin):
        return self._inverted[0] >> pin & 1

    def direction(self, pin):
        return self._directions[pin]