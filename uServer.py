import socket, json
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
def receive():
    msg_bytes, server =  recv_sock.recvfrom(SEG_SIZE)
    print(msg_bytes.decode())
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
            ack = receive()      
        except timeout:
            print("Timeout")
        else:
            if ack.isAck and ack.id_seq == expected:
                print("ACK " +str() + " recebido")
                ack = True
       
    return True
 
### MAIN HERE ###
 
SEG_SIZE = 1000
prox_id = 0
sender_port = 4000
dest_port = 5000
send_ip = "10.13.28.50"
my_ip = "10.13.37.191"
 
send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# ativando o listen do servdor
recv_sock.bind((my_ip, sender_port))
recv_sock.settimeout(2)
 
last_pkt_id = 0
 
msg_received = False

fire_moves = [app.Move("Tackle", 12.0, 100.0, 10), app.Move(
    "QuickAttack", 14.0, 100.0, 7), app.Move("Ember", 15.0, 100.0, 7)]
charmander = app.Pokemon("Charmander", 5, fire_moves)

pokemon_remote = None
finished = False
while not finished:
    while not msg_received:
        try:
            pkt = receive()
        except timeout:
            msg_received = False
        else:
            # caso receba o pkt novamente, reenvia o ack perdido
            if pkt.id_seq == last_pkt_id:
                ack = send_pack(pkt)
            else:
                if pkt.data == "You lose":
                    send_msg("You are a good trainer")
                    finished = True
                else:
                    # mensagem não repetida, enviando ack
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
    charmander = local_pokemon
    app.turn(charmander, remote_pokemon)
    
    if remote_pokemon.health < 0:
        print(remote_pokemon.name + " has been defeated!")
        print(charmander.name + " WIN!")
        print("END GAME")
        msg = "You lose"
        send_msg(msg)
        msg_received = False
        finished = True

    pokemon_data = app.prepare_dic(charmander)
    pokemon_data = [pokemon_data, remote_pokemon]
    pokemon_data = pokemon_data.__str__()
    send_msg(pokemon_data)
    msg_received = False
