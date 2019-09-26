import socket

HOST = "localhost"
PORT = 4000

# criando o socket (socket.SOCK_DGRAM para ser UDP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# realizando o bind com a porta e o endereço
server_socket.bind((HOST, PORT))

print("Servidor iniciado.")

while True:
    msg, client = server_socket.recvfrom(2048)
    print("Mensagem recebida de " + str(client) + " : " + msg)

server_socket.close()