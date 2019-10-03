import socket
from common import ip_checksum
import uPack

SEG_SIZE = 100
send_port = 4000
dest_port = 5000
send_ip = "localhost"

send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_pack(uPack):
    msg = uPack.toString()
    msg_bytes = str.encode(msg)
    send_sock.sendto(msg_bytes, (send_ip, send_port))
    

def sendAck(id_seq):
    uPack(send_port, dest_port, id_seq, True, None, None)


def make_pack(data):
            # send_port, dest_port, id_seq, isAck, checksum,  data
    pack = uPack(send_port, dest_port, None, False, ip_checksum(data), data)
    return pack