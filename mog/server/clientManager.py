import socket
import traceback

class ClientsInfo:
    connected_clients = []
    idCount = 0

class PseudoClient:

    def __init__(self,conn:socket.socket,addr,id):
        self.conn = conn
        self.ipaddr = addr
        self.id = id

        self.listenerThread = None

        self.running=True

        self.log(f"Created instance for Client [Id: {self.id}, Ip: {self.ipaddr}]")


    def log(self,*args,**kwargs):
        print(f"[pClient {self.id} : {self.ipaddr}]",*args,**kwargs)

    def Listener(self):
        self.log("Listener thread started")
        while self.running:
            try:
                raw_data = self.conn.recv(2048)
                data = raw_data.decode()
                self.log(f"Recieved: {data}","from Client!")



            except Exception as e:
                print("An Error has occured at pClient Listener:")
                traceback.print_last()
                break

        self.log("Listener has stopped.",f"Data: [self.running:{self.running}]")