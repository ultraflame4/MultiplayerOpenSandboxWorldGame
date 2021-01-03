import inspect
import threading
import typing
from pprint import pprint

import pygame


EventCallbacks={
    pygame.QUIT:[],
    pygame.KEYDOWN:[],
    pygame.MOUSEBUTTONDOWN:[],
    }

physics_callbacks = []
keypressedcallbacks = []

# Event callback subscriptions decorators
class SubscribeEvent:
    EventRun = True
    ListenerThread:threading.Thread=None

    @staticmethod
    def quit(func:typing.Callable):

        def wrapped(*args,**kwargs):
            func(*args,**kwargs)



        EventCallbacks[pygame.QUIT].append(wrapped)
        return wrapped

    @staticmethod
    def keydown(func):
        def wrapped(*args,**kwargs):

            func(*args,**kwargs)


        EventCallbacks[pygame.KEYDOWN].append(wrapped)
        return wrapped

    @staticmethod
    def keypressed(func):
        keypressedcallbacks.append(func)
        return func

    @staticmethod
    def mousebuttondown(func):
        def wrapped(*args, **kwargs):
            func(*args, **kwargs)

        EventCallbacks[pygame.MOUSEBUTTONDOWN].append(wrapped)
        return wrapped


    @staticmethod
    def registerPhysicsCallback(func):
        physics_callbacks.append(func)
        return func

def dispatchEventsCallbacks(callbacks,event):
    for i in callbacks:
        i(event)



def EventListener():
    while SubscribeEvent.EventRun:

        for event in pygame.event.get():

            try:
                callbackList = EventCallbacks[event.type]
            except KeyError:
                pass
            else:

                dispatchEventsCallbacks(callbackList,event)

    print("EventListener Loop broken, EventRun:",SubscribeEvent.EventRun)

@SubscribeEvent.quit
def stopEventRun(event):
    print("Kill events")
    SubscribeEvent.EventRun=False


def startEventListener():
    physicsThread = threading.Thread(target=physicsLoop)
    physicsThread.start()
    SubscribeEvent.ListenerThread=threading.Thread(target=EventListener)
    SubscribeEvent.ListenerThread.start()



def physicsLoop():
    clock = pygame.time.Clock()

    while SubscribeEvent.EventRun:
        clock.tick(30)

        keys = pygame.key.get_pressed()

        for func in keypressedcallbacks:
            func(keys)

        for i in physics_callbacks:
            i()