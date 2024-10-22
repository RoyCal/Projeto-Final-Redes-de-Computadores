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

pacote = IP(dst="15.228.191.109", proto="udp", len=31) # define o cabeçalho IP
pacote /= UDP(sport=59155, dport=50000, len=11, chksum=0x0000) # encapsula o cabeçalho UDP
pacote /= message # encapsula o payload 

checksum = calc_checksum(pacote) # calula o checksum do pacote

pacote_recebido = sr1(pacote) # envia um pacote ao servidor e captura a resposta

resultado = pacote_recebido.__bytes__() # converte o pacote recebido para bytes 

os.system("cls")

print("Mensagem enviada ao servidor:")
print(''.join(f'\\x{byte:02x}' for byte in message), end="\n\n") # imprime a mensagem enviada

print("Pacote completo enviado:")
print(''.join(f'\\x{byte:02x}' for byte in pacote.__bytes__()), end="\n\n") # imprime o pacote enviado em hexadecimal puro

pacote.show() # OBS.: o pacote é enviado com o checksum em 0x0000. O servidor não responde caso o checksum seja alterado para o valor calculado
              # Não sei se estamos calculando o checksum errado, mas acreditamos que não, pois realimos até cálculos manuais e deu o mesmo valor

print("Checksum do pacote enviado:", hex(checksum), end="\n\n") # imprime o checksum do pacote enviado ao servidor

print("Resposta do servidor:")
print(''.join(f'\\x{byte:02x}' for byte in resultado), end="\n\n")    # imprime a resposta do servidor em hexacecimal puro

print("Significado: ") # aqui abaixo são feitas as traduções dos hexadecimais para os caracteres ASCII

# os bytes da resposta que representam números são convertidos para inteiro automaticamente quando os acessamos, mas alguns deles são junções de mais de uma informação
# então precisamos converter alguns deles para binário a fim de obter essas informações
# é parecido com o cliente utilizando socketUDP mas agora precisamos pular a parte dos cabeçalhos para chegar até a mensagem

byte_0 = "{:08b}".format(resultado[28]) # converte o primeiro byte da resposta para binário
byte_1 = "{:08b}".format(resultado[29]) # converte o segundo byte da resposta para binário
byte_2 = "{:08b}".format(resultado[30]) # converte o terceiro byte da resposta para binário
byte_3 = resultado[31] # o quarto byte não precisa ser convertido pois corresponde ao tamanho da mensagem, que ocupa exatamente 1 byte

print("Tipo da mensagem:", byte_0[:4], "| Tipo da requisição:", byte_0[4:]) # a primeira metade do primeiro byte é o tipo da mensagem e a segunda metade é o tipo da requisição
print("Indentificador:", int(byte_1 + byte_2, 2)) # os dois bytes seguintes, isto é, o segundo e o terceiro, correspondem ao identificador
print("Tamanho da mensagem:", byte_3) # o quarto byte é o tamanho da mensagem

# do quinto byte em diante temos a mensagem, mas só pegamos o tamanho que o servidor forneceu no tamanho da mensagem...
if byte_0[4:] == "0010":
    print("Mensagem:", int.from_bytes(resultado[32:32 + byte_3], "big")) # no caso da quantidade de requisições, precisamos converter do formato "\x00\x00\x00\x00" para inteiro, pois  
else:                                                             # o programa pode interpretar cada "\x00" como um caractere ASCII, e não como um inteiro de 8 bits
    print("Mensagem:", resultado[32:32 + byte_3].decode()) # nos demais casos, o "\x00" deve ser interpretado como um caractere ASCII, então apenas chamamos o método decode