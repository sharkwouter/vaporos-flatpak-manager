from vfmgui.menu import Menu
import vfmgui
import pygame


class ListMenu(Menu):
    def __init__(self, application_list):
        self.__screen_button_limit = 9
        self.__screen_first_button = 0
        self.selected = 0
        self.font = pygame.font.Font(vfmgui.Fonts.REGULAR, 64)

        self.application_buttons = []

        for application in application_list:
            button = vfmgui.ApplicationButton(application)
            self.application_buttons.append(button)

    def draw(self, screen):
        screen_width, screen_height = screen.get_size()

        if len(self.application_buttons) == 0:
            text = self.font.render("No applications found", True, vfmgui.Colors.TEXT_SUBTITLE)
            rect_text = pygame.Rect(screen_width / 2 - text.get_width() / 2, screen_height / 2 - text.get_height() / 2,
                                    text.get_width(), text.get_height())
            screen.blit(text, rect_text)
            return

        for index in range(self.__screen_first_button-3, self.__screen_first_button+self.__screen_button_limit+3):
            if index < 0 or index > len(self.application_buttons)-1:
                continue
            button_number = index-self.__screen_first_button
            selected = (index == self.selected)
            button = self.application_buttons[index]
            button_width = screen_width/3
            button_height = (screen_height-160)/3
            button_x = button_width*(button_number % 3)
            button_y = 80+button_height*round(button_number/3)
            button.draw(button_x, button_y, button_width, button_height, selected, screen)

    def get_selected_application(self):
        return self.application_buttons[self.selected].application

    def get_selected_button(self):
        self.get_selected_application()

    def set_application_list(self, application_list):
        self.application_buttons = []
        for application in application_list:
            button = vfmgui.ApplicationButton(application)
            self.application_buttons.append(button)

        # Make sure a button has been selected, even if the old one no longer exists
        if self.selected > len(self.application_buttons)-1:
            self.selected = len(self.application_buttons) - 1

    def __change_selected(self, x, y):
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

    def event_button_up(self):
        self.__change_selected(0, -1)

    def event_button_down(self):
        self.__change_selected(0, 1)

    def event_button_left(self):
        self.__change_selected(-1, 0)

    def event_button_right(self):
        self.__change_selected(1, 0)

    def event_button_lb(self):
        application = self.get_selected_application()
        letter = str(application)[0]
        letters_found = []
        for index in range(self.selected, -1, -1):
            if index == 0:
                self.selected = 0
                self.__screen_first_button = 0
            current_letter = str(self.application_buttons[index].application)[0]
            if current_letter == letter or current_letter in letters_found:
                continue
            if len(letters_found) == 0:
                letters_found.append(current_letter)
            else:
                self.selected = index+1
                if self.selected < 3:
                    self.__screen_first_button = 0
                else:
                    self.__screen_first_button = self.selected - ((index+1) % 3)
                break

    def event_button_rb(self):
        application = self.get_selected_application()
        letter = str(application)[0]
        for index in range(self.selected, len(self.application_buttons)):
            if index == len(self.application_buttons) - 1:
                break
            current_letter = str(self.application_buttons[index].application)[0]
            if current_letter != letter:
                self.selected = index
                if self.selected < 3:
                    self.__screen_first_button = 0
                else:
                    self.__screen_first_button = self.selected - (index % 3)
                break