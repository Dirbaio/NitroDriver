import usb.core
import usb.util
import binascii
import struct
import time
import sys

from util import fromhex, tohex, tohex_short, read_file
from device import NitroDevice

def main():
    if len(sys.argv) != 2:
        print("Usage: nitro.py romfile.nds")
        return
    romfile = sys.argv[1]

    d = NitroDevice()

    d.full_reset()

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

    d.nds_reset()


if __name__ == '__main__':
    main()
