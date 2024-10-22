from scapy.layers.inet import IP, UDP
from scapy.sendrecv import sr1
import struct
import random
import os

def calc_checksum(pacote):
    data = pacote.__bytes__() # converte o pacote para o bytes

    if len(data) % 2 == 1: # se o pacote tiver um número ímpar de bytes, adiciona um \x00 ao final
        data += b'\x00'

    total = sum(struct.unpack("!%dH" % (len(data) // 2), data)) # desempacota os dados em uma tupla de inteiros, que possuem 2 bytes, e faz a soma

    total = (total & 0xFFFF) + (total >> 16) # soma os 16 bits mais significativos com os 16 bits menos significativos

    return ~total & 0xFFFF # inverte os bits para fazer o complemento de 1 e limita o valor a 2 bytes

# menu que será impresso
menu = """Escolha o tipo da requisição:1
1: Solicitar a data
2: Solicitar uma frase motivacional
3: Quantidade de respostas emitidas pelo servidor
4: Sair
"""

req = "0000" # 0000 significa uma requisição
tipo = "0000" # definindo 0000, que significa uma requisição de data, como default

identificador = "{:016b}".format(random.randint(1, 65535)) # sorteando o número identificador e convertendo para binário de 16 bits

validResponse = False
while not validResponse: # loop para escolher uma opção válida de requisição
    os.system("cls")

    choice = input(menu)
    
    match(choice):
        case "1":
            tipo = "0000" # Requisição de data
            validResponse = True
        case "2":
            tipo = "0001" # Requisição de frase motivacional
            validResponse = True
        case "3":
            tipo = "0010" # Requisição de quantidade de respostas emitidas pelo servidor
            validResponse = True
        case "4":
            quit()        # Finalizar o código do cliente
        case _:
            pass          # Opção inválida inserida pelo usuário

byte_0 = int(req + tipo, 2) # o primeiro byte é composto pelos 4 bits que indicam o tipo da mensagem (requisição ou resposta) + os 4 bits do tipo da requisição
byte_1 = int(identificador[:8], 2) # o segundo byte é a primeira metade do identificador
byte_2 = int(identificador[8:], 2) # o terceiro byte é a segunda metade do identificador

message = bytes([byte_0, byte_1, byte_2]) # unindo os pedaços para formar a mensagem

pacote = IP(dst="15.228.191.109")
pacote /= UDP(sport=59155, dport=50000, chksum=0x0000)
pacote /= message

checksum = calc_checksum(pacote)
print("Checksum do pacote enviado:", hex(checksum), end="\n\n")

resultado = sr1(pacote)
print(resultado.__bytes__())