import pygame
import subprocess
import os
import pyflatpak

class Color():
    RED = 255, 0, 0
    BLUE = 0, 0, 255
    GREEN = 0,255,0
    BLACK = 0, 0, 0
    WHITE = 255, 255 ,255


class GameState():
    MENU = 1


class Button():
    A = 0
    B = 1
    X = 2
    Y = 3
    LB = 4
    RB = 5
    SEL = 6
    START = 7
    HOME = 8
    LTHUMB = 9
    RTHUMB = 10


class Axis():
    LHOR = 0
    LVERT = 1
    RHOR = 4
    RVERT = 3

class Font():
    REGULAR = "../fonts/DejaVuSansMono.ttf"
    BOLD = "../fonts/DejaVuSansMono-Bold.ttf"

flatpak_manager = pyflatpak.manager()
application_list = flatpak_manager.get_application_list()

def display_text( text, x, y, size, text_color=Color.GREEN, font=Font.REGULAR):
    font = pygame.font.Font(font, size)
    text_surface = font.render(text, True, text_color)
    text_rectangle = text_surface.get_rect()
    text_rectangle.center = (x, y)
    screen.blit(text_surface, text_rectangle)

def draw_application_buttons(page, selected, grid_size):
    page_offset = page*5
    for index in range(0, 5):
        font = Font.REGULAR
        if index-page_offset == selected:
            font = Font.BOLD

        if page_offset+index < len(application_list):
            display_text(str(application_list[index+page_offset]), screen_width/2, grid_size*2+grid_size*3*index, grid_size, font=font)

def draw_loading_screen(screen, screen_width, screen_height, grid_size):
    screen.fill(Color.BLUE)
    display_text("VaporOS Flatpak Manager", screen_width/2, screen_height/2, grid_size*2, font=Font.BOLD)
    pygame.display.update()

# Setup pygame
pygame.init()

# Setup gamepads/joysticks
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
for joystick in joysticks:
    joystick.init()
    print("Axes: {}".format(joystick.get_numaxes()))

# Setup screen
#screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
grid_size = screen_width/32


# Timer to be able to lock fps
clock = pygame.time.Clock()

page = 0
selected = 1

draw_loading_screen(screen, screen_width, screen_height, grid_size)

# Main loop
running = True
while running:
    # Background has to go first
    screen.fill(Color.BLUE)

    # Check for input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.JOYBUTTONDOWN:
            print(event.button)
            if event.button == Button.A:
                running = False
            elif event.button == Button.LB:
                page -= 1
                display_text("Loading", screen_width/2, screen_height/2, grid_size, font=Font.REGULAR)
                pygame.display.update()
                print("page: {}".format(page))
            elif event.button == Button.RB:
                page += 1
                display_text("Loading", screen_width/2, screen_height/2, grid_size, font=Font.REGULAR)
                pygame.display.update()
                print("page: {}".format(page))
            elif event.button == Button.SEL:
                running = False
        elif event.type == pygame.JOYHATMOTION:
            if event.value == (0, 1):
                selected -= 1
            elif event.value == (0, -1):
                selected += 1


    if selected < 0:
        selected = 4
    elif selected > 4:
        selected = 0

    draw_application_buttons(page, selected, grid_size)

    # Draw grid, for testing purposes
    for y in range(0, screen_height, grid_size):
        pygame.draw.line(screen, Color.BLACK, (0, y), (screen_width, y), 1)

    for x in range(0, screen_width, grid_size):
        pygame.draw.line(screen, Color.BLACK, (x, 0), (x, screen_height), 1)

    # Update display
    pygame.display.update()
    clock.tick(30)
