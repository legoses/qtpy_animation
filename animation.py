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
        self.__clearGrids = []


    #Make sure there are no basic errors the the list the user passes
    def __checkArr(self):
        for i in range(len(self.__dispArr)):
            if len(self.__dispArr[i]) != 2:
                raise ValueError(f'Line {i+1} is missing a value')
            else:
                if (self.__dispArr[i][0] > 15) or (self.__dispArr[i][0] < 0):
                    raise ValueError(f"Segment value in row {i+1} is incorrect. Must be between 0 and 15.")
                if (self.__dispArr[i][1] > 4) or (self.__dispArr[i][1] < 0):
                    raise ValueError(f'Grid number in row {i+1} is in correct. Must be between 0 and 4')


    def __displaySeg(self, curPos, loops, byteArr):
        for i in range(loops):
            if curPos - i >= 0:
                if self.__dispArr[curPos-i][0] > 8:
                    num = self.__dispArr[curPos-i][0] - 8
                    byteArr[1][num] = "1"
                elif self.__dispArr[curPos-i][0] > 0:
                    print(self.__dispArr[curPos-i][0])
                    byteArr[0][self.__dispArr[curPos-i][0]-1] = "1"
            
        #byteArrStr = "".join(byteArr)
        #byteStr = "0b" + byteArrStr
        #return int(byteStr)


    def __listToByte(self, theList) -> int:
        listStr = "".join(theList)
        listStrByte = "0b" + listStr
        listByte = int(listStrByte)

        return listByte


    def __clearPrevGrid(self) -> void:
        #prevGridIndex = self.__gridAddr[prevGrid-1]
        print(self.__clearGrids)

        for i in self.__clearGrids:
            self.__i2c.writeto(self.__address, bytearray((self.__gridAddr[i-1], 0b00000000, 0b00000000)))

        self.__clearGrids.clear()


    @property
    def speed(self):
        return self.__speed


    @speed.setter
    def speed(self, value):
        if value <= 0:
            raise ValueError("Speed must be greater than 0")
        else:
            self.__speed = value


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
                gridNum = self.__gridAddr[self.__dispArr[i][1] - 1]
                allBytes = [
                    ["0", "0", "0", "0", "0", "0", "0", "0"],
                    ["0", "0", "0", "0", "0", "0", "0", "0"]
                ]

                #Get the byte to switch on segment
                if (gridNum == prevGrid) or (i == 0):
                    loops = 0

                    if i >= self.__trail:
                        loops = self.__trail
                    else:
                        loops = i + 1


                    self.__displaySeg(i, loops, allBytes)

                    byte1 = self.__listToByte(allBytes[0])
                    byte2 = self.__listToByte(allBytes[1])

                    #Get the bytes to be displayed
                    #if self.__dispArr[i][0] > 8:
                        #Convert given number to be used in the second display
                        #Normally the first int of the second byte doesn't do anything, so to avoid 9 being a dead number
                        #I only subtract 7, so the transition between first and second byte is smooth without any dead inbetween
                        #seg = self.__dispArr[i][0] - 7
                        #byte2 = self.__displaySeg(i, seg, loops)
                    #else:
                        #byte1 = self.__displaySeg(i, self.__dispArr[i][0], loops)

                    byteArray = bytearray((gridNum, byte1, byte2))
                    self.__writeBuffer.insert(0, byteArray)

                    if clearGrid == 1:
                        #clrOldGrid = self.__getGridNum(self.__dispArr[i][1]-1)
                        #byteArray = bytearray((prevGrid, 0b00000000, 0b00000000))
                        #self.__writeBuffer.insert(0, byteArray)
                        self.__clearPrevGrid()
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
                    gridNum = self.__getGridNum(self.__dispArr[i][1])
                    prevGrid = self.__getGridNum(self.__dispArr[i-self.__trail][1])

                    for j in range(self.__trail):
                        #Byte numbers
                        currentPosition = self.__dispArr[curRange+j][0]

                        curGridNum = self.__getGridNum(self.__dispArr[curRange+j][1])

                        #Pass the list and the index to be affected.
                        #The first digit in the second byte does not control anything.
                        #e.g. 0 will not light up a segment
                        if curGridNum == gridNum:
                            if currentPosition > 8:
                                num = currentPosition - 7
                                self.__insertInList(allBytes[1], num)
                            else:
                                self.__insertInList(allBytes[0], currentPosition)
                        else:
                            self.__clearGrids.append(self.__dispArr[curRange+j][1])

                            if currentPosition > 8:
                                num = currentPosition - 7
                                self.__insertInList(allBytes[3], num)
                            else:
                                self.__insertInList(allBytes[2], currentPosition)
                            
                        #Convert from a list to a byte
                        newGridByte1 = self.__listToByte(allBytes[0])
                        newGridByte2 = self.__listToByte(allBytes[1])
                        oldGridByte1 = self.__listToByte(allBytes[2])
                        oldGridByte2 = self.__listToByte(allBytes[3])

                        #Create bytearrays
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