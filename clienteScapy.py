from scapy.layers.inet import IP, UDP
from scapy.sendrecv import sr1
import struct

def calc_checksum(pacote):
    data = pacote.__bytes__() # converte o pacote para o bytes

    if len(data) % 2 == 1: # se o pacote tiver um número ímpar de bytes, adiciona um \x00 ao final
        data += b'\x00'

    total = sum(struct.unpack("!%dH" % (len(data) // 2), data)) # desempacota os dados em uma tupla de inteiros, que possuem 2 bytes, e faz a soma

    total = (total & 0xFFFF) + (total >> 16) # soma os 16 bits mais significativos com os 16 bits menos significativos

    return ~total & 0xFFFF # inverte os bits para fazer o complemento de 1 e limita o valor a 2 bytes

pacote = IP(dst="15.228.191.109")
pacote /= UDP(sport=59155, dport=50000, chksum=0x0000)
pacote /= b"\x00\xf0\x59"

checksum = calc_checksum(pacote)

pacote.show()

resultado = sr1(pacote)

resultado.show()