import tkinter as tk
import tkinter.messagebox as msb
import tkinter.filedialog as fdg
import glob
import os
from os.path import basename
import sys
import binascii
import datetime
import subprocess
global STARTING_DIR
STARTING_DIR = os.path.dirname(os.path.realpath(__file__))
now = datetime.datetime.now()
start_date = now.strftime("_%y-%m-%d")
log_file_name = "log" + start_date + ".txt"
log_file = os.path.join(STARTING_DIR, log_file_name)
global log_stream
log_stream = open(log_file, 'w+')


def get_module_number():
    # example file name: PRJ_VarCal_LN00100_BSS12_IPBCSWNonXCP
    module_num_str = input_hex_file_name.split("_")[2]  # eg. LN00102
    module_num_str = module_num[2:]  # strip("LN") # CHANGE b/c not always LN
    # module_num_str = module_num_str[4]  # DC
    return module_num_str


def get_hex_file():
    global input_hex_file
    global input_hex_file_name
    global IO_DIR_HEX
    file_read = False
    fdg_title = 'Please select your Intel-HEX File:'
    while not file_read:
        full_path_hex_file = fdg.askopenfilename(filetypes=(("Hex File", "*.hex"), ("All Files", "*.*")),
                                                 multiple=False, parent=root, title=fdg_title)
        if full_path_hex_file == '':
            msb.showinfo("HEX File Selection:", "No selection made: tool abort.\nPlease try again.")
            sys.exit(0)
        ext = os.path.splitext(full_path_hex_file)[1]
        if ext.lower() != '.hex':  # Check Extension
            msb.showerror("File extension check:", "Intel-HEX file must have '.hex' extension.\nPlease try again.")
        else:  # Confirm Selection
            res = msb.askquestion("Confirm hex file selection?", os.path.basename(full_path_hex_file), icon='question')
            if res != 'yes':
                msb.showinfo("Intel HEX file selection cancelled.\nPlease re-select.")
            else:
                input_hex_file = full_path_hex_file
                full_path_hex_file = os.path.basename(input_hex_file)
                input_hex_file_name = os.path.splitext(full_path_hex_file)[0]
                IO_DIR_HEX = os.path.split(input_hex_file)[0]  # Directory of the file
                file_read = True
                input_hex_file = os.path.join(os.path.abspath(IO_DIR_HEX), input_hex_file_name + '.hex')


def convert_hex_to_ascii(hex_value):
    try:
        # Decode from hex to ascii, replace OOB hex with \ufffd
        ascii_val = bytes.fromhex(hex_value).decode('ascii', 'replace')
        # Replace \ufffd with "." to be true to tbl file
        ascii_val = ascii_val.replace('\ufffd', '.')
        # Replace the first 6 chars with "......" to eliminate wildcard chars
        # ascii_val = "......" + ascii_val[6:len(ascii_val)]
        return ascii_val
    except UnicodeDecodeError:
        print("Ascii code out of range")
        return 0


def data_work():
    out_bin_file = os.path.join(os.path.abspath(IO_DIR_HEX), input_hex_file_name + '.bin')
    global bin_out_stream
    bin_out_stream = open(out_bin_file, 'wb')  # Write stream for Userinput PN.DLS file #EDITED to open in binary mode
    # buffer_hex_file = os.path.join(os.path.abspath(STARTING_DIR), input_hex_file_name + '_temp_buf.hex')
    # global hex_buffer_out
    # hex_buffer_out = open(buffer_hex_file, 'w')  # write stream for temp buffer hex file
    run_parse_hex()
    bin_out_stream.close()
    module_number = 3 # get_module_number()
    write_headers(out_bin_file, module_number)  # Output of HexAppend is in \Gen\final_with_header.bin
    # os.chdir(STARTING_DIR)  # Change current dir to help hexappend.exe
    if os.path.exists(out_bin_file):  # Delete old pn.bin file to avoid clashes
        os.remove(out_bin_file)
    os.rename(os.path.abspath(os.path.join(STARTING_DIR, 'Gen\\final_with_header.bin')), os.path.abspath(out_bin_file))
    # os.chdir(IO_DIR_HEX)  # Change directory back
    # if os.path.exists(buffer_hex_file):
    #     os.remove(buffer_hex_file)
    log_stream.close()
    root.destroy()
    sys.exit(0)


def write_headers(input_bin_file, module_number):
    #  Given a bin file, call HexAppend.exe to write the headers
    # Find relative path (for hexappend to work)
    relative_path = os.path.relpath(os.path.abspath(STARTING_DIR), os.path.abspath(IO_DIR_HEX))
    input_bin_file = relative_path + "\\" + input_hex_file_name + '.bin'  # Works for now but should be changed
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
    # os.chdir(IO_DIR_HEX)  # Change directory back


def run_parse_hex():
    with open(input_hex_file) as hex_in_stream:
        ln = ''
        byte = "a"  # initial placeholder
        while byte != '':
            byte = hex_in_stream.read(1)  # Read byte one by one from hex file
            if byte == ':':
                log_stream.write("hex line--->" + ln)
                hex_line_out(ln)
                ln = ''
            else:
                ln += byte
        hex_line_out(ln)
    hex_in_stream.close()


# Parse Data Out of Intel Hex lines
def hex_line_out(ln):
    if len(ln) == 0:
        return
    rec_type = int(ln[6:8], 16)  # rec_type, from hex to int
    if rec_type == 4:  # Extended Linear Address
        # Check to see if this line is needed in the bin file?
        # line_out = ln[2:len(ln) - 3]  # trim line (no checksum)
        return
    elif rec_type == 0:  # Data type
        line_out = ln[8:len(ln) - 3]  # Trim line (no checksum)
        log_stream.write("trimmed data (line_out) is " + line_out + "\n") # remove # bytes, addr, rec_type, checksum
        if not line_out == '':
            # hex_buffer_out.write(line_out)  # write line_out string to temp buffer hex file
            write_to_bin(line_out)  # Write line_out as formatted to bin file (displayed as ascii currenty...)


def write_to_bin(line_out):
    line_out = line_out.strip()  # EDITED: Try stripping to get rid of erroneous carriage returns
    bin_out_stream.write(binascii.unhexlify(line_out))  # EDITED


def exitroutine():
    root.destroy()
    sys.exit(0)


root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", exitroutine)
root.withdraw()
get_hex_file()
data_work()
