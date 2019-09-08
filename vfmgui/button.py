import pygame
import vfmgui


class Button:
    def __init__(self, text, width, height, action):
        self.text = " {} ".format(text)
        self.width = width
        self.height = height
        self.action = action
        self.selected = False

    def draw(self, x, y, screen):
        if self.selected:
            button_color = vfmgui.Colors.BUTTON_SELECTED
            text_color = vfmgui.Colors.BUTTON_TEXT_SELECTED
        else:
            button_color = vfmgui.Colors.BUTTON
            text_color = vfmgui.Colors.BUTTON_TEXT

        rectangle = pygame.Rect(x, y, self.width, self.height)
        #pygame.draw.rect(screen, button_color, rectangle)

        font = pygame.font.Font(vfmgui.Fonts.REGULAR, self.height)
        text = font.render(self.text, True, text_color, button_color)
        screen.blit(text, rectangle)



