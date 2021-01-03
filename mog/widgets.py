import os.path
import pygame
import pygame.locals as pl

from . import EventsHandler

pygame.font.init()


class Text:
    def __init__(self, text, font_size, surface:pygame.Surface, xy, bold=False, italic=False, color=(20, 20, 25), bg=None,
                 centerHorizontal=False, xyCenter=False):
        """
        :param text: The Text
        :param font_size: The txt_string size
        :param surface: The surface to draw txt_string on
        :param xy: position of txt_string
        :param bold: Bold
        :param italic: Italic
        :param color: Color of txt_string
        :param bg: Background color of txt_string
        :param centerHorizontal: To draw the txt_string on the center of the x axis

        Note. This will overwrite the given x coordinates

        :param xyCenter: When True, the given xy coords would determine where the center of the txt_string is
        """

        self.font = pygame.font.SysFont("Courier", font_size, bold, italic)
        self.text = self.font.render(text, True, color, bg)

        self.rect = self.text.get_rect()
        self.target_surface = surface

        #Calculate pos
        if centerHorizontal:
            self.xy=(int((surface.get_width()/2)-(self.rect.width/2)),xy[1])

        else:
            if xyCenter:
                self.xy=(
                    xy[0] + self.rect.width / 2,
                    xy[1] + self.rect.height / 2
                )
            else:
                self.xy = xy

    def drawText(self):
        self.target_surface.blit(self.text, self.xy)


class TextInput(Text):
    def __init__(self, font_size, surface: pygame.Surface, xy, text='',
                 max_chars=40,
                 bold=False, italic=False, color=(20, 20, 25),
                 bg=(255,255,255),
                 centerHorizontal=False, xyCenter=False):

        Text.__init__(self,'',font_size,surface,xy,bold,italic,color,None,centerHorizontal,xyCenter)
        EventsHandler.SubscribeEvent.keydown(self.handle_keystrokes)
        EventsHandler.SubscribeEvent.mousebuttondown(self.checkSelected)


        self.txt_string = text
        self.active=False
        self.color = color
        self.bg = pygame.Color(*bg)
        self.max_char = max_chars

        self.rxy = xy
        self.centerHorizontal = centerHorizontal
        self.xyCenter=xyCenter

        self.minWidth = 500


        self.txtBox_Rectangle = pygame.rect.Rect(self.xy[0] - self.minWidth * .5, self.xy[1], self.minWidth, self.rect.height)

        self.text = self.font.render(self.txt_string, True, self.color, None)
        self.recalculatePosition()


    def handle_keystrokes(self,event):
        if self.active:
            if event.key == pygame.K_RETURN:
                self.active=False
            elif event.key == pygame.K_BACKSPACE:
                self.txt_string = self.txt_string[:-1]

            elif len(self.txt_string) < self.max_char:
                self.txt_string += event.unicode

            self.text = self.font.render(self.txt_string, True, self.color, None)
            self.recalculatePosition()


    def drawHover(self):
        if self.txtBox_Rectangle.collidepoint(*pygame.mouse.get_pos()):
            pygame.draw.rect(self.target_surface,
                             self.bg.lerp(pygame.Color(200,200,200),.3),
                             self.txtBox_Rectangle)

    def checkSelected(self,event):
        if self.txtBox_Rectangle.collidepoint(*pygame.mouse.get_pos()):
            self.active=True
        else:
            self.active=False

    def get_text(self):
        return self.txt_string

    def recalculatePosition(self):
        self.rect = self.text.get_rect()
        if self.centerHorizontal:
            self.xy=(int((self.target_surface.get_width()/2)-(self.rect.width/2)),self.rxy[1])

        else:
            if self.xyCenter:
                self.xy=(
                    self.rxy[0] + self.rect.width / 2,
                    self.rxy[1] + self.rect.height / 2
                )
            else:
                self.xy = self.rxy
        if self.rect.width > self.minWidth:
            self.txtBox_Rectangle.x, self.txtBox_Rectangle.y = self.xy


    def drawText(self):
        pygame.draw.rect(self.target_surface, self.bg, self.txtBox_Rectangle)
        self.drawHover()
        Text.drawText(self)

class Button(Text):
    def __init__(self, text, font_size, surface:pygame.Surface, xy,
                 clickedCallback=None, bold=False, italic=False, txtcolor=(20, 20, 25),
                 centerHorizontal=False, xyCenter=False):
        Text.__init__(self,text,font_size,surface,xy,bold,italic,txtcolor,None,centerHorizontal,xyCenter)

        x,y,w,h = self.text.get_rect()

        addSize=30
        xAddSize=40
        self.button_rect = pygame.rect.Rect(self.xy[0]-(addSize+xAddSize)/2,self.xy[1]-addSize/2,
                                            w+addSize+xAddSize,h+addSize)
        self.callback = clickedCallback
        self.bg = pygame.Color(255,255,255)
        EventsHandler.SubscribeEvent.mousebuttondown(self.checkClicked)

    def drawHover(self):
        if self.button_rect.collidepoint(*pygame.mouse.get_pos()):
            pygame.draw.rect(self.target_surface,
                             self.bg.lerp(pygame.Color(100,200,90),.2),
                             self.button_rect)

    def checkClicked(self,event):
        if self.button_rect.collidepoint(*pygame.mouse.get_pos()):
            if self.callback is not None:
                self.callback()


    def drawToSurface(self):
        pygame.draw.rect(self.target_surface,self.bg,self.button_rect)
        self.drawHover()
        self.drawText()
