import threading
import socket


class ConnectionHandler:
    serverip = None
    serverport = 8888
    listenerThread = None
    listening = False
    client:socket.socket=None

    @staticmethod
    def join_server(serverip,serverport=8888):
        ConnectionHandler.serverip = serverip
        ConnectionHandler.serverport=serverport

        ConnectionHandler.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ConnectionHandler.client.connect((serverip,serverport))


        ConnectionHandler.listenerThread=threading.Thread(target=ConnectionHandler.serverListener)
        ConnectionHandler.listening = True
        ConnectionHandler.listenerThread.start()


    @staticmethod
    def serverListener():
        while ConnectionHandler.listening:
            data = ConnectionHandler.client.recv(2048).decode()
            if not data:
                print(f"ERROR: Data is {repr(data)}. stopping...")
                break

            else:
                print(data)

        print("ConnectionHandler:","serverListener stopped",f"({ConnectionHandler.listening})")