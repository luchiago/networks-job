import socket

HOST = "localhost"
PORT = 4000

# criando o socket para o cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# endereço do servidor
servidor = (HOST, PORT)

print("Cliente iniciado")

while True:
    # recebendo a mensagem a ser enviada
    msg = input()
    # convertendo para bytes
    msg_bytes = str.encode(msg)
    # realizando o envio
    client_socket.sendto(msg_bytes, servidor)

client_socket.close()