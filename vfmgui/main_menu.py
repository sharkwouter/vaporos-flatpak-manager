from vfmgui.menu import Menu
import vfmgui
import vfmflathub


class MainMenuButtons:
    available_applications = "Available Applications"
    installed_applications = "Installed Applications"
    update_all = "Update All"
    exit = "Exit"


class MainMenu(Menu):
    def __init__(self, title):
        self.__screen_button_limit = 4
        self.__screen_first_button = 0
        self.selected = 0
        self.title = title
        self.updating = False
        self.update_process = None

        self.buttons = []
        self.buttons.append(vfmgui.Button(MainMenuButtons.available_applications))
        self.buttons.append(vfmgui.Button(MainMenuButtons.installed_applications))
        self.buttons.append(vfmgui.Button(MainMenuButtons.update_all))
        self.buttons.append(vfmgui.Button(MainMenuButtons.exit))

    def draw(self, screen):
        screen_width, screen_height = screen.get_size()
        for index in range(self.__screen_first_button-3, self.__screen_first_button+self.__screen_button_limit+3):
            if index < 0 or index > len(self.buttons)-1:
                continue
            button_number = index-self.__screen_first_button
            selected = (index == self.selected)
            button = self.buttons[index]
            button_width = screen_width/3
            button_height = (screen_height-160)/7
            button_x = screen_width/2-button_width/2
            button_y = 80+button_height*2+button_height*button_number

            # Show that we're updating
            if button.text == vfmgui.MainMenuButtons.update_all and self.updating:
                self.__update_progress(button)

            # Draw button
            button.draw(button_x, button_y, button_width, button_height, selected, screen)

    def update_all(self):
        if not self.updating:
            self.updating = True
            self.update_process = vfmflathub.update_all()

    def __update_progress(self, button):
        if self.update_process is not None and self.update_process.poll() is None:
            button.add_progress()
        else:
            button.progress = -1
            button.done = True
            if self.update_process.poll() == 0:
                button.failed = False
            else:
                button.failed = True
                self.updating = False

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

        # Move the screen down or up if needed
        while self.selected not in range(self.__screen_first_button, self.__screen_first_button+self.__screen_button_limit):
            if self.selected < self.__screen_first_button:
                self.__screen_first_button -= 1
            if self.selected > self.__screen_first_button + self.__screen_button_limit-1:
                self.__screen_first_button += 1

    def event_button_up(self):
        self.__change_selected(-1)

    def event_button_down(self):
        self.__change_selected(1)

    def event_button_left(self):
        return

    def event_button_right(self):
        return
