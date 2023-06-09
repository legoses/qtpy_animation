import board
from adafruit_ht16k33.segments import Seg14x4
import animation
import time


#This is a two dimensional list, which is a list made up of smaller lists.
#Each of the smaller lists contained in the main list represent one step in your animation
#The first two digits represent the segments that will be lit up on the display.
#1-8 will light up a single segment on each display. See the diagram for more info. A 0 will not light up anything.
#The third digit represents the grid that will be used to displayed on. Grid are labeled 1-4 going from left to right.
stepsTrail = [
    [8, 2, 1],
    [7, 2, 1],
    [1, 2, 1],
    [2, 2, 1],
    [4, 2, 1],
    [5, 1, 1],
    [5, 1, 2], #start of next grid
    [6, 1, 2],
    [1, 1, 2],
    [2, 1, 2],
    [3, 0, 2],
    [8, 0, 2],
    [8, 0, 3], #start of next grid
    [7, 0, 3],
    [1, 0, 3],
    [2, 0, 3],
    [4, 0, 3],
    [5, 0, 3],
    [5, 0, 4], #start of next grid
    [6, 0, 4],
    [1, 0, 4],
    [2, 0, 4],
    [3, 0, 4],
    [8, 0, 4],
    [7, 0, 4], #Start reverse
    [1, 0, 4],
    [2, 0, 4],
    [4, 0, 4],
    [5, 0, 3], #start of next grid
    [4, 0, 3],
    [2, 0, 3],
    [1, 0, 3],
    [7, 0, 3],
    [8, 0, 3],
    [8, 0, 2], #start of next grid
    [3, 0, 2],
    [2, 0, 2],
    [1, 0, 2],
    [6, 0, 2],
    [3, 0, 2],
    [5, 0, 1], #start of next grid
    [4, 0, 1],
    [3, 0, 1],
]

#Initiate the i2c connection
i2c = board.STEMMA_I2C()
address:int = 0x72

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
test.start(False)