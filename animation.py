import time


class DisplayPattern:
    def __init__(self, dispArr, address, i2c, speed=0.1, trail = 2):
        self.__dispArr = dispArr
        self.__address = address
        self.__speed = speed
        self.__gridAddr: int = [0x00, 0x02, 0x04, 0x06]
        self.__i2c = i2c
        self.__trail = trail
        self.__writeBuffer = []


    #Make sure there are no basic errors the the list the user passes
    def __checkArr(self):
        for i in range(len(self.__dispArr)):
            if len(self.__dispArr[i]) != 3:
                raise ValueError(f'Line {i+1} is missing a value')
            else:
                if (self.__dispArr[i][0] > 8) or (self.__dispArr[i][0] < 0):
                    raise ValueError(f"Segment value in row {i+1} is incorrect. Must be between 0 and 7.")
                if (self.__dispArr[i][1] > 4) or (self.__dispArr[i][1] < 0):
                    raise ValueError(f'Grid number in row {i+1} is in correct. Must be between 0 and 4')


    #setup the bytes to be displayed
    def __displaySeg(self, curPos, loops, bit) -> int:
        byteArr = ["0", "0", "0", "0", "0", "0", "0", "0"]

        for i in range(loops):
            if curPos - i >= 0:
                byteNum = self.__dispArr[curPos-i][bit]
                if byteNum != 0:
                    byteArr[byteNum-1] = "1"
            
        byteArrStr = "".join(byteArr)
        byteStr = "0b" + byteArrStr
        return int(byteStr)


    def __listToByte(self, theList) -> int:
        listStr = "".join(theList)
        listStrByte = "0b" + listStr
        listByte = int(listStrByte)

        return listByte


    def clearPrevGrid(self, prevGrid) -> void:
        prevGridIndex = self.__gridAddr[prevGrid-1]
        self.__i2c.writeto(self.__address, bytearray((prevGridIndex, 0b00000000, 0b00000000)))


    @property
    def speed(self):
        return self.__speed


    @speed.setter
    def speed(self, value):
        if value <= 0:
            raise ValueError("Speed must be greater than 0")


    @property
    def segmentTrail(self):
        return self.__trail


    @segmentTrail.setter
    def segmentTrail(self, setTrail):
        if (setTrail > 0) and (setTrail < 8):
            self.__trail = setTrail
        else:
            raise ValueError("Trail must be greater than 0 and less than 8")


    def __writeToDisplay(self):
        for i in range(len(self.__writeBuffer)):
            self.__i2c.writeto(self.__address, self.__writeBuffer[i])

    #Created because I keep forgetting that the grid number needs to be grabbed from the gridAddr list, and not the dispArr list
    def __getGridNum(self, iVal):
        return self.__gridAddr[iVal-1]


    def __insertInList(self, theList, theByte) -> void:
        newByte = theByte - 1
        if theByte != 0:
            theList[newByte] = "1"


    def start(self, loop):
        self.__checkArr()
        
        self.__i2c.try_lock()

        #Keep track of whether or not previous grid should be cleared
        clearGrid = 0
        prevGrid = 0

        while True:
            prevByteArray = 0

            for i in range(len(self.__dispArr)):
                #Get the grid the user selected
                #User will choose a number between 1 and 4. Subtract 1 to get the array index
                gridNum = self.__gridAddr[self.__dispArr[i][2] - 1]

                #Get the byte to switch on segment
                if (gridNum == prevGrid) or (i == 0):
                    loops = 0

                    if i >= self.__trail:
                        loops = self.__trail
                    else:
                        loops = i + 1

                    #Get the bytes to be displayed
                    byte1 = self.__displaySeg(i, loops, 0)
                    byte2 = self.__displaySeg(i, loops, 1)

                    byteArray = bytearray((gridNum, byte1, byte2))
                    self.__writeBuffer.insert(0, byteArray)

                    if clearGrid == 1:
                        clrOldGrid = self.__getGridNum(self.__dispArr[i][2]-1)
                        byteArray = bytearray((prevGrid, 0b00000000, 0b00000000))
                        self.__writeBuffer.insert(0, byteArray)
                        clearGrid = 0

                    #Write from the buffer to the display
                    self.__writeToDisplay()
                    prevByteArray = byteArray

                else:
                    allBytes = [
                        ["0", "0", "0", "0", "0", "0", "0", "0"], #Current grid byte 1
                        ["0", "0", "0", "0", "0", "0", "0", "0"], #Current grid byte 2
                        ["0", "0", "0", "0", "0", "0", "0", "0"], #Previous grid byte 1
                        ["0", "0", "0", "0", "0", "0", "0", "0"], #Previous grid byte 2
                    ]

                    #Index of furthest back segment being displayed
                    curRange = i - (self.__trail - 1)

                    #Number of the previous and current grids
                    gridNum = self.__getGridNum(self.__dispArr[i][2])
                    prevGrid = self.__getGridNum(self.__dispArr[i-self.__trail][2])

                    for j in range(self.__trail):
                        #Byte numbers
                        currentPosition1 = self.__dispArr[curRange+j][0]
                        currentPosition2 = self.__dispArr[curRange+j][1]

                        curGridNum = self.__getGridNum(self.__dispArr[curRange+j][2])

                        if curGridNum == gridNum:
                            self.__insertInList(allBytes[0], currentPosition1)
                            self.__insertInList(allBytes[1], currentPosition2)
                        else:
                            self.__insertInList(allBytes[2], currentPosition1)
                            self.__insertInList(allBytes[3], currentPosition2)
                            
                        #Convert from a list to a byte
                        newGridByte1 = self.__listToByte(allBytes[0])
                        newGridByte2 = self.__listToByte(allBytes[1])
                        oldGridByte1 = self.__listToByte(allBytes[2])
                        oldGridByte2 = self.__listToByte(allBytes[3])

                        #Create byteararys
                        newGridArray = bytearray((gridNum, newGridByte1, newGridByte2))
                        prevGridArray = bytearray((prevGrid, oldGridByte1, oldGridByte2))

                        #Insert into buffer before writing to display
                        self.__writeBuffer.insert(0, newGridArray)
                        self.__writeBuffer.insert(0, prevGridArray)

                        #Display the buffer contents, then clear the display
                        self.__writeToDisplay()
                        self.__writeBuffer.clear()
                        clearGrid = 1
                        i += 1    

                self.__writeBuffer.clear()
                time.sleep(self.__speed)
                #time.sleep(.5)

            if loop == False:
                self.__i2c.unlock()
                return