'''
##################################
#   M3 ENIGMA CIPHER MACHINE     #
#      WRITTEN IN PYTHON         #
#  BY - MICHAEL AMAR, 308104215  #
##################################
'''

import sys
import string
import random
import cProfile


class Enigma:

    def __init__(self, settings, mapping):
        self.rotors = []

        # Settings for the machine ("Rotor #", Offset, Setting)
        #self.rotorsettings = [("I", 1, 1), ("II", 1, 1), ("III", 1, 1)]
        self.rotorsettings = settings

        self.reflectorsetting = "B"

        # Plugboard mapping = [("A", "B"), ("C", "D")] / [("A", "T"), ("C", "E"), ("R", "L")]
        #self.plugboardsetting = [("G", "I"), ("L", "M"), ("R", "K")]
        self.plugboardsetting = mapping

        self.plugboard = Plugboard(self.plugboardsetting)

        for i in range(len(self.rotorsettings)-1, -1, -1):
            self.rotors.append(Rotor(self.rotorsettings[i]))

        self.reflector = Reflector(self.reflectorsetting)

    def print_setup(self):
        print()
        print("Rotor sequence:")
        for r in reversed(self.rotors):
            print(r.setting, "\t", r.sequence)

        print()
        print("Reflector sequence:")
        print(self.reflector.setting, "\t", self.reflector.sequence, "\n")

        print("Plugboard settings:")
        print(self.plugboard.mapping, "\n")

    def reset(self):
        for r in self.rotors:
            r.reset()

    def encode(self, c):
        c = c.upper()

        if (not c.isalpha()):
            return c

        self.rotors[0].rotate()

        # Normal stepping
        for i in range(len(self.rotors) - 1):
            if(self.rotors[i].turnover):
                self.rotors[i].turnover = False
                self.rotors[i + 1].rotate()

        # Double step
        if self.rotors[1].base[0] in self.rotors[1].notch:
            self.rotors[1].rotate()



        # Passthrough the plugboard forward
        index = self.plugboard.forward(c)

        # Move through the rotors forward
        for r in self.rotors:
            index = r.forward(index)

        # Pass through the reflector
        index = self.reflector.forward(index)

        # Move back through rotors in reverse
        for r in reversed(self.rotors):
                index = r.reverse(index)

        # Pass through the plugboard reverse
        c = self.plugboard.reverse(index)

        return c


class Rotor:

    def __init__(self, settings):
        self.setting = settings[0]
        self.ringoffset = settings[1] - 1
        self.rotor_setting = settings[2] - 1
        self.base = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.ring_setting = []
        self.settings = {
                "I":    ["EKMFLGDQVZNTOWYHXUSPAIBRCJ", ["R"], ["Q"]],
                "II":   ["AJDKSIRUXBLHWTMCQGZNPYFVOE", ["F"], ["E"]],
                "III":  ["BDFHJLCPRTXVZNYEIWGAKMUSQO", ["W"], ["V"]],
                "IV":   ["ESOVPZJAYQUIRHXLNFTGKDCMWB", ["K"], ["J"]],
                "V":    ["VZBRGITYUPSDNHLXAWMJQOFECK", ["A"], ["Z"]]}
        self.turnovers = self.settings[self.setting][1]
        self.notch = self.settings[self.setting][2]
        self.sequence = None
        self.turnover = False
        self.reset()

    def reset(self):
        self.base = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if self.rotor_setting == 0:
            self.sequence = self.sequence_settings()
            self.ring_setting = self.sequence
        else:
            self.sequence = self.sequence_settings()
            for i in range(len(self.sequence)):
                self.ring_setting.append(self.base[(self.base.index(self.sequence[i]) + self.rotor_setting) % 25])
            print(self.ring_setting)
        self.ring_offset()

    def sequence_settings(self):
        return self.settings[self.setting][0]

    def ring_offset(self):
        for _ in range(self.ringoffset):
            self.rotate()

    def forward(self, index):
        return self.base.index(self.sequence[index])

    def reverse(self, index):
        return self.sequence.index(self.base[index])

    def rotate(self):
        self.base = self.base[1:] + self.base[:1]
        self.sequence = self.sequence[1:] + self.sequence[:1]
        if self.base[0] in self.turnovers:
            self.turnover = True


class Reflector:

    def __init__(self, setting):
        self.setting = setting
        self.base = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.settings = {"B":   "YRUHQSLDPXNGOKMIEBFZCWVJAT"}

        self.sequence = self.sequence_settings()

    def sequence_settings(self):
        return self.settings[self.setting]

    def forward(self, index):
        return self.sequence.index(self.base[index])


class Plugboard:

    def __init__(self, mapping):

        self.base = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.mapping = {}

        for m in self.base:
            self.mapping[m] = m

        for m in mapping:
            self.mapping[m[0]] = m[1]
            self.mapping[m[1]] = m[0]

    def forward(self, c):
        return self.base.index(self.mapping[c])

    def reverse(self, index):
        return self.mapping[self.base[index]]


def string_generator(size=6, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))


def offset_generator():
    return random.randint(1, 26)


def rotor_picker():
    rotors = ["I", "II", "III", "IV", "V"]
    return random.choice(rotors)


def plugboard_generator():
    mapping = []
    for x in range(random.randint(0,11)):
        mapping.append((random.choice(string.ascii_uppercase), random.choice(string.ascii_uppercase)))
    return mapping


#[("A", "T"), ("C", "E"), ("R", "L")]
def main():

    #for _ in range(1000):
        machine = Enigma([("I", 1, 1), ("II", 1, 1), ("III", 1, 1)], [])
        #machine = Enigma([(rotor_picker(), offset_generator(), 1), (rotor_picker(), offset_generator(), 1),
                          #(rotor_picker(), offset_generator(), 1)], plugboard_generator())
        machine.print_setup()
        ciphertext = ""

        try:
            # plaintext = sys.argv[1]
            plaintext = "MIKI"

            print("Plaintext", "\t", plaintext)
            for character in plaintext:
                ciphertext += machine.encode(character)

            print("Ciphertext", "\t", ciphertext)
            print('--------------------')

        except IndexError:
            for plaintext in sys.stdin:
                for character in plaintext:
                    sys.stdout.write(machine.encode(character))


if __name__ == '__main__':

    #main()
    cProfile.run('main()')