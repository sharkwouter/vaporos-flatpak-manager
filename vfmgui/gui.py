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
        self.__fullscreen = fullscreen

        self.__grid_size = screen_width/32
        self.application_buttons = []

        self.framerate = 30
        self.running = False

        self.__screen_button_limit = 9
        self.__screen_first_button = 0
        self.selected = 0

    def run(self):
        self.running = True
        self.__setup_pygame()
        self.__setup_joysticks()
        self.__show_splash_screen()

        # Add Flathub to Flatpak and get the application list. This can take a while
        vfmflathub.add_flathub()
        for application in vfmflathub.get_applications():
            button = vfmgui.ApplicationButton(application)
            self.application_buttons.append(button)

        self.__run()

    def __setup_pygame(self):
        pygame.init()
        if self.__fullscreen:
            self.__screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        else:
            self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_height))
        pygame.display.set_caption(self.application_name)
        self.__clock = pygame.time.Clock()

        self.__title_font = pygame.font.Font(vfmgui.Fonts.REGULAR, 64)

    def __setup_joysticks(self):
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for joystick in joysticks:
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
        # Draw the buttons for the applications
        for index in range(self.__screen_first_button-3, self.__screen_first_button+self.__screen_button_limit+3):
            if index < 0 or index > len(self.application_buttons)-1:
                continue
            button_number = index-self.__screen_first_button
            selected = (index == self.selected)
            button = self.application_buttons[index]
            button_width = self.__screen_width/3
            button_height = (self.__screen_height-160)/3
            button_x = button_width*(button_number % 3)
            button_y = 80+button_height*round(button_number/3)
            button.draw(button_x, button_y, button_width, button_height, selected, self.__screen)

        # Draw borders
        border_top = pygame.Rect(0, 0, self.__screen_width, 64)
        border_bottom = pygame.Rect(0, self.__screen_height - 64, self.__screen_width, self.__screen_height)
        pygame.draw.rect(self.__screen, vfmgui.Colors.BACKGROUND, border_top)
        pygame.draw.rect(self.__screen, vfmgui.Colors.BACKGROUND, border_bottom)

        # Draw title
        title = self.__title_font.render(self.application_name, True, vfmgui.Colors.TEXT_TITLE)
        title_rect = pygame.Rect(self.__screen_width/2-title.get_width()/2, -10, title.get_width(), title.get_height())
        self.__screen.blit(title, title_rect)

        # Draw bottom text
        bottom_text = self.__title_font.render("A - install  X - uninstall   START - exit", True, vfmgui.Colors.TEXT_TITLE)
        bottom_text_rect = pygame.Rect(self.__screen_width / 2 - bottom_text.get_width() / 2, self.__screen_height-bottom_text.get_height(), bottom_text.get_width(), bottom_text.get_height())
        self.__screen.blit(bottom_text, bottom_text_rect)

    def __read_input(self):
        application = self.get_selected_application()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.JOYHATMOTION:
                if event.value == (0, 1):
                    self.change_selected(0, -1)
                elif event.value == (0, -1):
                    self.change_selected(0, 1)
                elif event.value == (-1, 0):
                    self.change_selected(-1, 0)
                elif event.value == (1, 0):
                    self.change_selected(1, 0)
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == 1 and event.value < -0.5:
                    self.change_selected(0, -1)
                elif event.axis == 1 and event.value > 0.5:
                    self.change_selected(0, 1)
                elif event.axis == 0 and event.value < -0.5:
                    self.change_selected(-1, 0)
                elif event.axis == 0 and event.value > 0.5:
                    self.change_selected(1, 0)
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == GamepadButton.A and not application.installed:
                    self.__show_loading_screen("Installing...")
                    vfmflathub.install(application)
                elif event.button == GamepadButton.X and application.installed:
                    self.__show_loading_screen("Uninstalling...")
                    vfmflathub.uninstall(application)
                elif event.button == GamepadButton.LB:
                    self.change_selected(0, -3)
                elif event.button == GamepadButton.RB:
                    self.change_selected(0, 3)
                elif event.button == GamepadButton.SEL or event.button == GamepadButton.START:
                    self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not application.installed:
                    self.__show_loading_screen("Installing...")
                    vfmflathub.install(application)
                elif event.key == pygame.K_BACKSPACE and application.installed:
                    self.__show_loading_screen("Uninstalling...")
                    vfmflathub.uninstall(application)
                elif event.key == pygame.K_UP:
                    self.change_selected(0, -1)
                elif event.key == pygame.K_DOWN:
                    self.change_selected(0, 1)
                elif event.key == pygame.K_LEFT:
                    self.change_selected(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.change_selected(1, 0)
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

    def __update_screen(self):
        pygame.display.update()
        self.__clock.tick(self.framerate)

    def __display_text_centered(self, text, x, y, size, text_color, font):
        font = pygame.font.Font(font, size)
        text_surface = font.render(text, True, text_color)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (x, y)
        self.__screen.blit(text_surface, text_rectangle)

    def __display_text(self, text, x, y, size, text_color, font):
        font = pygame.font.Font(font, size)
        text_surface = font.render(text, True, text_color)
        rect = pygame.Rect(x, y, self.__screen_width-self.__grid_size*3-x, size)
        self.__screen.blit(text_surface, rect)

    def change_selected(self, x, y):
        selected_before = self.selected
        position_x = self.selected % 3
        if position_x + x in range(0, 3):
            self.selected += x
        if y != 0:
            self.selected += y * 3

        # Make sure the selection is within bounds
        if self.selected > len(self.application_buttons)-1:
            self.selected = selected_before

        if self.selected < 0:
            self.selected = selected_before

        # Move the screen down or up if needed
        while self.selected not in range(self.__screen_first_button, self.__screen_first_button+self.__screen_button_limit):
            if self.selected < self.__screen_first_button:
                self.__screen_first_button -= 3
            if self.selected > self.__screen_first_button + self.__screen_button_limit-1:
                self.__screen_first_button += 3

    def get_selected_application(self):
        if self.selected > len(self.application_buttons)-1:
            return None
        return self.application_buttons[self.selected].application
