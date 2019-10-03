import socket
from multiprocessing import TimeoutError
from multiprocessing.pool import ThreadPool

def timeout(seconds):
    def decorator(function):
        def wrapper(*args, **kwargs):
            pool = ThreadPool(processes=1)
            result = pool.apply_async(function, args=args, kwds=kwargs)
            try:
                return result.get(timeout=seconds)
            except TimeoutError as e:
                return e
        return wrapper
    return decorator

@timeout(5)
def send_msg(msg_bytes, dest):
    client_socket.sendto(msg_bytes, dest)
    msg_bytes, client = client_socket.recvfrom(2048)
    if msg_bytes.decode() == "ACK":
        return msg_bytes.decode()
    

HOST = "localhost"
PORT = 4000

# criando o socket para o cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind((HOST, 3000))
# endereço do servidor
servidor = (HOST, PORT)

print("Cliente iniciado")

while True:
    ack = ""
    # recebendo a mensagem a ser enviada
    msg = input()
    # convertendo para bytes
    msg_bytes = str.encode(msg)
    # realizando o envio
    while ack != "ACK":
        ack = send_msg(msg_bytes, servidor)
        if isinstance(ack, TimeoutError):
            print('Pacote perdido! Reenviando!')
            ack = send_msg(msg_bytes, servidor)
            continue
        else:
            print('Recebido ', ack)

client_socket.close()