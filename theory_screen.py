import pygame
from button import Button


class TheoryScreen():
    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.folder = '_internal/images/'
        self.bg_color = (255, 255, 255)
        self.font = 'sans'
        self.little_font = pygame.font.SysFont(self.font, 38)
        self.middle_font = pygame.font.SysFont(self.font, 40, bold=True)
        self.big_font = pygame.font.SysFont(self.font, 50)

        self.pictures = [pygame.transform.scale(pygame.image.load(self.folder + "theory.png"), (self.app.monitor.width - 30 - 30, self.app.monitor.height - 30 - 60))]

        self.pictures_positions = [(30, 30)]

        self.buttons = [Button(app, "Назад", (self.app.monitor.width - 300 - 30, self.app.monitor.height - 80 - 60 ), (300, 80))]

    def _update_screen(self):
        self.screen.fill(self.bg_color)
#        for index, surface in enumerate(self.strings_surfaces):
#            self.screen.blit(surface, self.text_positions[index])

        for index, picture in enumerate(self.pictures):
            self.screen.blit(picture, self.pictures_positions[index])

        for button in self.buttons:
            button.draw_button()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._check_buttons(mouse_position)

    def _check_buttons(self, mouse_position):
        for index, button in enumerate(self.buttons):
            if button.rect.collidepoint(mouse_position):
                if index == 0:
                    self.app.active_screen = self.app.menu_screen
