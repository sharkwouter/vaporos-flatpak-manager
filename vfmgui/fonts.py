import pygame


pygame.font.init()


class Fonts:
    __font = pygame.font.match_font('liberationsansnarrow')
    print(__font)
    REGULAR = pygame.font.Font(__font, 64)
    SMALL = pygame.font.Font(__font, 32)
    LARGE = pygame.font.Font(__font, 96)
