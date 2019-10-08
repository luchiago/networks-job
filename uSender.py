import socket, json
from socket import timeout
from uPack import *

# evia um pacote para o destino
def send_pack(uPack):
    msg = uPack.toString()
    msg_bytes = str.encode(msg)
    return send_sock.sendto(msg_bytes, (send_ip, dest_port))

# envia um ack com o id de sequencia fornecido
def sendAck(id_seq):
    ack = uPack(sender_port, dest_port, id_seq, True, None)
    send_pack(ack)

# cria um pacote com a mensagem recebida
def make_pack(data):
    # sender_port, dest_port, id_seq, isAck, checksum,  data
    pack = uPack(sender_port, dest_port, None, False, data)
    return pack

# transforma um json em um pacote uPack
def mount_pack(jsn):
    send_prt = jsn['send_port']
    dest_prt = jsn['dest_port']
    id = jsn['id_seq']
    ack = jsn['isAck']
    data = jsn['data']
    
    pkt = uPack(send_prt, dest_prt, id, ack, data)
    return pkt

# recebe uma mensagem
def receiv():
    msg_bytes, server =  recv_sock.recvfrom(SEG_SIZE)
    res_pkt = json.loads(msg_bytes.decode())
    
    pkt = mount_pack(res_pkt)

    return pkt

# envia um pacote com a mensagem recebida e gerencia seu ack de confirmcao
def send_msg(msg):
    global prox_id
    # criando o pkt
    pkt = make_pack(msg)
    # set id de sequencia
    pkt.setId_req(prox_id)
    # atualizando o prox id
    prox_id = 1 - prox_id
    # id seq do ack esperado
    expected = pkt.id_seq
    
    ack = False

    while not ack:
        # envia o pkt
        send_pack(pkt)
        try:
            # tenta receber o ack referente
            ack = receiv()      
        except timeout:
            # caso não receba antes do timeout, renvia
            print("Timeout")
        else:
            # caso receba um pkt antes do timeout, verifica se é ack e o esperado
            if ack.isAck and ack.id_seq == expected:
                print("ACK " +str(ack.id_seq) + " recebido")
                ack = True
        
    return True

### MAIN HERE ###

SEG_SIZE = 100
prox_id = 0
sender_port = 5000
dest_port = 4000

send_ip = input("IP destino: ")
my_ip = input("meu ip: ")


send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# ativando o listen do servdor
recv_sock.bind((my_ip, sender_port))
recv_sock.settimeout(2)

last_pkt_id = 0

def send(msg):
    while True:
        if send_msg(msg):
            break
    
def receive():
    while True:
        try:
            # tentando receber uma mensagem
            pkt = receiv()
        except timeout:
            # timeout = nenhuma mensagem recebida, não fazer nada
            continue
        else:
            # se o pacote recebido igual, o ack foi perdido. Reenviando
            if pkt.id_seq == last_pkt_id:
                sendAck(last_pkt_id)
            else:
                # caso receba o pkt novo envia o ack e atualiza o last_pkt_id
                sendAck(pkt.id_seq)
                last_pkt_id = pkt.id_seq

def set_ip_dest(ip):
    global send_ip
    send_ip = ip

def set_my_ip(ip):
    global my_ip
    my_ip = ip

while True:
    send_msg(input("Sua msg: "))
    msg = receive()
    print(" <<< " + str(msg.data))
    
