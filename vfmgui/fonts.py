import pygame
import os


class Fonts:
    REGULAR = pygame.font.match_font('liberationsansnarrow')
    print(os.path.exists(REGULAR))
