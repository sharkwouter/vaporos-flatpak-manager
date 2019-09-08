import pygame
import vfmgui


class ApplicationButton:
    def __init__(self, application, x, y, width, height, screen):
        self.application = application
        self.__screen = screen
        self.selected = False

        # Keeps some space between buttons without effort
        x += 1
        y += 1
        width -= 2
        height -= 2

        self.application_name = str(application)
        self.font = pygame.font.Font(vfmgui.Fonts.REGULAR, 64)
        self.__set_title()

        # Create the different rectangles to draw different elements in
        self.rect_button = pygame.Rect(x, y, width, height)
        self.rect_image = pygame.Rect(x+width/2-64, y+16, 128, 128)

        # Make sure the application name isn't long to fit
        if self.title.get_width() > width:
            drop_letters = 3
            while self.title.get_width() > width:
                self.application_name = str(self.application)[:-drop_letters] + ".."
                self.__set_title()
                drop_letters += 1

        # Make sure the title isn't draw too low
        if x+160+self.title.get_height() > x+height:
            self.rect_title = pygame.Rect(x + width / 2 - self.title.get_width() / 2, y+height-self.title.get_height(), self.title.get_width(),
                                          self.title.get_height())
        else:
            self.rect_title = pygame.Rect(x+width/2-self.title.get_width()/2, y+160, self.title.get_width(), self.title.get_height())

        # Try loading the application image
        image_path = application.get_image()
        try:
            loaded_image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(loaded_image, (128, 128))
        except:
            print("{} isn't a valid image".format(image_path))
            self.image = None

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

    def draw(self, selected):
        self.selected = selected
        self.__set_title()

        pygame.draw.rect(self.__screen, self.__get_color(), self.rect_button)
        if self.image is not None:
            self.__screen.blit(self.image, self.rect_image)
        self.__screen.blit(self.title, self.rect_title)
