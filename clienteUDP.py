from socket import *
import os
import random

server_address = ("15.228.191.109", 50000)
clientSocket = socket(AF_INET,
SOCK_DGRAM)

menu = """Escolha o tipo da requisição:1
1: Solicitar a data
2: Solicitar uma frase motivacional
3: Quantidade de respostas emitidas pelo servidor
4: Sair
"""

req = "0000"
tipo = "0000"
identificador = str(random.randint(1, 65535))

validResponse = False
while not validResponse:
    os.system("cls")

    choice = input(menu)
    
    match(choice):
        case "1":
            tipo = "0000"
            validResponse = True
        case "2":
            tipo = "0001"
            validResponse = True
        case "3":
            tipo = "0010"
            validResponse = True
        case "4":
            quit()
        case _:
            pass

message = req + tipo + identificador

clientSocket.sendto(message.encode(), server_address)

data, serverAddress = clientSocket.recvfrom(2048)

print(data.decode())

clientSocket.close()