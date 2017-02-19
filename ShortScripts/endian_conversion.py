def convert_id(old_id):
    # Given: old ID from csv file: eg 100000202, string of 9 chars + leading 0
    # Output: switched endianness, with 10 chars, in hex format
    first_place = "0x" + old_id[7:9]
    second_place = "0x" + old_id[5:7]
    third_place = "0x" + old_id[3:5]
    fourth_place = "0x" + old_id[1:3]
    fifth_place = "0x0" + old_id[0]  # Plus leading 0
    converted_id = (first_place + "," + second_place + "," + third_place + ","
                    + fourth_place + "," + fifth_place)
    format_converted = "{" + converted_id + "}"
    logFileStream.write("\n\tEndian Conversion: " + old_id + "-> " + converted_id)
    return format_converted
