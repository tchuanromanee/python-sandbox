import tkinter as tk
import tkinter.messagebox as msb
import tkinter.filedialog as fdg
import glob
import os
from os.path import basename
import sys
import binascii
import datetime
import struct
import zipfile
import subprocess
#------------------------------------------------------------------------------------------------------------------------
global STARTING_DIR
STARTING_DIR = os.path.dirname(os.path.realpath(__file__))
now = datetime.datetime.now()
start_date = now.strftime("_%y-%m-%d-%H-%M")
logFileName = "log" + start_date + ".txt"
logFile = os.path.join(STARTING_DIR, logFileName)
global logFileIO
logFileIO = open(logFile, 'w+')
#------------------------------------------------------------------------------------------------------------------------
def get_module_number():
    # example file name: PRJ_VarCal_LN00100_BSS12_IPBCSWNonXCP
    module_num_str = input_hex_file_name.split("_")[2] # eg. LN00102
    module_num_str = module_num[4:] #strip("LN00") # CHANGE b/c not always LN00
    module_num_str = module_num_str[4] # DC
    return module_num_str

def getHexFile():
    global input_hex_file
    global input_hex_file_name
    global IO_DIR_HEX
    file_read = False
    sTmp = 'Please select your Intel-HEX File:'
    while not file_read:
        full_path_hex_file = fdg.askopenfilename(filetypes=(("Hex File", "*.hex"), ("All Files", "*.*")), multiple=False, parent=root, title=sTmp)
        if full_path_hex_file=='':
            msb.showinfo(MODULE_NAME + " HEX File Selection:", "No selection made: tool abort.\nTo try again, please re-run the tool.")
            sys.exit(0)
        # Check Extension
        ext = os.path.splitext(full_path_hex_file)[1]
        if ext.lower() != '.hex':
            msb.showerror("File extension check:", "Intel-HEX file must have '.hex' extension.\nPlease try again.")
        # Confirm Selection
        else:
            res = msb.askquestion("Confirm hex file selection?", os.path.basename(full_path_hex_file), icon='question')
            if res != 'yes':
                msb.showinfo("Intel HEX file selection cancelled.\nPlease re-select.")
            else:
                input_hex_file = full_path_hex_file
                full_path_hex_file = os.path.basename(input_hex_file)
                input_hex_file_name = os.path.splitext(full_path_hex_file)[0]
                IO_DIR_HEX = os.path.split(input_hex_file)[0] # Directory of the file
                file_read = True
                input_hex_file = os.path.join(os.path.abspath(IO_DIR_HEX), input_hex_file_name + '.hex')
    return input_hex_file_name
#------------------------------------------------------------------------------------------------------------------------
def convert_hex_to_ascii(hex_value):
    try:
        # Decode from hex to ascii, replace OOB hex with \ufffd
        ascii_val = bytes.fromhex(hex_value).decode('ascii', 'replace')
        # Replace \ufffd with "." to be true to tbl file
        ascii_val = ascii_val.replace('\ufffd', '.')
        ## Replace the first 6 chars with "......" to eliminate wildcard chars
        #ascii_val = "......" + ascii_val[6:len(ascii_val)]
        return ascii_val
    except UnicodeDecodeError:
        print("Ascii code out of range")
        return 0
#------------------------------------------------------------------------------------------------------------------------
def dataWork():
    out_bin_file = os.path.join(os.path.abspath(IO_DIR_HEX), input_hex_file_name + '.bin')
    global flOBin
    flOBin = open(out_bin_file, 'wb') # Write stream for Userinput PN.DLS file #EDITED to open in binary mode
    #--------------------------------------------------------------------------------------------------------------------
    buffer_hex_file = os.path.join(os.path.abspath(STARTING_DIR), input_hex_file_name + '_temp_buf.hex')
    global hex_buffer_out
    hex_buffer_out = open(buffer_hex_file, 'w') # write stream for temp buffer hex file
    runParseCalHex()
    module_number = get_module_number()
    write_headers(out_bin_file, module_number)  # Output of HexAppend is in \Gen\final_with_header.bin
    os.chdir(STARTING_DIR) # Change current dir to help hexappend.exe
    if os.path.exists(out_bin_file):  # Delete old pn.bin file to avoid clashes
       os.remove(out_bin_file)
    os.rename(os.path.abspath(os.path.join(STARTING_DIR, 'Gen\\final_with_header.bin')), os.path.abspath(out_bin_file)) # Clean up this line

    os.chdir(IO_DIR_HEX) # Change directory back
    #------------------------------------------------------------------------------------------------------------------------
    # zipDPSContainer()
    logFileIO.close()
    root.destroy()
    sys.exit(0)
