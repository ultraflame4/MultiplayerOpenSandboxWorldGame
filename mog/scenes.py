import pygame
from . import EventsHandler, game, network
from . import widgets

WINDOW_SIZE = (1600,900)


class baseScene(pygame.Surface):
    def __init__(self,window:pygame.Surface):
        pygame.Surface.__init__(self, WINDOW_SIZE)
        self.window = window
        self.isActive=False
        self.bg = (0,0,0)
        EventsHandler.SubscribeEvent.quit(self.killScene)


    def runScene(self):
        self.isActive=True
        self.updateLoop()


    def killScene(self,event):
        print(f"{self.__class__.__name__} : killing scene")
        self.isActive=False


    def clearSurface(self):
        self.fill(self.bg)

    def update(self):
        pass

    def _exit_protocol(self):
        """
        Called when loop stops
        """
        pass

    def _preLoop(self):
        pass

    def updateLoop(self):
        self._preLoop()
        while self.isActive:
            self.clearSurface()
            self.update()
            self.updateToWindow()

        self._exit_protocol()


    def updateToWindow(self):
        pygame.event.pump()
        self.window.blit(self,(0,0))
        pygame.display.flip()


class ServerMenu(baseScene):
    def __init__(self,window):
        baseScene.__init__(self,window)
        self.bg = (245,245,245)
        offset=200
        self.title = widgets.Text("Multiplayer Open Sandbox World Game",60,self,(0,90),centerHorizontal=True,bold=True)


        self.serveriptext = widgets.Text("Server Ip Address",50,self,(0,60+offset),centerHorizontal=True)

        self.serveriptextinput = widgets.TextInput(30,self,(0,150+offset),centerHorizontal=True,text="localhost")


        self.serverporttext = widgets.Text("Server Port", 50, self, (0, 210+offset), centerHorizontal=True)

        self.serverportinput = widgets.TextInput(30,self,(0,300+offset),centerHorizontal=True,text="8888")


        self.JoinButton = widgets.Button("Join",55,self,(0,700),centerHorizontal=True,clickedCallback=self.joincallback)


    def joincallback(self):
        network.ConnectionHandler.join_server(
            self.serveriptextinput.get_text(),
            int(self.serverportinput.get_text())
            )

        SceneManager.switchToGameScene()

    def update(self):
        self.title.drawText()
        self.serveriptext.drawText()
        self.serveriptextinput.drawText()
        self.serverporttext.drawText()
        self.serverportinput.drawText()
        self.JoinButton.drawToSurface()


class GameScene(baseScene):
    def __init__(self,window):
        baseScene.__init__(self,window)
        self.bg = (245,245,245)
        self.world = game.World(self)

    def _preLoop(self):
        self.world.init()

    def update(self):
        self.world.draw(self)



class SceneManager:
    window = pygame.display.set_mode(WINDOW_SIZE)
    mainmenu=ServerMenu(window)
    gamescene = GameScene(window)

    currentScene:baseScene = None

    run = True

    @staticmethod
    def _switchScene(scene:baseScene):
        print("SceneManager:",f"Switching to scene: {scene.__class__.__name__}")

        if SceneManager.currentScene is not None:
            SceneManager.currentScene.killScene(None)

        SceneManager.currentScene = scene



    @staticmethod
    def switchToMainMenu():
        SceneManager._switchScene(SceneManager.mainmenu)

    @staticmethod
    def switchToGameScene():
        SceneManager._switchScene(SceneManager.gamescene)





    @staticmethod
    def mainloop():
        while EventsHandler.SubscribeEvent.EventRun:

            SceneManager.currentScene.runScene()
