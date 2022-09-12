#-*- coding: utf-8 -*-
import os
import sys
def getString(fileName,data,type):
    # type-evt/game
    #type="evt"
    # print length of file
    if data[0:4] == b'BDAT':
        print('BDAT Header Match')
    numberOfData = int.from_bytes(data[12:16], byteorder='little')
    dataOffset = int.from_bytes(data[40:44], byteorder='little')

    if type=="game":
        headerOffsetLocation=6
    elif type=="evt":
        headerOffsetLocation = 20
    headerOffset = int.from_bytes(data[32:36], byteorder='little') + headerOffsetLocation

    message=""
    print("numberOfData :", numberOfData)
    print("DataOffset : 0x%08x" % dataOffset)
    print("headerOffset : 0x%08x" %headerOffset)

    for i in range(numberOfData):
        print('String #' + str(i).zfill(4), "- ", end='')
        # dataBlockLocation = int.from_bytes(data[(i * 8) + 16:(i * 8) + 20], byteorder='little')
        # print bytes as 0x hex
        # print('Data Block Location: ', data[(i * 10) + 151:(i * 10) + 153])
        if type=="game":
            dataBlockLocation = int.from_bytes(data[(i * 10) + headerOffset:(i * 10) + headerOffset + 4],byteorder='little')
        if type=="evt":
            dataBlockLocation = int.from_bytes(data[(i * 24) + headerOffset:(i * 24) + headerOffset + 4],byteorder='little')
        dataBlockLocation = dataBlockLocation + dataOffset
        # print dataBlockLocation as format 0
        print('Data Block Location: 0x%08x ' % dataBlockLocation, end="")

        # print data from dataBlockLocation(until 0x00)

        msg=""
        nullChar = False
        seek = dataBlockLocation
        if data[seek] == 0:
            nullChar = True

        while not nullChar:
            # print data[seek] as ascii
            byteData=chr(data[seek])
            if byteData == '\n':
                byteData="|"
            msg=msg+byteData
            seek = seek + 1
            if data[seek] == 0:
                nullChar = True

        print("STR=["+msg+"]")
        message=message+msg
        if i<numberOfData-1:
            message=message+"\n"
    return message
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Wrong argument has been given")
        print("USAGE: python extract.py <fileName> <type>")
        print("EXAMPLE1 : python extract.py msg_tq012615t.bdat evt ")
        print("EXAMPLE2 : python extract.py system.bdat game ")
        print("It will extract all strings from the BDAT and save to folderName")
        exit(0)
    openfile = sys.argv[1]
    filename=openfile.split('.')[0]
    f=open(openfile,'rb')
    #print f.read()
    f.seek(0)
    data=f.read()

    #print length of file
    if data[0:4]==b'BDAT':
        print('BDAT Header Match')

    #get data from header
    numberOfData=int.from_bytes(data[8:12],byteorder='little')
    fileSize=int.from_bytes(data[12:16],byteorder='little')

    #if temp folder is not created, create it
    if not os.path.exists(filename):
        os.makedirs(filename)

    #divide by blocks
    for i in range(numberOfData):
        print('Data Block #'+str(i))
        dataBlockLocation=int.from_bytes(data[(i*4)+16:(i*4)+20],byteorder='little')
        if i==numberOfData-1:
            dataBlockEnd=fileSize
        else:
            dataBlockEnd=int.from_bytes(data[(i*4)+20:(i*4)+24],byteorder='little')
        print('Data Block Location: ' , dataBlockLocation,"~",dataBlockEnd)
        #save data block dataBlockLocation:dataBlockEnd to file
        message=getString(filename,data[dataBlockLocation:dataBlockEnd],sys.argv[2])
        f2 = open(filename+'/msg' + str(i) + '.txt', 'w',encoding='utf-8')
        f2.write(message)
        f2.close()

    print("numberOfData :",numberOfData)
    print("FileSize :",fileSize,"bytes")


    #close the file
    f.close()