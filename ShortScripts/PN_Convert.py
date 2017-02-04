import binascii

def stringAsHex(partNo):
    # Converts PN (23420994) to hex (1656042)
    # Then for hex represent treated as ascii (3031363536303432)
    # Convert to hex
    hexPart = hex(int(partNo))
    hexPart = hexPart[2:len(hexPart)]
    # Append leading zero: later, check for odd/even number of chars
    if not len(hexPart) % 2 == 0:
        hexPart = '0' + hexPart
    hexPart = ''.join("{:02x}".format(ord(c)) for c in hexPart)
    return hexPart

partNo = '23420994'
hexPart = hex(int(partNo))
print("Old hexPart " + hexPart)
hexPart = hexPart[2:len(hexPart)]
# Append leading zero: later, check for odd/even number of chars
if not len(hexPart) % 2 == 0:
    hexPart = '0' + hexPart
print("Mid hexPart " + hexPart)
hexPart = ''.join("{:02x}".format(ord(c)) for c in hexPart)
print("New hexPart " + hexPart)
