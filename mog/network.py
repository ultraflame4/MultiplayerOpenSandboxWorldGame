import threading
import socket

from mog import EventsHandler, networkConstants


class DataCallbacks:
    players_pos=None
    players_clear=lambda :print("Warning In network.py: DataCallbacks.players_clear func is not set")


class ConnectionHandler:
    serverip = None
    serverport = 8888
    listenerThread = None
    listening = False
    client:socket.socket=None

    @staticmethod
    def join_server(serverip,serverport=8888):
        print("Joining server...")
        ConnectionHandler.serverip = serverip
        ConnectionHandler.serverport=serverport

        ConnectionHandler.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ConnectionHandler.client.connect((serverip,serverport))


        ConnectionHandler.listenerThread=threading.Thread(target=ConnectionHandler.serverListener)
        ConnectionHandler.listening = True
        ConnectionHandler.listenerThread.start()


    @staticmethod
    def send(data:str):
        if ConnectionHandler.client is not None:
            ConnectionHandler.client.send(f"{data};?".encode())
        else:
            print("ConnectionHandler:","Socket is not ready")


    @staticmethod
    @EventsHandler.SubscribeEvent.quit
    def stopListener(event):
        ConnectionHandler.listening=False
        if ConnectionHandler.client is not None:
            ConnectionHandler.send(networkConstants.client_exit)
            ConnectionHandler.client.close()


    @staticmethod
    def serverListener():
        while ConnectionHandler.listening:
            rawdata = ConnectionHandler.client.recv(2048).decode()
            if not rawdata:
                print(f"ERROR: Data is {repr(rawdata)}. stopping...")
                break

            else:
                for data in rawdata.split(";?"):

                    d = data.split(":",1)
                    dtype = d.pop(0)
                    if len(d) > 0:
                        dt = d[0]
                    else:
                        dt=None

                    if dtype == networkConstants.players_pos:
                        DataCallbacks.players_pos(dt)

                    elif dtype == networkConstants.players_clear:
                        DataCallbacks.players_clear()





        print("ConnectionHandler:","serverListener stopped",f"({ConnectionHandler.listening})")