import board
from adafruit_ht16k33.segments import Seg14x4
import animation
import time


#This is a two dimensional list, which is a list made up of smaller lists.
#Each of the smaller lists contained in the main list represent one step in your animation
#The first digit represents the segment you want to light up. This will be between 1-15
#A 0 will mean no segment is lit up
#The second digit represents the grid that will be used to displayed on. Grid are labeled 1-4 going from left to right.


stepsTrail = [
    [9, 1],
    [3, 1],
    [2, 1],
    [7, 1],
    [10, 1],
    [11, 1],
    [12, 1],
    [13, 1],
    [14, 1],
    [15, 1],
    [9, 2],
    [10, 2],
    [11, 2],
    [12, 2],
    [13, 2],
    [14, 2],
    [15, 2],
    [9, 3],
    [10, 3],
    [11, 3],
    [12, 3],
    [13, 3],
    [14, 3],
    [15, 3],
    [9, 4],
    [10, 4],
    [11, 4],
    [12, 4],
    [13, 4],
    [14, 4],
    [15, 4],
]

#Initiate the i2c connection
i2c = board.STEMMA_I2C()
address:int = 0x70

#Setup the display
display = Seg14x4(i2c, address=(address))
display.brightness = 0.2

#Set up the animation, pass the display address, and the list
test = animation.DisplayPattern(stepsTrail, address, i2c)

#Control the speed the animation plays at
#The number represents the delay in seconds between each step
test.speed = .2

#How many segments are displayed at once
test.segmentTrail = 2

#Start the animation. Pass True if you want it to loop continiosly, or false if you want it to stop once it has completed each step
test.start(True)