from scapy.layers.inet import IP, UDP
from scapy.sendrecv import sr1, send
import struct

def calc_checksum(pacote):
    data = pacote.__bytes__()

    if len(data) % 2 == 1:
        data += b'\x00'

    total = sum(struct.unpack("!%dH" % (len(data) // 2), data))

    while total > 0xFFFF:
        total = (total & 0xFFFF) + (total >> 16)

    return ~total & 0xFFFF

pacote = IP(dst="15.228.191.109")
pacote /= UDP(sport=59155, dport=50000, chksum=0x0000)
pacote /= b"\x00\xf0\x59"

checksum = calc_checksum(pacote)

pacote = IP(dst="15.228.191.109")
pacote /= UDP(sport=59155, dport=50000, chksum=checksum)
pacote /= b"\x00\xf0\x59"

pacote.show()

resultado = sr1(pacote)

resultado.show()