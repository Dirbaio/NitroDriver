import usb.core
import usb.util
import binascii
import struct
import time
import sys
import argparse

from util import fromhex, tohex, tohex_short, read_file
from device import NitroDevice

def nds_rom_launch( romfile, gba_on): 

    #Intercept eventual error detected by NitroDevice to display a clean Error message
    try:
        d = NitroDevice()
    except Exception as error:
        error_type, error_content, error_traceback = sys.exc_info()
        sys.exit('NitroDevice detected a ' + error_type.__name__ + ' : %s \nExiting...' % error_content)

    d.full_reset()

    #Technically, the full reset... fully reset the kit and power off every activated things. But sometime when testing, the slot2 got not shuted down. So, to be totally clean, i shut them off before doing anything
    d.slot1_off()
    d.slot2_off()

    d.nds_stop()

    d.slot1_write(0, read_file(romfile))

    debugrom = read_file('debugrom/debugrom.bin')
    d.slot1_write(0x0ff80000, debugrom)

    debugrom_len = len(debugrom)
    if debugrom_len & 0x1ff:
        debugrom_len &= ~0x1ff
        debugrom_len += 0x200
    d.slot1_write(0x160, struct.pack('IIII', 0x8ff80000, debugrom_len, 0x02700000, 0x02700004)) # Overwrite debug ROM pointers in header.

    d.slot1_on()

    if gba_on != False:
        d.slot2_on()

    d.nds_reset()

def gba_retail_launch():
    #Intercept eventual error detected by NitroDevice to display a clean Error message
    try:
        d = NitroDevice()
    except Exception as error:
        error_type, error_content, error_traceback = sys.exc_info()
        sys.exit('NitroDevice detected a ' + error_type.__name__ + ' : %s \nExiting...' % error_content)

    d.full_reset()

    d.slot2_off()

    d.nds_stop()

    d.slot2_on()

    d.nds_reset()

    print 'If the NDS menu don\'t start (black screen or NDS game launch), restart the IS-NITRO-DEBUGGER kit with the power switch, the kit need to be manually restarted after launching a GBA game (whatever you want to do) or a NDS game (only if you want to launch GBA games, otherwhise it\'s not needed)'

def main():
    parser = argparse.ArgumentParser(description='Welcome to NitroDrivers ! Get happy with your IS-NITRO-DEBUGGER and say goodbye to the windows only nintendo program !')
    parser.add_argument('-n', '--nds-rom', help='Launch a Nintendo DS rom. Need to be decrypted before (hello "ndstool -se my_rom_file.nds")')
    parser.add_argument('-g', '--gba-cart', help='Launch a Retail GBA cart. Need to be insered BEFORE power on the kit.', action='store_true')
    parser.add_argument('-7', '--gba-on', help='Start "System2"/GBA on the kit. Usefull only when launching NDS rom that use content from gba cart (example: Pokemon NDS games).', action='store_true') #-7 because the GBA proc is arm7, and -g already used. lol    

    args = parser.parse_args()
    
    if args.gba_cart == False and args.nds_rom == None:
        parser.print_help()
        return

    if args.nds_rom != None:
	nds_rom_launch(args.nds_rom, args.gba_on)
    elif args.gba_cart == True:
	gba_retail_launch()

if __name__ == '__main__':
    main()
