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
    
    # retorna o objeto em formato de string json
    def toString(self):
        msg = "{"
        msg += "send_port: " + str(self.send_port) + ","
        msg += "dest_port: " + str(self.dest_port) + ","
        msg += "id_seq: " + str(self.id_seq) + ","
        msg += "isAck: " + str(self.isAck) + ","
        msg += "RST: " + str(self.RST) + ","
        msg += "SYN: " + str(self.SYN) + ","
        msg += "FIN: " + str(self.FIN) + ","
        msg += "data: " + str(self.data) + ""
        msg += "}"
        
        return msg