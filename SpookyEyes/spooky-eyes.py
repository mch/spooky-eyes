#!/bin/python

# Based on original code for Arduino by Bill Earl of Adafruit Industries
# https://learn.adafruit.com/random-spooky-led-eyes/the-code

import colorsys
import random
import time

try:
    import Adafruit_WS2801
    import Adafruit_WS2801
    import Adafruit_GPIO

    def WS2801(np, spi):
        return Adafruit_WS2801.WS2801Pixels(np, spi = spi)

    def WS2801_rgb_to_color(r, g, b):
        return Adafruit_WS2801.RGB_to_color(r, g, b)

    def SpiDev(port, device):
        return Adafruit_GPIO.SPI.SpiDev(port, device)

except ImportError:
    print "Missing Adafruit WS2801 or GPIO libraries."
    print "Using no-op implementations."

    def WS2801(np, spi):
        return Pixels()

    def WS2801_rgb_to_color(r, g, b):
        # bogus
        return r + (g << 8) + (b << 16)

    def SpiDev(port, device):
        return None

    class Pixels:
        def clear(self):
            print "Cleared all pixels"

        def set_pixel(self, ledNumber, color):
            print "Set pixel %d to color %d" % (ledNumber, color)

        def show(self):
            print "Showing pixels"


SPI_PORT = 0
SPI_DEVICE = 0

NUM_PIXELS = 15

MAX_EYES = 3

DEAD_TIME_MIN = 50
DEAD_TIME_MAX = 500

INTERVAL_MIN = 10
INTERVAL_MAX = 300

STEP_INTERVAL = 10

class LedAction:

    def __init__(self, ledNumber, red, green, blue, intensity):
        self.ledNumber = ledNumber
        self.red = red
        self.green = green
        self.blue = blue
        self.intensity = intensity


class Blinker:

    def __init__(self):
        self.active = False

        self.deadtime = 0

        # Position of the left eye. The right eye is pos + 1
        self.pos = 0

        self.red = 0
        self.green = 0
        self.blue = 0

        self.repeats = 0

        self.increment = 0
        self.intensity = 0


    def startBlink(self, pos):
        self.active = True

        self.deadtime = random.randint(DEAD_TIME_MIN, DEAD_TIME_MAX)

        self.pos = pos

        self.red = random.randint(150, 255)
        self.green = random.randint(0, 100)
        self.blue = 0

        self.repeats += random.randint(1, 3)

        self.increment = random.randint(1,6)
        self.intensity = 0


    def step(self):

        actions = []

        if not self.active:
            if self.deadtime > 0:
                self.deadtime -= 1

            return actions

        self.intensity += self.increment

        if self.intensity >= 75:
            self.increment = -self.increment
            self.intensity += self.increment

        if self.intensity <= 0:

            # Make pixels are off
            actions.append(LedAction(self.pos, 0, 0, 0, 0))
            actions.append(LedAction(self.pos + 1, 0, 0, 0, 0))

            self.repeats -= 1
            if self.repeats <= 0:
                self.active = False
            else:
                self.increment = random.randint(1,5)

            return actions

        actions.append(LedAction(self.pos, self.red, self.green,
                                 self.blue, self.intensity))
        actions.append(LedAction(self.pos + 1, self.red, self.green,
                                 self.blue, self.intensity))
        return actions


class Eyes:

    def __init__(self, num_pixels):
        # to account for the +1 for "right" eye and the zero index
        # of the first pixel
        self.num_pixels = num_pixels - 2
        
        self.countdown = 0
        self.blinkers = [Blinker() for x in xrange(MAX_EYES)]

    def update_eyes(self):
        actions = []

        self.countdown -= 1

        for i in xrange(MAX_EYES):
            if (self.countdown <= 0) and (self.blinkers[i].active == False):
                newPos = random.randint(0, int(self.num_pixels / 2)) * 2

                for j in xrange(MAX_EYES):
                    if (self.blinkers[j].deadtime > 0) and (abs(newPos - self.blinkers[j].pos) < 4):
                        newPos = -1 # collision - do not start
                        break

                if newPos >= 0:
                    self.blinkers[i].startBlink(newPos)
                    self.countdown = random.randint(INTERVAL_MIN, INTERVAL_MAX)

            actions.extend(self.blinkers[i].step())

        return actions


def apply_actions(pixels, actions):
    for action in actions:
        if action.ledNumber >= pixels.count() or action.ledNumber < 0:
            print "WARNING: pixel number %d is invalid." % (action.ledNumber,)
            continue
        
        (hue, lightness, saturation) = colorsys.rgb_to_hls(action.red, action.green, action.blue)

        (r, g, b) = colorsys.hls_to_rgb(hue, action.intensity, saturation)

        color = WS2801_rgb_to_color(int(round(r)), int(round(g)), int(round(b)))

        pixels.set_pixel(action.ledNumber, color)

    if len(actions) > 0:
        pixels.show()



def main():

    spi = SpiDev(SPI_PORT, SPI_DEVICE)
    pixels = WS2801(NUM_PIXELS, spi)

    eyes = Eyes(NUM_PIXELS)

    pixels.clear()
    pixels.show()

    startTime = time.time()
    while True:
        time.sleep(0.01) # 10 ms
        currentTime = time.time()
        dt = (currentTime - startTime) * 1000
        if dt > STEP_INTERVAL:
            actions = eyes.update_eyes()
            apply_actions(pixels, actions)
            startTime = time.time()


if __name__ == '__main__':
    main()
