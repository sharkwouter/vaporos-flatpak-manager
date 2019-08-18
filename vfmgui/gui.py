import pygame
import vfmflatpak
import os


class Color():
    BACKGROUND = 19, 139, 67
    BUTTON = 20, 167, 92
    BUTTON_SELECTED = 108, 196, 154
    BUTTON_BORDER = 0, 0, 0
    BUTTON_BORDER_SELECTED = 185, 185 ,185
    TEXT_TITLE = 255, 255, 255
    TEXT = 0, 0, 0


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
    REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
    if not os.path.isfile(REGULAR):
        font_regular = "fonts/DejaVuSansMono.ttf"
    if not os.path.isfile(BOLD):
        font_bold = "fonts/DejaVuSansMono-Bold.ttf"


class gui:

    def __init__(self, application_name="VaporOS Flatpak Manager", screen_width=1280, screen_height=720, fullscreen=False, page_size=5):
        self.application_name = application_name
        self.__screen_width = screen_width
        self.__screen_height = screen_height
        self.__fullscreen = fullscreen
        self.__page_size = page_size
        self.__fullscreen = fullscreen

        self.__grid_size = screen_width/32
        self.application_list = []

        self.framerate = 30
        self.running = False

        self.page = 1
        self.selected = 0

    def run(self):
        self.running = True
        self.__setup_pygame()
        self.__setup_joysticks()
        self.__show_splash_screen()

        # This can take a while
        self.__flatpak_manager = vfmflatpak.manager()
        self.application_list = self.__flatpak_manager.get_application_list()

        self.__run()

    def __setup_pygame(self):
        pygame.init()
        if self.__fullscreen:
            self.__screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        else:
            self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_height))
        pygame.display.set_caption(self.application_name)
        self.__clock = pygame.time.Clock()

    def __setup_joysticks(self):
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for joystick in joysticks:
            joystick.init()

    def __show_splash_screen(self):
        self.__draw_background()
        self.__display_text_centered(self.application_name, self.__screen_width/2, self.__screen_height/2, self.__grid_size*2, Color.TEXT_TITLE, Font.BOLD)
        self.__update_screen()

    def __show_loading_screen(self, text):
        self.__draw_background()
        self.__display_text_centered(text, self.__screen_width/2, self.__screen_height/2, self.__grid_size*2, Color.TEXT_TITLE, Font.BOLD)
        self.__update_screen()

    def __run(self):
        while self.running:
            self.__read_input()
            self.__draw_background()
            self.__draw_gui()
            self.__update_screen()

    def __draw_background(self):
        self.__screen.fill(Color.BACKGROUND)

    def __draw_gui(self):
        # Draw title
        self.__display_text_centered(self.application_name, self.__screen_width/2, self.__grid_size*0.75, self.__grid_size, Color.TEXT_TITLE, Font.BOLD)

        # Draw the buttons for the applications
        page_offset = (self.page-1)*self.__page_size
        for index in range(0, self.__page_size):
            if index+page_offset >= len(self.application_list):
                return

            selected = (index == self.selected)
            if page_offset+index < len(self.application_list):
                self.__draw__application_button(self.application_list[index+page_offset], index, selected)

        # Draw bottom text
        bottom_text = "A - install  X - uninstall   START - exit"
        self.__display_text_centered(bottom_text, self.__screen_width/2, self.__screen_height-self.__grid_size*0.75, self.__grid_size, Color.TEXT_TITLE, Font.REGULAR)


    def __read_input(self):
        application = self.get_selected_application()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.JOYHATMOTION:
                if event.value == (0, 1):
                    self.selected -= 1
                elif event.value == (0, -1):
                    self.selected += 1
                elif event.value == (-1, 0):
                    self.change_page(-1)
                elif event.value == (1, 0):
                    self.change_page(1)
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == 1 and event.value < -0.5:
                    self.selected -= 1
                elif event.axis == 1 and event.value > 0.5:
                    self.selected += 1
                elif event.axis == 0 and event.value < -0.5:
                    self.change_page(-1)
                elif event.axis == 0 and event.value > 0.5:
                    self.change_page(1)
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == Button.A and not application.installed:
                    self.__show_loading_screen("Installing...")
                    self.__flatpak_manager.install(application)
                elif event.button == Button.X and application.installed:
                    self.__show_loading_screen("Uninstalling...")
                    self.__flatpak_manager.uninstall(application)
                elif event.button == Button.LB:
                    self.change_page(-1)
                elif event.button == Button.RB:
                    self.change_page(1)
                elif event.button == Button.SEL or event.button == Button.START:
                    self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not application.installed:
                    self.__show_loading_screen("Installing...")
                    self.__flatpak_manager.install(application)
                elif event.key == pygame.K_BACKSPACE and application.installed:
                    self.__show_loading_screen("Uninstalling...")
                    self.__flatpak_manager.uninstall(application)
                elif event.key == pygame.K_UP:
                    self.selected -= 1
                elif event.key == pygame.K_DOWN:
                    self.selected += 1
                elif event.key == pygame.K_LEFT:
                    self.change_page(-1)
                elif event.key == pygame.K_RIGHT:
                    self.change_page(1)
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

        if self.selected < 0:
            self.selected = 0
            self.change_page(-1, self.__page_size-1)
        elif self.selected > self.__page_size-1:
            self.selected = 4
            self.change_page(1, 0)

    def __update_screen(self):
        pygame.display.update()
        self.__clock.tick(self.framerate)

    def __display_text_centered(self, text, x, y, size, text_color=Color.TEXT, font=Font.REGULAR):
        font = pygame.font.Font(font, size)
        text_surface = font.render(text, True, text_color)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (x, y)
        self.__screen.blit(text_surface, text_rectangle)

    def __display_text(self, text, x, y, size, text_color=Color.TEXT, font=Font.REGULAR):
        font = pygame.font.Font(font, size)
        text_surface = font.render(text, True, text_color)
        rect = pygame.Rect(x, y, self.__screen_width-self.__grid_size*3-x, size)
        self.__screen.blit(text_surface, rect)

    def __draw__application_button(self, application, index, selected):
        if selected:
            button_color = Color.BUTTON_SELECTED
            button_border_color = Color.BUTTON_BORDER_SELECTED
            font = Font.BOLD
        else:
            button_color = Color.BUTTON
            button_border_color = Color.BUTTON_BORDER
            font = Font.REGULAR

        # draw the rectangle
        rect_x = self.__grid_size*3
        rect_y = self.__grid_size*1.5+self.__grid_size*3*index+1
        rect_width = self.__screen_width-self.__grid_size*6
        rect_height = self.__grid_size*3-2
        pygame.draw.rect(self.__screen, button_color, pygame.Rect(rect_x, rect_y, rect_width, rect_height))

        pygame.draw.line(self.__screen, button_border_color, (rect_x, rect_y), (rect_x+rect_width, rect_y), 1)
        pygame.draw.line(self.__screen, button_border_color, (rect_x, rect_y+rect_height), (rect_x+rect_width, rect_y+rect_height), 1)
        pygame.draw.line(self.__screen, button_border_color, (rect_x, rect_y), (rect_x, rect_y+rect_height), 1)
        pygame.draw.line(self.__screen, button_border_color, (rect_x+rect_width, rect_y), (rect_x+rect_width, rect_y+rect_height), 1)

        self.__display_text(str(application), rect_x+self.__grid_size*0.5, rect_y, self.__grid_size, Color.TEXT_TITLE, Font.REGULAR)
        description_short = application.description
        if len(description_short) >= 80:
            description_short = "{}...".format(description_short[:79])
        self.__display_text(description_short, rect_x+self.__grid_size*0.5, rect_y+self.__grid_size*2, self.__grid_size/2, Color.TEXT_TITLE, Font.REGULAR)
        if application.installed:
            self.__display_text("Installed", rect_x+rect_width-self.__grid_size*5, rect_y+self.__grid_size*0.5, self.__grid_size/2, Color.TEXT_TITLE, Font.REGULAR)



    def change_page(self, change, selected=None):
        if (self.page + change) < 1 or (self.page + change) > len(self.application_list)/self.__page_size:
            return
        if selected is not None:
            self.selected = selected
        self.page += change

    def get_selected_application(self):
        index = (self.page-1)*self.__page_size+self.selected
        if index >= len(self.application_list):
            return None
        return self.application_list[(self.page-1)*self.__page_size+self.selected]
