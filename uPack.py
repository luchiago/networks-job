class uPack:
    def __init__(self, send_port, dest_port, id_seq, isAck, RST, SYN, FIN, data):
        self.send_port = send_port
        self.dest_port = dest_port
        self.id_seq = id_seq
        self.isAck = isAck
        self.RST = RST
        self.SYN = SYN
        self.FIN = FIN
        self.data = data