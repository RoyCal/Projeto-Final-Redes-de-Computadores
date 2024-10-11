from socket import *
import os
import random

server_address = ("15.228.191.109", 50000) # definindo o endereço IP e a porta do servidor
clientSocket = socket(AF_INET, SOCK_DGRAM) # criando o socket com protocolo IPv4 e protocolo UDP

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

clientSocket.sendto(message, server_address) # envia a mensagem para o servidor

data, serverAddress = clientSocket.recvfrom(2048) # recebe a resposta do servidor

os.system("cls")
print("Resposta do servidor:")
print(data) # imprime a resposta

clientSocket.close() # fecha a conexão