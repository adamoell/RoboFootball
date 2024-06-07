# https://github.com/psolyca/micropython-pcf8574/blob/master/pcf8574/pcf8574pin.py
"""PCF8574/A library

Micropython 1.10

This library aims to add compatibility with machine.Pin behaviour over PCF8574 class.

Damien "psolyca" Gaignon <damien.gaignon@gmail.com>
"""


class PCFPin():

    def __init__(self, pcf, pin):
        self._pcf = pcf
        self._pin = bytes([pin])
        # Initial state, useful for output toggle
        self._state = bytearray([pcf.read_pin(pin)])
        self._inverted = bytearray(pcf.inverted(pin))

    def value(self, value=None):
        if value is None:
            # Update state
            self._state[0] = self._pcf.read_pin(self._pin[0])
            return self._state[0]
        else:
            self._pcf.write_pin(self._pin[0], value)
            self._state[0] = value

    def on(self):
        self.value(self._inverted[0])

    def off(self):
        self.value(not self._inverted[0])

    def toggle(self):
        self._state[0] = not self.value()
        self._pcf.write_pin(self._pin[0], self._state[0])

    def mode(self, value=None, invert=False):
        if value is None:
            return self._pcf.direction(self._pin[0])
        else:
            if value == "IN":
                self._pcf.input_pin(self._pin[0], invert)
            else:
                self._pcf.output_pin(self._pin[0], invert)
            self._inverted[0] = invert

    def input(self):
        self.mode("IN", self._inverted[0])

    def output(self):
        self.mode("OUT", self._inverted[0])

    def inverted(self):
        if self._inverted[0] == 0:
            self._pcf.invert_pin(self._pin[0], True)
            self._inverted[0] = 1
            self._state[0] = not self.value()

    def noninverted(self):
        if self._inverted[0] == 1:
            self._pcf.invert_pin(self._pin[0], False)
            self._inverted[0] = 0
            self._state[0] = not self.value()