import pygame
import pygame_widgets
from button import Button
from slider import *
from demo import Demo
import pygame_chart as pyc
from chart import Chart

class DemoScreen:
    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.speed = 0.5
        self.bg_color = (210, 210, 210)
        self.font = 'corbel'
        self.little_font = pygame.font.SysFont(self.font, 35)
        self.middle_font = pygame.font.SysFont(self.font, 40, bold=True)
        self.big_font = pygame.font.SysFont(self.font, 50)

        self.buttons = [Button(app, "Назад", (1300, 900), (300, 80))]

        param_names = ['Размер связанных частиц:', 'Температура:', 'Число молекул:', 'Коэффицент упругости:', 'Коэффицент нелинейности:', 'Масса связанных частиц:']
        sliders_gap = 70
        param_poses = [(1600, h) for h in range(150, 150 + len(param_names) * sliders_gap + 1, sliders_gap)]
        param_bounds = [(1, 5), (0, 500), (50, 150), (100, 500), (0.01, 1), (1, 10)]
        param_step = [round((b[1] - b[0]) / 100, 3) for b in param_bounds]
        param_step[1], param_step[2] = int(param_step[1]), int(param_step[2])
        par4sim = ['R', 'T', 'r', 'k', 'gamma', 'm_spring']
        dec_numbers = [1, 0, 0, 0, 1, 0]

        self.sliders = [SliderTest(app, name, pos, bounds, step, name_par, dec_number, button_color=self.bg_color, font='sans', bold=False, fontSize=25)
                         for name, pos, bounds, step, name_par, dec_number in zip(param_names, param_poses, param_bounds, param_step, par4sim, dec_numbers)]
        self.demo = Demo(app, (170, 50), (600, 600), (255, 255, 255), (100, 100, 100), self.bg_color, {name: sl.getValue() for name, sl in zip(par4sim, self.sliders)})
        
        self.demo_params = {'params': {name: sl.getValue() for name, sl in zip(par4sim, self.sliders)}, 'kinetic': 0, 'potential': 0}

        self.graphics = [Chart(self.app,'kinetic', (100, 670), (500, 400), (100, 100, 100)),
                         Chart(self.app,'potential', (650, 670), (500, 400), (100, 100, 100))]



        self.slider_grabbed = False
    
    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self.demo.draw_check(self.demo_params)
        for button in self.buttons:
            button.draw_button()
        for slider in self.sliders:
            slider.draw_check(self.demo_params['params'])
        self._draw_figures()
    
    def _check_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._check_buttons(mouse_position)
            
            mouse_pos = pygame.mouse.get_pos()
            mouse = pygame.mouse.get_pressed()
            self._check_sliders(mouse_pos, mouse)
        #pygame_widgets.update(events)

    def _check_sliders(self, mouse_position, mouse_pressed):
        for slider in self.sliders:
                if slider.slider.button_rect.collidepoint(mouse_position):
                    if mouse_pressed[0] and not self.slider_grabbed:
                        slider.slider.grabbed = True
                        self.slider_grabbed = True
                if not mouse_pressed[0]:
                    slider.slider.grabbed = False
                    self.slider_grabbed = False
                if slider.slider.button_rect.collidepoint(mouse_position):  
                    slider.slider.hover()
                if slider.slider.grabbed:
                    slider.slider.move_slider(mouse_position)
                    slider.slider.hover()
                else:
                    slider.slider.hovered = False

    def _check_buttons(self, mouse_position):
        for index, button in enumerate(self.buttons):
            if button.rect.collidepoint(mouse_position):
                if index == 0:
                    self.app.active_screen = self.app.menu_screen

    def _draw_figures(self):
        for fig in self.graphics:
            fig.draw(self.demo_params)