#------------------------------------------------------------------------------------------------------------------------
def write_headers(input_bin_file, module_number):
    #  Given a bin file, call HexAppend.exe to write the headers
    # Find relative path (for hexappend to work)
    relative_path = os.path.relpath(os.path.abspath(STARTING_DIR), os.path.abspath(IO_DIR_HEX))
    input_bin_file = relative_path + "\\" + input_hex_file_name + '.bin' # Works for now but should be changed
    hex_append_path = os.path.join(STARTING_DIR, 'HexAppend.exe')
    os.chdir(STARTING_DIR)
    envelope_1_ini_file = 'rb\\as\project\Cal\Configuration_envelope1_Cal' + str(module_number) + '.ini'
    envelope_2_ini_file = 'rb\\as\project\Cal\Configuration_envelope2_Cal' + str(module_number) + '.ini'
    # Append envelope 1
    args = [hex_append_path, '-cini:' + envelope_1_ini_file, '-ibin:' + input_bin_file, '-name:intermediate.bin']
    subprocess.call(args)
    # Append envelope 2
    args = [hex_append_path, '-cini:' + envelope_2_ini_file, '-ibin:Gen\intermediate.bin', '-name:final_with_header.bin']
    subprocess.call(args)
    # Output of HexAppend is in \Gen\header.bin
    os.chdir(IO_DIR_HEX) # Change directory back

#------------------------------------------------------------------------------------------------------------------------
def runParseCalHex():
    global n
    n=4
    global nB
    nB=8
    global nPn
    nPn=132
    with open(input_hex_file) as hex_in_stream:
        ln=''
        byte = "a" # initial placeholder
        while byte != '':
            byte = hex_in_stream.read(1) # Read byte one by one from hex file
            if byte == ':':
                logFileIO.write("hex line--->" + ln)
                hexLineOut(ln)
                ln=''
            else:
                ln += byte
        hexLineOut(ln)
    hex_in_stream.close()
    flOBin.close()
#------------------------------------------------------------------------------------------------------------------------
#   Parse Data Out of Intel Hex lines
def hexLineOut(ln):
    if len(ln) == 0:
        return
    addr = int(ln[2:6], 16) # Address, from hex to int
    recType = int(ln[6:8], 16) # recType, from hex to int

    if recType==4: # Extended Linear Address
        # DC: Do we need to write the 04 rectype line to the bin file? Assumption: yes
        iDat = ln[2:len(ln) - 3] # trim line (no checksum)
    elif recType==0: # Data type
        iDat = ln[8:len(ln) - 3] # Trim line (no checksum)
        logFileIO.write("trimmed data (iDat) is " + iDat + "\n") # Taking out # bytes, address, rectype, and checksum
        if not iDat=='':
            hex_buffer_out.write(iDat) # write iDat string to temp buffer hex file
            write2Bin(iDat) # Write iDat as formatted to bin file (displayed as ascii currenty...)


def write2Bin(iDat):
    iDat = iDat.strip() # EDITED: Try stripping to get rid of erroneous carraige returns
    flOBin.write(binascii.unhexlify(iDat))  # EDITED

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
#------------------------------------------------------------------------------------------------------------------------
def zip_folder(input_folder):
    with zipfile.ZipFile(input_folder, 'w', zipfile.ZIP_DEFLATED) as zipf:  #or iNmNewDps
        for dirpath, dirnames, files in os.walk(IO_DIR_HEX):
            for file in files:
                logFileIO.write("\narchiving file %s" % (file) ) # Double checking in console: remove later
                zipf.write(os.path.join(os.path.abspath(dirpath), file),  os.path.relpath(file))
    zipf.close()
#------------------------------------------------------------------------------------------------------------------------
def exitroutine():
    root.destroy()
    sys.exit(0)
#------------------------------------------------------------------------------------------------------------------------
root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", exitroutine)
root.withdraw()
getHexFile()
dataWork()
# root.update()
# root.deiconify()
#------------------------------------------------------------------------------------------------------------------------
# root.mainloop()
