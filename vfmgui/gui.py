import pygame
import vfmflathub
import os
import vfmgui


class Image:
    LOGO = "/usr/share/pixmaps/vaporos-flatpak-manager.png"
    if not os.path.isfile(LOGO):
        LOGO = "data/vaporos-flatpak-manager.png"


class GamepadButton:
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


class Axis:
    LHOR = 0
    LVERT = 1
    RHOR = 4
    RVERT = 3


class gui:

    def __init__(self, application_name="VaporOS Flatpak Manager", screen_width=1920, screen_height=1080, fullscreen=False):
        self.application_name = application_name
        self.__screen_width = screen_width
        self.__screen_height = screen_height
        self.__fullscreen = fullscreen

        self.__grid_size = screen_width/32
        self.application_buttons = []
        self.application_list = []
        self.active_menu = None

        self.framerate = 30
        self.running = False

        self.__screen_button_limit = 9
        self.__screen_first_button = 0
        self.selected = 0

        self.input_wait = 0

    def run(self):
        self.running = True
        self.__setup_pygame()
        self.__setup_joysticks()
        self.__show_splash_screen()

        # Add Flathub to Flatpak and get the application list. This can take a while
        vfmflathub.add_flathub()

        # Get the application list
        self.application_list = vfmflathub.get_applications()
        self.installed_application_list = []
        # Remove installed applications from the available application list
        for application in self.application_list:
            if application.installed:
                self.installed_application_list.append(application)

        self.main_menu = vfmgui.MainMenu()
        self.list_available_menu = vfmgui.ListMenu(self.application_list)
        self.list_installed_menu = vfmgui.ListMenu(self.installed_application_list)
        self.active_menu = self.main_menu
        self.previous_menu = None

        self.__run()

    def __setup_pygame(self):
        pygame.init()
        if self.__fullscreen:
            self.__screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.__screen_width, self.__screen_height = self.__screen.get_size()
        else:
            self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_height), pygame.RESIZABLE)
        pygame.display.set_caption(self.application_name)
        self.__clock = pygame.time.Clock()

        self.__title_font = pygame.font.Font(vfmgui.Fonts.REGULAR, 64)

    def __setup_joysticks(self):
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for joystick in self.joysticks:
            joystick.init()

    def __show_splash_screen(self):
        self.__draw_background()
        # draw logo
        logo = pygame.image.load(Image.LOGO)
        logo_x = self.__screen_width / 2 - logo.get_width() / 2
        logo_y = self.__screen_height / 2 - logo.get_height() /2
        logo_rect = pygame.Rect(logo_x, logo_y, logo.get_width(), logo.get_height())
        self.__screen.blit(logo, logo_rect)

        # draw title
        self.__display_text_centered(self.application_name, self.__screen_width / 2, self.__screen_height - self.__grid_size,
                                     self.__grid_size, vfmgui.Colors.TEXT, vfmgui.Fonts.REGULAR)
        self.__update_screen()

    def __show_loading_screen(self, text):
        self.__draw_background()
        self.__display_text_centered(text, self.__screen_width / 2, self.__screen_height/2,
                                     self.__grid_size*2, vfmgui.Colors.TEXT, vfmgui.Fonts.REGULAR)
        self.__update_screen()

    def __run(self):
        while self.running:
            self.__read_input()
            self.__draw_background()
            self.__draw_gui()
            self.__update_screen()

    def __draw_background(self):
        self.__screen.fill(vfmgui.Colors.BACKGROUND)

    def __draw_gui(self):
        # Draw the currently used menu, this can change
        self.active_menu.draw(self.__screen)

        # Draw borders
        border_top = pygame.Rect(0, 0, self.__screen_width, 64)
        border_bottom = pygame.Rect(0, self.__screen_height - 64, self.__screen_width, self.__screen_height)
        pygame.draw.rect(self.__screen, vfmgui.Colors.BORDER, border_top)
        pygame.draw.rect(self.__screen, vfmgui.Colors.BORDER, border_bottom)

        # Draw title
        title = self.__title_font.render(self.application_name, True, vfmgui.Colors.TEXT_TITLE)
        title_rect = pygame.Rect(self.__screen_width/2-title.get_width()/2, -10, title.get_width(), title.get_height())
        self.__screen.blit(title, title_rect)

    def __read_input(self):
        # Handle analog stick and trigger input. It has to wait a little before responding to an input a second time
        for joystick in self.joysticks:
            axis_x = joystick.get_axis(0)
            axis_y = joystick.get_axis(1)
            axis_amount = joystick.get_numaxes()
            wait_time = 7
            if self.input_wait > 0:
                # wait a shorter amount of time if the analog stick is pushed further
                self.input_wait -= 1
            elif axis_y < -0.5:
                self.active_menu.event_button_up()
                self.input_wait = wait_time
            elif axis_y > 0.5:
                self.active_menu.event_button_down()
                self.input_wait = wait_time
            elif axis_x < -0.5:
                self.active_menu.event_button_left()
                self.input_wait = wait_time
            elif axis_x > 0.5:
                self.active_menu.event_button_right()
                self.input_wait = wait_time
            elif axis_amount > 4 and joystick.get_axis(2) > 0.8:
                self.active_menu.event_button_lt()
                self.input_wait = wait_time
            elif axis_amount > 4 and joystick.get_axis(5) > 0.8:
                self.active_menu.event_button_rt()
                self.input_wait = wait_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.JOYHATMOTION:
                if event.value == (0, 1):
                    self.active_menu.event_button_up()
                elif event.value == (0, -1):
                    self.active_menu.event_button_down()
                elif event.value == (-1, 0):
                    self.active_menu.event_button_left()
                elif event.value == (1, 0):
                    self.active_menu.event_button_right()
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == GamepadButton.A:
                    self.__event_button_a()
                elif event.button == GamepadButton.B:
                    self.__event_button_b()
                elif event.button == GamepadButton.X:
                    self.active_menu.event_button_x()
                elif event.button == GamepadButton.Y:
                    self.active_menu.event_button_y()
                elif event.button == GamepadButton.LB:
                    self.active_menu.event_button_lb()
                elif event.button == GamepadButton.RB:
                    self.active_menu.event_button_rb()
                elif event.button == GamepadButton.SEL:
                    self.running = False
                elif event.button == GamepadButton.START:
                    self.__event_button_a()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.__event_button_a()
                elif event.key == pygame.K_BACKSPACE:
                    self.__event_button_b()
                elif event.key == pygame.K_UP:
                    self.active_menu.event_button_up()
                elif event.key == pygame.K_DOWN:
                    self.active_menu.event_button_down()
                elif event.key == pygame.K_LEFT:
                    self.active_menu.event_button_left()
                elif event.key == pygame.K_RIGHT:
                    self.active_menu.event_button_right()
                elif event.key == pygame.K_PAGEUP:
                    self.active_menu.event_button_lt()
                elif event.key == pygame.K_PAGEDOWN:
                    self.active_menu.event_button_rt()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key in range( pygame.K_a, pygame.K_z + 1 ) and isinstance(self.active_menu, vfmgui.ListMenu):
                    self.active_menu.go_to_letter(pygame.key.name(event.key).upper())
            elif event.type == pygame.VIDEORESIZE:
                self.__screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
                self.__screen_width, self.__screen_height = event.dict['size']

    def __update_screen(self):
        pygame.display.update()
        self.__clock.tick(self.framerate)

    def __display_text_centered(self, text, x, y, size, text_color, font):
        font = pygame.font.Font(font, int(size))
        text_surface = font.render(text, True, text_color)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (x, y)
        self.__screen.blit(text_surface, text_rectangle)

    def __event_button_a(self):
        selection = self.active_menu.get_selected_button()
        if isinstance(self.active_menu, vfmgui.MainMenu):
            if selection == vfmgui.MainMenuButtons.available_applications:
                self.active_menu = self.list_available_menu
            elif selection == vfmgui.MainMenuButtons.installed_applications:
                self.active_menu = self.list_installed_menu
            elif selection == vfmgui.MainMenuButtons.exit:
                self.running = False
        elif isinstance(self.active_menu, vfmgui.ListMenu):
            application = self.active_menu.get_selected_application()
            if not application.busy:
                self.previous_menu = self.active_menu
                self.active_menu = vfmgui.ApplicationMenu(application)
        elif isinstance(self.active_menu, vfmgui.ApplicationMenu):
            if selection == vfmgui.ApplicationMenuButtons.back:
                self.__event_button_b()
            elif selection == vfmgui.ApplicationMenuButtons.install:
                application = self.active_menu.application
                application.install()
                self.installed_application_list.append(application)
                self.installed_application_list.sort()
                self.list_installed_menu.set_application_list(self.installed_application_list)
                self.__event_button_b()
            elif selection == vfmgui.ApplicationMenuButtons.uninstall:
                application = self.active_menu.application
                application.uninstall()
                self.installed_application_list.remove(application)
                self.list_installed_menu.set_application_list(self.installed_application_list)
                self.__event_button_b()

    def __event_button_b(self):
        if isinstance(self.active_menu, vfmgui.ApplicationMenu):
            self.active_menu = self.previous_menu
        elif isinstance(self.active_menu, vfmgui.ListMenu):
            self.active_menu = self.main_menu
        elif isinstance(self.active_menu, vfmgui.MainMenu):
            self.running = False

