from scapy.layers.inet import IP, UDP
from scapy.sendrecv import srp1

pacote = IP(dst="15.228.191.109")
pacote /= UDP(dport=50000, chksum=0x0000)
pacote /= "\x00\x57\x22"

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

pacote = IP(dst="15.228.191.109")
pacote /= UDP(dport=50000, chksum=int(checksum, 16))
pacote /= "\x00\x57\x22"

resultado = srp1(pacote)

resultado.show()