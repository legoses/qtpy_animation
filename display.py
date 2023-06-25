'''
    TODO:
    1. fix write function so it uses new buffer system
    2. create function to clear buffer after it has been written to the display
'''

#import board
#import busio

HT16K33_BLINK_CMD = 0x80
HT16K33_BLINK_DISPLAYON = 0x01
HT16K33_CMD_BRIGHTNESS = 0xE0
HT16K33_OSCILATOR_ON = 0x21 # turn on display
HT16K33_DISPLAY_ON = 0x81

i2c = ""
address = -1
grids = [0x00, 0x02, 0x04, 0x06]


# Bytes will be save here before being written to the display
# After bytes are written to the display, this gets reset
buffer = [
    [
        ["0", "0", "0", "0", "0", "0", "0", "0"],
        ["0", "0", "0", "0", "0", "0", "0", "0"]
    ],
    [
        ["0", "0", "0", "0", "0", "0", "0", "0"],
        ["0", "0", "0", "0", "0", "0", "0", "0"]
    ],
    [
        ["0", "0", "0", "0", "0", "0", "0", "0"],
        ["0", "0", "0", "0", "0", "0", "0", "0"]
    ],
    [
        ["0", "0", "0", "0", "0", "0", "0", "0"],
        ["0", "0", "0", "0", "0", "0", "0", "0"]
    ]
]


#Lock the i2c bus in order to write to it
def lockBus():
    while not i2c.try_lock():
        pass


#Unlocks i2c bus
def unlockBus():
    i2c.unlock()


#Resets the buffer
def clearBuffer():
    global buffer

    for i in range(len(buffer)):
        buffer[i][0] = ["0", "0", "0", "0", "0", "0", "0", "0"]
        buffer[i][1] = ["0", "0", "0", "0", "0", "0", "0", "0"]


#Write from the buffer to the display
def show():
    global buffer

    lockBus() 
    for i in range(len(buffer)):
        #Join arrays within buffer into a single int
        #end result looks something like 0b00010000
        byte1 = int("0b" + "".join(buffer[i][0]))
        byte2 = int("0b" + "".join(buffer[i][1]))

        i2c.writeto(address, bytearray([grids[i], byte1, byte2]))

    unlockBus()
    clearBuffer()


#Write to the buffer
def write(info):
    global grid
    global buffer
    grid = info[1] - 1
    seg = info[0]

    #The user only gives a single number to choose the segment,
    #But the segment requires multiple bytes
    #This converts user input into two bytes
    if (seg > 8) & (seg < 16):
        buffer[grid][1][seg-2] = "1"
    elif (seg >= 0) & (seg <= 8):
        buffer[grid][0][seg-1] = "1"
    else:
        print("Please enter a number between 0 and 15")


#Clear the display
def clear():
    global address
    global i2c
    global grids

    lockBus()

    for i in range(len(grids)):
        i2c.writeto(address, bytearray([grids[i], 0b00000000, 0b00000000]))

    unlockBus()


#Adjust the brigtness
#The brightness can be controled by writing hex bytes to the display
#0xE0 indicates the lowest brightness level, 0xE1 will increase the brightness
#This continues up to at least 0xEa
def brightness(num):
    global address
    global i2c

    #Convert num from decimal to byte
    if num == 1:
        byte = int(0xEa)
    else:
        conv = 10 * num
        byte = int("0xE" + str(conv))

    lockBus()
    i2c.writeto(address, bytes([byte]))
    unlockBus()


#Initialize the display
def begin(i, a):
    global i2c
    global address

    i2c = i
    address = a

    lockBus()

    i2c.writeto(address, bytes([HT16K33_OSCILATOR_ON]))
    i2c.writeto(address, bytes([HT16K33_DISPLAY_ON]))

    unlockBus()

    clear()