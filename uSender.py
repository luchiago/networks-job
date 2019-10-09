import socket
import json
from socket import timeout
from uPack import *
import Application as app

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
    msg_bytes, server = recv_sock.recvfrom(SEG_SIZE)
    res_pkt = json.loads(msg_bytes.decode())

    pkt = mount_pack(res_pkt)

    return pkt

# envia um pacote com a mensagem recebida e gerencia seu ack de confirmcao


def send_msg(msg):
    global prox_id
    pkt = make_pack(msg)
    pkt.setId_req(prox_id)
    prox_id = 1 - prox_id
    expected = pkt.id_seq

    ack = False

    while not ack:
        send_pack(pkt)
        try:
            ack = receiv()
        except timeout:
            print("Timeout")
        else:
            if ack.isAck and ack.id_seq == expected:
                print("ACK " + str() + " recebido")
                ack = True

    return True

### MAIN HERE ###


SEG_SIZE = 1000
prox_id = 0
sender_port = 5000
dest_port = 4000
send_ip = "10.13.37.191"
my_ip = "10.13.28.50"

send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# ativando o listen do servdor
recv_sock.bind((my_ip, sender_port))
recv_sock.settimeout(2)

last_pkt_id = 0

eletric_moves = [app.Move("Thunderbolt", 15.0, 100.0, 7), app.Move(
    "QuickAttack", 14.0, 100.0, 7), app.Move("ThunderShock", 20.0, 100.0, 3)]
pikachu = app.Pokemon("Pikachu", 30, eletric_moves)
pokemon_remote = None
finished = False

while not finished:
    msg = app.prepare_dic(pikachu)
    msg = [msg, pokemon_remote]
    msg = msg.__str__()
    send_msg(msg)
    msg_received = False

    while not msg_received:
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
                # mensagem não repetida, enviando ack
                if pkt.data == "You lose":
                    print(pkt.data)
                    send_msg("You are a good trainer")
                    finished = True
                else:
                    pokemon_local = eval(pkt.data)[1]
                    pokemon_remote = eval(pkt.data)[0]
                sendAck(pkt.id_seq)
                msg_received = True
    moves = pokemon_remote['moves']
    remote_pokemon_move = []
    for move in moves:
        remote_pokemon_move.append(
            app.Move(move[0], move[1], move[2], move[3]))
    remote_pokemon = app.Pokemon(
        pokemon_remote['name'], pokemon_remote['health'], remote_pokemon_move)
    moves = pokemon_local['moves']
    local_pokemon_move = []
    for move in moves:
        local_pokemon_move.append(
            app.Move(move[0], move[1], move[2], move[3]))
    local_pokemon = app.Pokemon(
        pokemon_remote['name'], pokemon_remote['health'], remote_pokemon_move)
    pikachu = local_pokemon
    app.turn(pikachu, remote_pokemon)
    if remote_pokemon.health < 0:
        print(remote_pokemon.name + " has been defeated!")
        print(pikachu.name + " WIN!")
        print("END GAME")
        msg = "You lose"
        send_msg(msg)
        msg_received = False
        finished = True
