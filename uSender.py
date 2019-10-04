import socket
from common import ip_checksum
import uPack
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

SEG_SIZE = 100
prox_id = 0
send_port = 4000
dest_port = 5000
send_ip = "localhost"
my_ip = "localhost"

send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_sock.bind((my_ip, send_port))

@timeout(3)
def send_pack(uPack):
    msg = uPack.toString()
    msg_bytes = str.encode(msg)
    return send_sock.sendto(msg_bytes, (send_ip, send_port))
    

def sendAck(id_seq):
    uPack(send_port, dest_port, id_seq, True, None, None)


def make_pack(data):
    # send_port, dest_port, id_seq, isAck, checksum,  data
    pack = uPack(send_port, dest_port, None, False, ip_checksum(data), data)
    return pack

def send_msg(msg):
    pkt = make_pack(msg)
    pkt.setId_req(prox_id)
    prox_id = 1 - prox_id
    expected = pkt.id_seq
    send_pack(pkt)
    ack = recv_sock.recvfrom(SEG_SIZE)

    while True:
        if isinstance(ack, TimeoutError) or ack.id_seq != expected:
            print("Timeout. Pacote " + str(pkt.id_seq) + " perdido. Reenviando.")
            send_pack(pkt)
            ack = recv_sock.recvfrom(SEG_SIZE)
            continue
        else:
            print("Recebido ACK " + str(ack.id_seq))
            break
    
    return True