import pygame
import vfmgui
import threading


class ApplicationButton:
    def __init__(self, application):
        self.application = application
        self.selected = False
        self.image = None
        self.invalid_image = False
        self.getting_image = False
        self.application_name = str(application)
        self.font = pygame.font.Font(vfmgui.Fonts.REGULAR, 64)

    def __get_color(self):
        if self.selected:
            return vfmgui.Colors.BUTTON_SELECTED
        return vfmgui.Colors.BUTTON

    def __get_text_color(self):
        if self.selected:
            return vfmgui.Colors.BUTTON_TEXT_SELECTED
        return vfmgui.Colors.BUTTON_TEXT

    def __set_title(self):
        self.title = self.font.render(self.application_name, True, self.__get_text_color(), self.__get_color())

    def __set_image(self):
        # Try loading the application image
        self.getting_image = True
        image_path = self.application.get_image()
        try:
            loaded_image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(loaded_image, (128, 128))
        except:
            print("{} isn't a valid image".format(image_path))
            self.invalid_image = True

        self.getting_image = False

    def draw(self, x, y, width, height, selected, screen):
        # Set the colors based on if this button is the current selection
        if selected:
            text_color = vfmgui.Colors.BUTTON_TEXT_SELECTED
            button_color = vfmgui.Colors.BUTTON_SELECTED
        else:
            text_color = vfmgui.Colors.BUTTON_TEXT
            button_color = vfmgui.Colors.BUTTON

        # Keeps some space between buttons
        x += 1
        y += 1
        width -= 2
        height -= 2

        # Download the image in another thread
        if self.image is None and not self.invalid_image and not self.getting_image:
            thread = threading.Thread(target=self.__set_image)
            thread.start()

        # Create the different rectangles to draw different elements in
        rect_button = pygame.Rect(x, y, width, height)
        rect_image = pygame.Rect(x + width / 2 - 64, y + 15, 128, 128)

        # Create the title text
        title = self.font.render(self.application_name, True, text_color, button_color)

        # Make sure the application name isn't long to fit
        if title.get_width() > width:
            drop_letters = 3
            while title.get_width() > width:
                self.application_name = str(self.application)[:-drop_letters] + ".."
                title = self.font.render(self.application_name, True, text_color, button_color)
                drop_letters += 1

        # Make sure the title isn't draw too low
        if x + 160 + title.get_height() > x + height:
            rect_title = pygame.Rect(x + width / 2 - title.get_width() / 2,
                                          y + height - title.get_height(), title.get_width(),
                                          title.get_height())
        else:
            rect_title = pygame.Rect(x + width / 2 - title.get_width() / 2, y + height - title.get_height() - 16, title.get_width(),
                                          title.get_height())

        # Draw everything
        pygame.draw.rect(screen, button_color, rect_button)
        if self.image is not None:
            screen.blit(self.image, rect_image)
        screen.blit(title, rect_title)
