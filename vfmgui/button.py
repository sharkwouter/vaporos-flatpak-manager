import pygame
import vfmgui


class Button:
    def __init__(self, text):
        self.text = text
        self.font = pygame.font.Font(vfmgui.Fonts.REGULAR, 64)

    def draw(self, x, y, width, height, selected, screen):
        if selected:
            button_color = vfmgui.Colors.BUTTON_SELECTED
            text_color = vfmgui.Colors.BUTTON_TEXT_SELECTED
        else:
            button_color = vfmgui.Colors.BUTTON
            text_color = vfmgui.Colors.BUTTON_TEXT

        # Leave some space between buttons
        x += 1
        y += 1
        width -= 2
        height -= 2

        text = self.font.render(self.text, True, text_color, button_color)

        # Make sure the text is never wider than the button
        if text.get_width() > width:
            width = text.get_width()

        rect_text = pygame.Rect(x + width / 2 - text.get_width() / 2, y + height / 2 - text.get_height() / 2,
                                    text.get_width(), text.get_height())
        rect_button = pygame.Rect(x, y, width, height)

        # Draw everything
        pygame.draw.rect(screen, button_color, rect_button)
        screen.blit(text, rect_text)
