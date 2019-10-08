import socket, json
from uPack import *
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

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

@timeout(3)
def send_pack(uPack):
    msg = uPack.toString()
    msg_bytes = str.encode(msg)
    return send_sock.sendto(msg_bytes, (send_ip, dest_port))
    

def sendAck(id_seq):
    uPack(sender_port, dest_port, id_seq, True, None)


def make_pack(data):
    # send_port, dest_port, id_seq, isAck, checksum,  data
    pack = uPack(sender_port, dest_port, None, False, data)
    return pack

def receive():
    msg_bytes, server =  recv_sock.recvfrom(SEG_SIZE)
    res_pkt = json.loads(msg_bytes.decode())

    send_prt = res_pkt['send_port']
    dest_prt = res_pkt['dest_port']
    id = res_pkt['id_seq']
    ack = res_pkt['isAck']
    data = res_pkt['data']
    
    pkt = uPack(send_prt, dest_prt, id, ack, data)

    return pkt

def send_msg(msg):
    global prox_id
    pkt = make_pack(msg)
    pkt.setId_req(prox_id)
    prox_id = 1 - prox_id
    expected = pkt.id_seq
    ack = send_pack(pkt)
    resp = receive()
    
    while True:
        if isinstance(ack, TimeoutError) or (resp.isAck and resp.id_seq != expected):
            print("Timeout. Pacote " + str(pkt.id_seq) + " perdido. Reenviando.")
            send_pack(pkt)
            ack = recv_sock.recvfrom(SEG_SIZE)
            continue
        else:
            print("Recebido ACK " + str(ack.id_seq))
            break
    
    return True

def listen():
    msg_bytes, peer = recv_sock.recvfrom(SEG_SIZE)
    msg = msg_bytes.decode()
    print("Recebido de " + str(peer) + str(msg))
    res_pkt = json.loads(msg)

    if res_pkt['data'] == "RST":
        global send_ip
        send_ip = peer[0]
        pkt = make_pack("SYN")
        send_pack(pkt)
    
        return True
        
### MAIN HERE ###

SEG_SIZE = 100
prox_id = 0
sender_port = 4000
dest_port = 5000
send_ip = "localhost"
my_ip = get_ip()

send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# ativando o listen do servdor
recv_sock.bind((my_ip, sender_port))

listen()