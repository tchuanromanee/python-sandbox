import binascii

def runCrc32():
    hexFileIO = open('hexBuffer.hex', 'r') # Open the temp buffer hex file to read
    dataIn = hexFileIO.read()
    dataToConvert = dataIn[:len(dataIn)-128]
    hexFileIO.close()
    print('dataToConvert size is: ' + str(len(dataIn)) + "\n")

    # Changes bufDat from hex to ascii, calculates crc, then formats to hex format again
    bufCrc32 = '%08X' % (binascii.crc32(binascii.a2b_hex(dataToConvert)) & 0xffffffff)
    print('orig crc32 is ' + bufCrc32 + "\n")
    hCrc32 = "".join(reversed([bufCrc32[i:i+2] for i in range(0, len(bufCrc32), 2)]))
    print('Crc is: ' + str(hCrc32))
    # ?? Write crc to buffer hex file
    return str(hCrc32)

finalCRC = runCrc32()
