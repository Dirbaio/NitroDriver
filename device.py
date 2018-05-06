import usb.core
import usb.util
import binascii
import struct
import time

from util import tohex, fromhex

class NitroDevice:
    def __init__(self):
        # find our device
        self.dev = usb.core.find(idVendor=0x0f6e, idProduct=0x0404)

        # was it found?
        if self.dev is None:
            raise ValueError('Device not found')

        # set the active configuration. With no arguments, the first
        # configuration will be the active one
        self.dev.set_configuration()
        self.dev.reset()  # Avoids weird timeout errors when running the program multiple times.

        # get an endpoint instance
        cfg = self.dev.get_active_configuration()
        intf = cfg[(0,0)]

        self.ep_out = usb.util.find_descriptor(intf, bEndpointAddress = 0x01)
        self.ep_in = usb.util.find_descriptor(intf, bEndpointAddress = 0x82)
        assert self.ep_out is not None
        assert self.ep_in is not None


    def usb_read(self, size):
        res = b''
        while len(res) < size:
            res += bytes(self.ep_in.read(size - len(res)))
        return res

    def usb_write(self, data):
        while len(data) != 0:
            written = self.ep_out.write(data)
            data = data[written:]


    def read(self, code, size):
        cmd = struct.pack(
            "hBBiii",
            code,
            0x11, 0, # some flags?
            0, # unknown
            size,
            0, # unknown
        )
        self.usb_write(cmd)
        res = self.usb_read(size)
        print('read {:02x} {:08x} = {}'.format(code, size, tohex(res)))
        return res

    def write(self, code, data):
        cmd = struct.pack(
            "hBBiii",
            code,
            0x10, 0, # some flags?
            0, # unknown
            len(data),
            0, # unknown
        )
        print('write {:02x} {:08x} = {}'.format(code, len(data), tohex(data)))
        self.usb_write(cmd + data)


    def read_offs(self, code, code2, offs, size):
        cmd = struct.pack(
            "hBBiii",
            code,
            0x11, code2, # some flags?
            offs, # unknown
            size,
            0, # unknown
        )
        print('read_offs {:02x} {:01x} {:08x} {:08x}'.format(code, code2, offs, size))
        self.usb_write(cmd)
        res = self.usb_read(size)
        return res

    def write_offs(self, code, code2, offs, data):
        cmd = struct.pack(
            "hBBiii",
            code,
            0x10, code2, # some flags?
            offs,
            len(data),
            0, # unknown
        )
        print('write_offs {:02x} {:01x} {:08x} {:08x}'.format(code, code2, offs, len(data)))
        self.usb_write(cmd + data)


    def slot2_read(self, offs, size):
        return self.read_offs(0, 2, offs, size)

    def slot2_write(self, offs, data):
        self.write_offs(0, 2, offs, data)


    def slot1_read(self, offs, size):
        chunk_len = 0x10000
        data = b''
        while len(data) < size:
            n = min(size-len(data), chunk_len)
            data += self.read_offs(0, 1, offs + len(data), n)
        return data

    def slot1_write(self, offs, data):
        chunk_len = 0x100000 # 1MB
        i = 0
        while i < len(data):
            n = min(len(data)-i, chunk_len)
            self.write_offs(0, 1, offs + i, data[i:i+n])
            i += n

    def slot1_write_checked(self, offs, data):
        self.slot1_write(offs, data)
        data2 = self.slot1_read(offs, len(data))
        assert data == data2


    def slot1_on(self):
        self.write(0xad, fromhex('ad0000000a00000001000000000000000000000000000000'))

    def slot1_off(self):
        self.write(0xad, fromhex('ad0000000a00000000000000000000000000000000000000'))

    def slot1_emulate_eject(self):
        self.write(0xad, fromhex('ad0000000d00000001000000000000000000000000000000'))
        self.write(0xad, fromhex('ad0000000d00000000000000000000000000000000000000'))


    def slot2_on(self):
        self.write(0xad, fromhex('ad0000000200000001000000000000000000000000000000'))
        self.write(0xad, fromhex('ad0000000400000000000000000000000000000000000000'))

    def slot2_off(self):
        self.write(0xad, fromhex('ad0000000200000000000000000000000000000000000000'))

    def slot2_emulate_eject(self):
        self.write(0xad, fromhex('ad0000000500000001000000000000000000000000000000'))
        self.write(0xad, fromhex('ad0000000500000000000000000000000000000000000000'))

    # Reset the full IS-NITRO-EMULATOR (DS cpu, slot1, slot2 power settings, many more things?)
    def full_reset(self):
        self.write(0x81, fromhex('81f2'))

    # Resets the NDS hardware
    def nds_reset(self):
        self.write(0x8a, fromhex('8a000000'))

    # Stops the NDS hardware
    # Screens stop refreshing, leading to a cool fading effect!
    def nds_stop(self):
        self.write(0x8a, fromhex('8a000100'))

    def select_arm9(self):
        self.write(0x8b, fromhex('8b000000'))

    def select_arm7(self):
        self.write(0x8b, fromhex('8b000100'))

    def trigger_fiq(self):
        self.write(0xaa, fromhex('aa000100'))
        self.write(0xaa, fromhex('aa000000'))
