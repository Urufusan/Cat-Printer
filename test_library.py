# this script tries to use printer.py as a library.
import printer as prtlib
import time
import atexit
import sys
import subprocess
import new_pbm_generator
import os

def zenity_file_dialog(dialog_mode_type : int):
    try:
        # Use the zenity command to open a file dialog
        match dialog_mode_type:
            case 1:
                file_path = subprocess.run("zenity --title='BunnyPrint' --file-selection --save --confirm-overwrite --file-filter='Image file | *' --filename=BUP-$(date +'%Y-%b-%d').fmbsx.gz", capture_output=True, shell=True).stdout.decode().strip()
            case 2:
                file_path = subprocess.run("zenity --title='BunnyPrint' --file-selection --file-filter='Image file | *'", capture_output=True, shell=True).stdout.decode().strip()
            case _:
                raise IOError("Unknown file dialog operation")
        return file_path
    except subprocess.CalledProcessError:
        print("Error: Unable to open file dialog.")
        return ""


printer : prtlib.PrinterDriver = None
def safeunload():
    global printer
    if printer is not None:
        if printer.device is not None:
            # print("state ->", printer.device.is_connected)
            if printer.device.is_connected: printer.unload()
    input("!! >> ")

atexit.register(safeunload)

def create_prt_object(scantime : float = 2.0, energy : float = 0.1, quality : int = 4, speedmul : float = 1, image_param : str = ""):
    global printer
    energy = int(energy * 0xffff)
    printer = prtlib.PrinterDriver()
    printer.scan_time = scantime
    printer.energy = energy
    printer.speed = (4 * (quality + 5)) * speedmul
    if 'flip' in image_param:
        printer.flip_h = True
        printer.flip_v = True
    elif 'fliph' in image_param:
        printer.flip_h = True
    elif 'flipv' in image_param:
        printer.flip_v = True
    print(ptr_list := printer.scan("EE:10:16:21:45:11"))
    printer.connect(ptr_list[0].name, ptr_list[0].address)
    return printer

def print_image(printer : prtlib.PrinterDriver, arg_file, unload : bool = False):
    file = arg_file
        
    mode = 'pbm'
    mag_image = new_pbm_generator.create_image(file, printer.model.paper_width) 
    try:
        printer.print(mag_image, mode=mode)
    finally:
        if hasattr(file, "close"): file.close()
        mag_image.close()
        if unload: printer.unload()

def print_text(printer : prtlib.PrinterDriver, text_str, font_family = "Ubuntu Mono", align_text = "left", font_size = 120, unload : bool = False):
    # if arg_file == '-':
    #     file = sys.stdin.buffer
    # else:
    #     file = open(arg_file, 'rb')
    
    mode = 'pbm'
    mag_image = new_pbm_generator.create_text_image(text_str, printer.model.paper_width, font_family, font_size, align_text) 
    try:
        printer.print(mag_image, mode=mode)
    finally:
        mag_image.close()
        if unload: printer.unload()


if __name__ == "__main__":
    # while not (z := int(input("Select program mode\n1. Text\n2.Image\n>> "))) < 3:
    #     print("Enter a valid choice.")
    z = 1 if sys.argv[1].strip() != "nautilus-menu" else 3
    match z:
        case 1:
            # le_text = os.popen("neofetch --stdout | fold -w 40 -s").read()
            le_text = "Centered text test\nWith multiple\nlines\nand things" if sys.stdin.isatty() else sys.stdin.read()
            print(le_text)
            prt = create_prt_object(speedmul=3)
            print_text(prt, le_text, "Impact", align_text="center")
        case 2:
            # fpath = zenity_file_dialog(2)
            fpath = "~/Pictures/nikoaf5.png"
            print(fpath)
            prt = create_prt_object(speedmul=3)
            print_image(prt, fpath)
        case 3:
            fpaths = sys.argv[2:]
            print(fpaths)
            prt = create_prt_object()
            for fpath in fpaths:
                print_image(prt, fpath)
        case _:
            print("haha funne")