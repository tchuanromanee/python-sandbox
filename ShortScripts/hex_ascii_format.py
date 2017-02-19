# Test:  Take the hex that was going to be written to the bin file
# Convert it to ascii
# Then write to bin file
# Then compare it to the orig result
import binascii
import os
import sys
import codecs
import re

def formatHex(hexIn):
    # Format hex to print to ascii by adding \x to each char
    outStr = ''
    for i in range(0, len(hexIn), 2):
        if i+2 >= len(hexIn): # Reached the end of iDat
            #out += chr(int("0x" + iDat[i:len(iDat)], 16)) # Extract whatever is left
            #outStr += chr(int(r"\x" + hexIn[i:len(hexIn)], 16))
            outStr += r"\x" + hexIn[i:len(hexIn)] # Extract whatever is left
        else:
            #oDat += chr(int("0x" + iDat[i:i+2], 16)) + ' ' # Extract the next 4 digits from iDat
            # outStr += chr(int(r"\x" + hexIn[i:i+2], 16))
            outStr += r"\x" + hexIn[i:i+2] # Extract the next 4 digits from iDat
    return outStr


testFileName = "testRes.bin"
# testFile = os.path.join(this_current_dir, logFileName)
testFileIO = open(testFileName, 'w+', encoding="latin-1")

# hexstr = "01 52 45 4C ED D5 00 00 00 90 01 00 04 00 00 00 C0 5F 07"
hexstrBU = "0152454CEDD5000090"
hexstr = '0152454CEDD500000090010004000000C05F070020D00500FFFFFFFFFFFFFFFF'

bla="\x01\x52\x45\x4C\xED\xD5\x00\x00\x90\x01" # bla is a string
# hexstr = hexstr.replace("90", "2E") # Replace OOB char with period
# hexstr = hexstr.replace("D5", "2E") # Replace OOB Char Õ with 2E (period)
# hexstr = hexstr.replace("C2", "2E") # Replace OOB Char with 2E (period)
# hexstr = hexstr.replace("ED", "2E") # Replace OOB Char with 2E (period)
# hexstr = hexstr.replace("C0", "2E") # Replace OOB Char with 2E (period)
# hexstr = hexstr.replace("D0", "2E") # Replace OOB Char with 2E (period)
# hexstr = hexstr.replace("FF", "2E") # Replace OOB Char with 2E (period)
# hexStrNew = formatHex(hexstr)
# hexstr = re.sub(r"[8-9A-F]\d", "2E", hexstr)
# print(hexStrNew)
# hexStrNew.replace("0x", "\x")
# testFileIO.write(hexStrNew)
# testFileIO.write(bla)
testFileIO.write(str(binascii.unhexlify(hexstr),'charmap')) # Need to decode as ascii
testFileIO.close()
