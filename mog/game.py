import pygame

from mog import EventsHandler


class Player(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self,0,0,100,100)

        self.move_vel=9
        self.color=(0,0,0)

        self.velocity = [0,0]

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

    def addForce(self,x,y):
        self.velocity[0] += x
        self.velocity[1] += y


    def handle_movements(self,key):

        if key[pygame.K_w] and abs(self.velocity[1]) < self.move_vel:
            self.addForce(0,-self.move_vel*1)

        elif key[pygame.K_a] and abs(self.velocity[0]) < self.move_vel:
            self.addForce(-self.move_vel * 1, 0)

        elif key[pygame.K_s] and abs(self.velocity[1]) < self.move_vel:
            self.addForce(0, self.move_vel * 1)

        elif key[pygame.K_d] and abs(self.velocity[0]) < self.move_vel:
            self.addForce(self.move_vel * 1, 0)


    def draw(self,surface):
        pygame.draw.rect(surface,self.color,self)