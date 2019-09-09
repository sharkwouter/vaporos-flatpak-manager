from vfmgui.menu import Menu
import vfmgui

class ApplicationMenuButtons:
    install = "Install"
    uninstall = "Uninstall"
    back = "back"

class ApplicationMenu(Menu):
    def __init__(self, application):
        self.selected = 0
        self.application = application

        self.buttons = []
        self.buttons.append(vfmgui.Button(ApplicationMenuButtons.install))
        self.buttons.append(vfmgui.Button(ApplicationMenuButtons.back))

    def draw(self, screen):
        screen_width, screen_height = screen.get_size()
        for index, button in enumerate(self.buttons):
            # Depending on the state of the application, change the install button to uninstall or the other way around
            if button.text == ApplicationMenuButtons.install and self.application.installed:
                button.text = ApplicationMenuButtons.uninstall
            if button.text == ApplicationMenuButtons.uninstall and not self.application.installed:
                button.text = ApplicationMenuButtons.install
            selected = (index == self.selected)
            button_width = screen_width/3
            button_height = (screen_height-160)/7
            button_x = screen_width/2-button_width/2
            button_y = 80+button_height*2+button_height*index
            button.draw(button_x, button_y, button_width, button_height, selected, screen)

    def get_selected_button(self):
        return self.buttons[self.selected].text

    def __change_selected(self, x):
        selected_before = self.selected
        self.selected += x

        # Make sure the selection is within bounds
        if self.selected > len(self.buttons)-1:
            self.selected = selected_before

        if self.selected < 0:
            self.selected = selected_before

    def event_button_up(self):
        self.__change_selected(-1)

    def event_button_down(self):
        self.__change_selected(1)

    def event_button_left(self):
        return

    def event_button_right(self):
        return
