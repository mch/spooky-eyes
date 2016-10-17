# WS2801 Spooky Eyes for the Raspberry Pi

This in an implementation of [Adafruit's Random Spooky LED Eyes](https://learn.adafruit.com/random-spooky-led-eyes) 
for the Raspberry Pi. The original is for an Arduino, but I happen to have a
Raspberry Pi, and the SPI pins on the Pi can be used to drive a string of WS2801
LEDs. 

I got my 5v LEDs off
of
[eBay](http://www.ebay.ca/itm/12mm-IP68-Waterproof-Full-Color-Digital-Diffused-RGB-LED-Pixel-WS2801-2801-/351627715013),
but they had a 3 pin connector on the output end and were a bit hard to figure out. 
The [Adafruit ones](https://www.adafruit.com/products/738) are better quality,
and have proper 4 pin connectors on both ends. 

My implementation depends on
the [Adafruit Python WS2801](https://github.com/adafruit/Adafruit_Python_WS2801)
library. 

I tested with both software and hardware SPI, and hardware SPI is definitely the
way to go. For good fading effects, hardware SPI is a must. The software
emulation's timing is off and causes other LEDs to flicker.

For this I used an external power supply for the LEDs, just a wall wart.
Although the Pi has a 5v pin, I doubt it will provide enough power to run the
LEDs. Be sure to connect the ground of the Pi with the ground of the LED power
supply. 

The green wire of the LEDs is the clock, and must be connected
to [SCLK](http://pinout.xyz/pinout/pin23_gpio11) pin on the Pi. The white wire is
the data signal, and must be connected to
the [MOSI](http://pinout.xyz/pinout/pin19_gpio10) pin on the Pi.

Be sure to enable the [SPI module](https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/README.md). 

