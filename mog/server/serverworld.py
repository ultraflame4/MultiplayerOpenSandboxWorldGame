import ast
import typing
import threading
import time


def invoke(func,delay=0):
    time.sleep(delay)
    threading.Thread(target=func).start()

class Player:
    def __init__(self,client):
        self.client=client
        self.pos = [0,0]
        self.client.player_pos_cb = self.updatePos

    def updatePos(self,xy):
        x,y = ast.literal_eval(xy)
        self.pos[0]=x
        self.pos[1]=y



    def sendOtherPlayerPos(self,pos_dict):
        del pos_dict[str(self.client.id)]
        if len(pos_dict) > 0:
            self.client.send(f'players/pos:{pos_dict}')



class World:
    def __init__(self):
        self.players:typing.Dict[int,Player]={}

        self.updateLoopThread = threading.Thread(target=self.WorldUpdateLoop)
        self.updateLoopThread.start()

    def addPlayer(self,client):
        self.players[client.id] = Player(client)


    def removePlayer(self,client):
        print("removing player ( Client:",client.id,")")
        del self.players[client.id]
        for p in self.players.values():
            p.client.send("players/clear")

    def sendPosToAllPlayers(self):
        all_pos = {str(k):v.pos for k,v in self.players.items()}
        for v in self.players.values():
            v.sendOtherPlayerPos(all_pos.copy())

    def WorldUpdateLoop(self):
        while True:
            start = time.time()
            invoke(self.sendPosToAllPlayers)

            time.sleep(max(1. / 60 - (time.time() - start), 0))

class Manager:
    world = World()
