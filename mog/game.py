import json

import pygame

from mog import EventsHandler, network, widgets


class WorldCamera:
    def __init__(self,surface:pygame.Surface):
        self.center = pygame.Vector2(surface.get_width()/2,surface.get_height()/2)
        self.pos = pygame.Vector2(0,0)
        self.scale=1.0


    def moveCamera(self,x,y):
        self.pos.x = x - self.center.x
        self.pos.y = y - self.center.y


    def caclRectDimension(self,rect):
        return rect.x-self.pos.x,rect.y-self.pos.y,rect.w,rect.h

    def caclRawRectDimension(self,x,y,w,h):
        return x - self.pos.x, y - self.pos.y, w, h

class Player(pygame.Rect):
    def __init__(self,scene,cam:WorldCamera):
        pygame.Rect.__init__(self,0,0,100,100)
        self.move_vel=9
        self.color=(0,0,0)
        self.scene = scene
        self.cam = cam

        self.velocity = [0,0]


    def init(self):
        EventsHandler.SubscribeEvent.keypressed(self.handle_movements)

        EventsHandler.SubscribeEvent.registerPhysicsCallback(self.velocity_move)


    def velocity_move(self):

        self.move_ip(*self.velocity)

        if self.velocity[0] > 0:
            self.velocity[0] -= 1
        elif self.velocity[0] < 0:
            self.velocity[0] += 1

        if self.velocity[1] > 0:
            self.velocity[1] -= 1
        elif self.velocity[1] < 0:
            self.velocity[1] += 1

        self.cam.moveCamera(self.centerx,self.centery)
        self.sendCoordsToServer()


    def sendCoordsToServer(self):
        network.ConnectionHandler.send(f"player/pos:{[self.x,self.y]}")


    def addForce(self,x,y):
            self.velocity[0] += x
            self.velocity[1] += y


    def handle_movements(self,key):
        if self.scene.isActive:
            if key[pygame.K_w] and abs(self.velocity[1]) < self.move_vel:
                self.addForce(0,-self.move_vel*1)

            elif key[pygame.K_a] and abs(self.velocity[0]) < self.move_vel:
                self.addForce(-self.move_vel * 1, 0)

            elif key[pygame.K_s] and abs(self.velocity[1]) < self.move_vel:
                self.addForce(0, self.move_vel * 1)

            elif key[pygame.K_d] and abs(self.velocity[0]) < self.move_vel:
                self.addForce(self.move_vel * 1, 0)

    def draw(self,surface):
        pygame.draw.rect(surface, self.color, self.cam.caclRectDimension(self))





class worldObject(pygame.Rect):
    def __init__(self,worldcamera,spawn_x,spawn_y,width,height,color=(100,100,100)):
        pygame.Rect.__init__(self,spawn_x,spawn_y,width,height)
        self.cam:WorldCamera = worldcamera
        self.color = color

    def draw(self,surface):
        pygame.draw.rect(surface, self.color, self.cam.caclRectDimension(self))

class World:
    def __init__(self,scene):
        self.coords_ui = widgets.Text("None",30,scene,(0,0))

        self.scene = scene
        self.camera = WorldCamera(scene)
        self.player = Player(scene,self.camera)
        self.otherPlayersPos=[]

        self.surface = scene


        network.DataCallbacks.players_pos=self.updateOtherPlayerPositions
        network.DataCallbacks.players_clear=self.otherPlayersPos.clear


    def updateOtherPlayerPositions(self,data):
        self.otherPlayersPos.clear()
        for k,v in json.loads(data.replace("'",'"')).items():
            self.otherPlayersPos.append(v)


    def drawUiCoords(self):
        self.coords_ui.text=self.coords_ui.font.render(
            f" x: {self.player.x}, y: {self.player.y}, vel:{self.player.velocity}", True, (0,0,0), None)
        self.coords_ui.drawText()

    def drawOtherPlayers(self):
        for coords in self.otherPlayersPos:
            pygame.draw.rect(self.surface,(0,0,0),self.camera.caclRawRectDimension(*coords,100,100))



    def init(self):
        self.player.init()

    def draw(self,surface):
        self.drawUiCoords()
        self.player.draw(surface)
        self.drawOtherPlayers()

