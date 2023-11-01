import pygame
import sys
from button import Button

class AuthorsScreen():
    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.folder = '_internal/images/'
        self.bg_color = (255, 255, 255)
        self.font = 'sans'
        self.little_font = pygame.font.SysFont(self.font, 38)
        self.middle_font = pygame.font.SysFont(self.font, 40, bold=True)
        self.big_font = pygame.font.SysFont(self.font, 50)
        self.strings = ["Московский Государственный Университет",
                        "Факультет вычислительной математики и кибернетики", 
                        "Лектор: Андреев Анатолий Васильевич",
                        "Руководитель: Чичигина Ольга Александровна",
                        "Валеев Арслан",
                        "Богачев Владимир"]
        
        self.strings_surfaces = []
        for index, string in enumerate(self.strings):
            if index < 2:
                self.strings_surfaces.append(self.middle_font.render(string, False, (0, 0, 0)))
            else:
                self.strings_surfaces.append(self.little_font.render(string, False, (0, 0, 0)))
        
        #self.text_positions = [(400, 100), (500, 150), (670, 850), (600, 790), (395, 720), (1230, 720)]
        self.text_positions = [(560, 100), (450, 150), (650, 850), (580, 790), (395, 720), (1200, 720)]
        
        self.pictures = [pygame.transform.scale(pygame.image.load(self.folder + "cmc_logo.jpg"), (140, 140)),
                         pygame.transform.scale(pygame.image.load(self.folder + "msu_logo.jpg"), (150, 150)),
                         pygame.transform.scale(pygame.image.load(self.folder + "volodya.png"), (400, 400)),
                         pygame.transform.scale(pygame.image.load(self.folder + "volodya.png"), (400, 400))]
        
        self.pictures_positions = [(1600, 80), (180, 80), (340, 300), (1160, 300)]
        self.buttons = [Button(app, "Назад", (1300, 900), (300, 80))]
    
    def _update_screen(self):
        self.screen.fill(self.bg_color)
        for index, surface in enumerate(self.strings_surfaces):
            self.screen.blit(surface, self.text_positions[index])


        for index, picture in enumerate(self.pictures):
            self.screen.blit(picture, self.pictures_positions[index])

        for button in self.buttons:
            button.draw_button()
    
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._check_buttons(mouse_position)
    
    def _check_buttons(self, mouse_position):
        for index, button in enumerate(self.buttons):
            if button.rect.collidepoint(mouse_position):
                if index == 0:
                    self.app.active_screen = self.app.menu_screen
        