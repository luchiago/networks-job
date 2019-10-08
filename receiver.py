from socket import socket, AF_INET, SOCK_DGRAM
from sys import argv, stdout
from common import ip_checksum


def send(content, to):
    checksum = ip_checksum(content)
    send_sock.sendto(checksum + content, to)

if __name__ == "__main__":
    dest_addr = "10.94.15.48"
    dest_port = 1602
    dest = (dest_addr, dest_port)
    listen_addr = "10.13.37.191"
    listen_port = 1601
    listen = (listen_addr, listen_port)

    send_sock = socket(AF_INET, SOCK_DGRAM)
    recv_sock = socket(AF_INET, SOCK_DGRAM)

    recv_sock.bind(listen)

    expecting_seq = 0

    while True:
        message, address = recv_sock.recvfrom(4096)
        checksum = message[:2]
        seq = message[2]
        content = message[3:]
        show = content.decode()

        if ip_checksum(content) == checksum:
            send("ACK" + seq, dest)
            if seq == str(expecting_seq):
                print show
                #stdout.write(content)
                expecting_seq = 1 - expecting_seq
        else:
            negative_seq = str(1 - expecting_seq)
            send("ACK" + negative_seq, dest)
