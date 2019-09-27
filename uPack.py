class uPack:
    def __init__(self, send_port, dest_port, id_seq, isAck, checksum,  data):
        self.send_port = send_port
        self.dest_port = dest_port
        self.id_seq = id_seq
        self.isAck = isAck
        self.checksum = checksum
        self.data = data
    
    # retorna o objeto em formato de string json
    def toString(self):
        msg = "{"
        msg += "send_port: " + str(self.send_port) + ","
        msg += "dest_port: " + str(self.dest_port) + ","
        msg += "id_seq: " + str(self.id_seq) + ","
        msg += "isAck: " + str(self.isAck) + ","
        msg += "checksum: " + str(self.checksum) + ","
        msg += "data: " + str(self.data) + ""
        msg += "}"
        
        return msg
    def setId_req(self, id_rec):
        self.id_seq = id_rec