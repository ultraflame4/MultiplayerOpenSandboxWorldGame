import pygame

from mog import EventsHandler
from mog import scenes

pygame.init()
pygame.key.set_repeat(600, 60)

EventsHandler.startEventListener()

scenes.SceneManager.switchToMainMenu()

scenes.SceneManager.mainloop()
