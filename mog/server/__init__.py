import socket

from mog.server import clientManager

server="localhost"
port=8888
serverip = socket.gethostbyname(server)


def addClient(conn,addr):
    clientManager.ClientsInfo.connected_clients.append(
        clientManager.PseudoClient(
            conn,addr,
            clientManager.ClientsInfo.idCount
            )
        )

    clientManager.ClientsInfo.idCount+=1


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