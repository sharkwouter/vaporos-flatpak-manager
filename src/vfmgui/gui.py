import pygame
import vfmflatpak


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

        self.background_color = Color.BLUE
        self.title_color = Color.BLACK
        self.text_color = Color.GREEN
        self.selection_color = Color.WHITE

        self.default_font = Font.REGULAR
        self.title_font = Font.BOLD

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
        self.__display_text(self.application_name, self.__screen_width/2, self.__screen_height/2, self.__grid_size*2, self.title_color, self.title_font)
        self.__update_screen()

    def __show_loading_screen(self, text):
        self.__draw_background()
        self.__display_text(text, self.__screen_width/2, self.__screen_height/2, self.__grid_size*2, self.title_color, self.title_font)
        self.__update_screen()

    def __run(self):
        while self.running:
            self.__read_input()
            self.__draw_background()
            self.__draw_gui()
            self.__update_screen()

    def __draw_background(self):
        self.__screen.fill(Color.BLUE)

    def __draw_gui(self):
        page_offset = (self.page-1)*self.__page_size
        for index in range(0, self.__page_size):
            if index+page_offset >= len(self.application_list):
                return
            font = Font.REGULAR
            if index == self.selected:
                font = Font.BOLD

            color=Color.GREEN
            if self.application_list[index+page_offset].installed:
                color=Color.WHITE

            if page_offset+index < len(self.application_list):
                self.__display_text(str(self.application_list[index+page_offset]), self.__screen_width/2, self.__grid_size*2+self.__grid_size*3*index, self.__grid_size, color, font)

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
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == Button.A and not application.installed:
                    self.__show_loading_screen("Installing...")
                    application.install()
                elif event.button == Button.X and application.installed:
                    self.__show_loading_screen("Uninstalling...")
                    application.uninstall()
                elif event.button == Button.LB:
                    self.change_page(-1)
                elif event.button == Button.RB:
                    self.change_page(1)
                elif event.button == Button.SEL:
                    self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not application.installed:
                    self.__show_loading_screen("Installing...")
                    application.install()
                elif event.key == pygame.K_BACKSPACE and application.installed:
                    self.__show_loading_screen("Uninstalling...")
                    application.uninstall()
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

    def __display_text(self, text, x, y, size, text_color, font):
        font = pygame.font.Font(font, size)
        text_surface = font.render(text, True, text_color)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (x, y)
        self.__screen.blit(text_surface, text_rectangle)

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
