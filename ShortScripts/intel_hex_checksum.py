# from http://stackoverflow.com/questions/7822956/how-to-convert-negative-integer-value-to-hex-in-python
def tohex(val, nbits):
  return hex((val + (1 << nbits)) % (1 << nbits))

def calculate_checksum(inLn): # inLn contains just the line w/o checksum
    # Calculates CheckSum8 2s Complement
    checksum = 0
    for i in range(0, len(inLn), 2):
        checksum += int(inLn[i:i+2], 16)
    # 2's complement of checksum: now in decimal so invert sign
    checksum = -checksum
    # Convert to hex: use this method to preserve signedness
    checksum = tohex(checksum, 64)
    # Take the LSB
    checksum = checksum[len(checksum)-2:]
    return checksum.upper()

print(calculate_checksum('2037E0004000400040004000400040004000400040004000400040004000400040004000'))
