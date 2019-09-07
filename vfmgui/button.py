import pygame
import vfmgui


class Button:
    def __init__(self, text, width, height, action):
        self.text = text
        self.width = width
        self.height = height
        self.action = action
        self.selected = False

    def draw(self, x, y, screen):
        if self.selected:
            button_color = vfmgui.Colors.BUTTON_SELECTED
        else:
            button_color = vfmgui.Colors.BUTTON

        rectangle = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(screen, button_color, rectangle)



