import struct

def make_branch(from_addr, to_addr, link):
    res = 0xEA000000
    if link:
        res |= 0x01000000

    offs = (to_addr // 4) - (from_addr // 4) - 2
    offs &= 0x00FFFFFF
    res |= offs

    return res


header = struct.pack(
    'II',
    make_branch(0x02700000, 0x02701000, False),
    make_branch(0x02700004, 0x02710000, False)
)

with open('header.bin', 'wb') as f:
    f.write(header)
