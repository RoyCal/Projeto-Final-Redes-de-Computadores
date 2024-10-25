# Vito Elias, Pedro Márcio e Rivando Neto

from socket import *
import os
import random

server_address = ("15.228.191.109", 50000) # definindo o endereço IP e a porta do servidor
clientSocket = socket(AF_INET, SOCK_DGRAM) # criando o socket com protocolo IPv4 e protocolo UDP

impressao_detalhada = True # variável que controla o tipo da impressão

# menu que será impresso
menu = """Escolha o tipo da requisição:
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

    if impressao_detalhada:
        print("(Impressão detalhada) ---- pressione ENTER para mudar", end="\n\n") # mostra qual tipo de impressão está selecionado
    else:
        print("(Impressão simplificada) - pressione ENTER para mudar", end="\n\n")

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
        case "":
            impressao_detalhada = impressao_detalhada ^ True # inverte o estado da variável
        case _:
            pass          # Opção inválida inserida pelo usuário

byte_0 = int(req + tipo, 2) # o primeiro byte é composto pelos 4 bits que indicam o tipo da mensagem (requisição ou resposta) + os 4 bits do tipo da requisição
byte_1 = int(identificador[:8], 2) # o segundo byte é a primeira metade do identificador
byte_2 = int(identificador[8:], 2) # o terceiro byte é a segunda metade do identificador

message = bytes([byte_0, byte_1, byte_2]) # unindo os pedaços para formar a mensagem

clientSocket.sendto(message, server_address) # envia a mensagem para o servidor

data, serverAddress = clientSocket.recvfrom(2048) # recebe a resposta do servidor

# os bytes da resposta que representam números são convertidos para inteiro automaticamente quando os acessamos, mas alguns deles são junções de mais de uma informação
# então precisamos converter alguns deles para binário a fim de obter essas informações

byte_0 = "{:08b}".format(data[0]) # converte o primeiro byte da resposta para binário
byte_1 = "{:08b}".format(data[1]) # converte o segundo byte da resposta para binário
byte_2 = "{:08b}".format(data[2]) # converte o terceiro byte da resposta para binário
byte_3 = data[3] # o quarto byte não precisa ser convertido pois corresponde ao tamanho da mensagem, que ocupa exatamente 1 byte

if impressao_detalhada:
    os.system("cls")

    print("Mensagem enviada ao servidor:")
    print(''.join(f'\\x{byte:02x}' for byte in message), end="\n\n") # imprime a mensagem enviada para o servidor em hexadecimal puro

    print("Resposta do servidor:")
    print(''.join(f'\\x{byte:02x}' for byte in data), end="\n\n")    # imprime a resposta do servidor em hexacecimal puro

    print("Significado: ") # aqui abaixo são feitas as traduções dos hexadecimais para os caracteres ASCII

    print("Tipo da mensagem:", byte_0[:4], "| Tipo da requisição:", byte_0[4:]) # a primeira metade do primeiro byte é o tipo da mensagem e a segunda metade é o tipo da requisição
    print("Indentificador:", int(byte_1 + byte_2, 2)) # os dois bytes seguintes, isto é, o segundo e o terceiro, correspondem ao identificador
    print("Tamanho da mensagem:", byte_3) # o quarto byte é o tamanho da mensagem

    # do quinto byte em diante temos a mensagem, mas só pegamos o tamanho que o servidor forneceu no tamanho da mensagem...
    if byte_0[4:] == "0010":
        print("Mensagem:", int.from_bytes(data[4:4 + byte_3], "big")) # no caso da quantidade de requisições, precisamos converter do formato "\x00\x00\x00\x00" para inteiro, pois  
    else:                                                             # o programa pode interpretar cada "\x00" como um caractere ASCII, e não como um inteiro de 8 bits
        print("Mensagem:", data[4:4 + byte_3].decode()) # nos demais casos, o "\x00" deve ser interpretado como um caractere ASCII, então apenas chamamos o método decode
else:
    os.system("cls")

    # do quinto byte em diante temos a mensagem, mas só pegamos o tamanho que o servidor forneceu no tamanho da mensagem...
    if byte_0[4:] == "0010":
        print(int.from_bytes(data[4:4 + byte_3], "big")) # no caso da quantidade de requisições, precisamos converter do formato "\x00\x00\x00\x00" para inteiro, pois  
    else:                                                             # o programa pode interpretar cada "\x00" como um caractere ASCII, e não como um inteiro de 8 bits
        print(data[4:4 + byte_3].decode()) # nos demais casos, o "\x00" deve ser interpretado como um caractere ASCII, então apenas chamamos o método decode

clientSocket.close() # fecha a conexão