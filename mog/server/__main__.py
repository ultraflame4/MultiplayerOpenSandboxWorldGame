import socket
import threading
import time
import traceback

import serverworld

class ClientsInfo:
    connected_clients = {}
    idCount = 0

def dummyfunc(*args,**kwargs):
    pass

class ClientHandler:

    def __init__(self,conn:socket.socket,addr,id):
        self.conn = conn
        self.ipaddr = addr
        self.id = id

        self.listenerThread = threading.Thread(target=self.Listener)

        self.running=True




        self.log(f"Created instance for client")


        self.log("Starting listener thread for client")
        self.listenerThread.start()


        #CALLBACKS
        self.player_pos_cb = dummyfunc


        time.sleep(0.2)
        self.log("Adding player to world")
        serverworld.Manager.world.addPlayer(self)

    def log(self,*args,info=False,**kwargs):

        print(f"[pClient {self.id} : {self.ipaddr}]",*args,**kwargs)

    def send(self,data:str):
        self.conn.send(f"{data};?".encode())

    def Listener(self):
        self.log("Listener thread started")
        while self.running:
            try:
                raw_data = self.conn.recv(2048)
                data = raw_data.decode()


                # self.log(f"Recieved: {data}","from Client!")


                for d in data.split(';?'):
                    pdata = d.split(":",1)
                    dtype = pdata.pop(0)

                    if dtype not in ("player/pos"):
                        self.log(f"Recieved: {data}", "from Client!")

                    if dtype == "client/exit":
                        self.log("Client has disconnected. Stopping listener")
                        self.running=False

                    elif dtype == "player/pos":
                        self.player_pos_cb(pdata[0])


            except ConnectionResetError:
                self.log("Client has unexpectedly disconnected..")
                self.running=False




            except Exception as e:
                print("\nAn Error has occured at pClient Listener:\n")
                print(traceback.format_exc())
                break

        self.log("Listener has stopped.",f"Data: [self.running:{self.running}]")
        serverworld.Manager.world.removePlayer(self)
        self.conn.close()


server="localhost"
port=8888
serverip = socket.gethostbyname(server)


def addClient(conn,addr):
    ClientsInfo.connected_clients[ClientsInfo.idCount]=ClientHandler(conn,addr,ClientsInfo.idCount)



    ClientsInfo.idCount+=1


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.bind((serverip,port))
    except socket.error as e:
        print(str(e))


    s.listen()
    print("Waiting for connection(s)...")

    while True:
        conn,addr = s.accept()
        print("Connected to:",addr)
        addClient(conn,addr)
