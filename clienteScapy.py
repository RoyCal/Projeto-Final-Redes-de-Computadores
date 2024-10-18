from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether
from scapy.sendrecv import srp1

pacote = Ether()
pacote /= IP(dst="15.228.191.109", len=0x001f, chksum=0x0000, ttl=128)
pacote /= UDP(sport=62719, dport=50000, chksum=0x0000, len=0x000b)
pacote /= "\x00\xf0\x59"

hex_string = ''.join(f'\\x{byte:02x}' for byte in bytes(pacote))

if((len(hex_string) / 4) % 2 != 0):
    hex_string += "\\x00"

print(hex_string)

byte_list = [int(hex_string[i:i+2] + hex_string[i+4:i+6], 16) for i in range(2, len(hex_string), 8)]

soma = hex(sum(byte_list))

soma_bin = "{:032b}".format(int(soma, 16))

soma = hex(int(soma_bin[:16], 2) + int(soma_bin[16:], 2))

checksum = "0x"

for num in soma[2:]:
    checksum += hex(15 - int(num, 16))[2:]

print(soma)

print(checksum)

pacote = Ether()
pacote /= IP(dst="15.228.191.109", len=0x001f, chksum=0x0000, ttl=128, id=48085)
pacote /= UDP(sport=62719, dport=50000, chksum=int("9f1d", 16), len=0x000b)
pacote /= "\x00\xf0\x59"

pacote.show()

resultado = srp1(pacote)

resultado.show()