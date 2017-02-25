import binascii

def convert_hex_to_ascii(hex_value):
    try:
        # Decode from hex to ascii, replace OOB hex with \ufffd
        ascii_val = bytes.fromhex(hex_value).decode('ascii', 'replace')
        # Replace \ufffd with "." to be true to tbl file
        ascii_val = ascii_val.replace('\ufffd', '.')
        # Replace the first 6 chars with "......" to eliminate wildcard chars
        ascii_val = "......" + ascii_val[6:len(ascii_val)]
        return ascii_val
    except UnicodeDecodeError:
        print("Ascii code out of range")
        return 0

def convert_ascii_to_hex(ascii_value):
    # Encode ascii to hex as str format, no spacecs between
    hex_val = binascii.hexlify(ascii_value).decode('ascii').upper()
    return hex_val


sample_hex = '05 00 8E 23 00 00 32 33 34 32 30 39 39 32 2E 41'
print(sample_hex + " converts to " + convert_hex_to_ascii(sample_hex))
sample_hex2 = '01 00 0E 04 77 00 32 33 34 32 30 39 38 38 2E 41'
print(sample_hex2 + " converts to " + convert_hex_to_ascii(sample_hex2))

sample_ascii = "......23420993.A"
sample_ascii_bytes_input = bytes(sample_ascii, 'ascii')
fin_hex = convert_ascii_to_hex(sample_ascii_bytes_input)
print(fin_hex)
