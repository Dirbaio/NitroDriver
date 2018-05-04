import usb.core
import usb.util
import binascii
import struct
import time


def fromhex(s):
    return binascii.unhexlify(s.encode('utf-8'))
def tohex(s):
    return binascii.hexlify(s).decode('utf-8')
def tohex_short(data):
    if len(data) < 64:
        return tohex(data)
    return tohex(data[:30]) + ".." + tohex(data[-30:])


def read_file(fn):
    with open(fn, mode='rb') as f:
        return f.read()
