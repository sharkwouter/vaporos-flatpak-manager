import pygame


pygame.font.init()


class Fonts:
    _font = pygame.font.match_font('liberationsansnarrow')
    print(_font)
    REGULAR = pygame.font.Font(_font, 64)
    SMALL = pygame.font.Font(_font, 32)
    LARGE = pygame.font.Font(_font, 96)
