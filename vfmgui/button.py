import pygame
import vfmgui


class Button:
    def __init__(self, text):
        self.text = text
        self.font = vfmgui.Fonts.REGULAR
        self.progress = -1
        self.progress_direction = 1
        self.done = False
        self.failed = False

    def add_progress(self):
        self.progress += self.progress_direction
        if self.progress == 100:
            self.progress_direction = -1
        elif self.progress == 0:
            self.progress_direction = 1

    def draw(self, x, y, width, height, selected, screen):
        if selected and not self.done:
            button_color = vfmgui.Colors.BUTTON_SELECTED
            text_color = vfmgui.Colors.BUTTON_TEXT_SELECTED
        elif selected and self.done:
            text_color = vfmgui.Colors.BACKGROUND
            if self.failed:
                button_color = vfmgui.Colors.BUTTON_ERROR_SELECTED
            else:
                button_color = vfmgui.Colors.BUTTON_SUCCESS_SELECTED
        elif self.done:
            text_color = vfmgui.Colors.BACKGROUND
            if self.failed:
                button_color = vfmgui.Colors.BUTTON_ERROR
            else:
                button_color = vfmgui.Colors.BUTTON_SUCCESS
        else:
            button_color = vfmgui.Colors.BUTTON
            text_color = vfmgui.Colors.BUTTON_TEXT

        if self.progress > -1:
            text_color = vfmgui.Colors.BACKGROUND

        # Leave some space between buttons
        x += 1
        y += 1
        width -= 2
        height -= 2

        text = self.font.render(self.text, True, text_color)

        # Make sure the text is never wider than the button
        if text.get_width() > width:
            width = text.get_width()

        rect_text = pygame.Rect(x + width / 2 - text.get_width() / 2, y + height / 2 - text.get_height() / 2,
                                    text.get_width(), text.get_height())
        rect_button = pygame.Rect(x, y, width, height)

        # Draw button
        pygame.draw.rect(screen, button_color, rect_button)

        # Show progress
        if self.progress > -1:
            progress_left = 5
            progress_right = 5
            print(float(width*0.01))
            if self.progress < progress_left:
                progress_left = self.progress
            if self.progress + progress_right > 100:
                progress_right = 100 - self.progress
            rect_progress = pygame.Rect(x + float(width * 0.01) * (self.progress - progress_left), y,
                                        float(width * 0.01) * (progress_left + progress_right), height)
            pygame.draw.rect(screen, vfmgui.Colors.BUTTON_PROGRESS, rect_progress)

        # Draw text
        screen.blit(text, rect_text)
