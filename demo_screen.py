import pygame
from button import Button
from slider import *
from demo import Demo
import pygame_chart as pyc
from chart import Chart
import config


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

        self.buttons = [Button(app, "Применить", (30, app.monitor.width * 0.43 + 60), (250, 80)),
                        Button(app, "Режим", (30 + 290, app.monitor.width * 0.43 + 60), (250, 80)),
                        Button(app, "Назад", (30 + 580, app.monitor.width * 0.43 + 60), (250, 80))]

        param_names, sliders_gap, param_poses, param_bounds, param_initial, param_step, par4sim, dec_numbers = (
            self._load_params())

        param_initial = map(_init_val_into_unit, param_initial, param_bounds)

        self.sliders = [
            ParamSlider(app, name, pos, bounds, step, name_par, dec_number,
                        button_color=self.bg_color, font='sans',
                        bold=False, fontSize=25,
                        initial_pos=initial
                        )
            for name, pos, bounds, initial, step, name_par, dec_number in
            zip(param_names, param_poses, param_bounds, param_initial, param_step, par4sim, dec_numbers)
        ]

        self.demo = Demo(app, (30, 30), (app.monitor.width * 0.43, app.monitor.width * 0.43), (255, 255, 255), (100, 100, 100), self.bg_color,
                         {name: sl.getValue() for name, sl in zip(par4sim, self.sliders)})

        self.demo_params = {'params': {name: sl.getValue() for name, sl in zip(par4sim[:-1], self.sliders[:-1])}, 'kinetic': [0] * param_bounds[-1][1],
                            'potential': [0] * param_bounds[-1][1], 'speed': self.sliders[-1].getValue()}

        buf_len = config.ConfigLoader()['buf_len']
        self.graphics = [Chart(self.app, 'kinetic', (app.monitor.width * 0.45 + 30, app.monitor.height * 0.30), (800, 330), (100, 100, 100),
                               len_buf=buf_len, const_legend='theoretical kinetic', const_func=self.demo.simulation.expected_kinetic_energy),
                         Chart(self.app, 'potential', (app.monitor.width * 0.45 + 30,  app.monitor.height * 0.30 + 340), (800, 330), (100, 100, 100),
                               len_buf=buf_len, const_legend='theoretical potential', const_func=self.demo.simulation.expected_potential_energy)]

        self.slider_grabbed = False

    def _load_params(self):
        loader = config.ConfigLoader()

        param_names = loader['param_names']
        sliders_gap = loader['sliders_gap']
        param_poses = [(self.app.monitor.width * 0.73 + 30, h) for h in range(50, 150 + len(param_names) * sliders_gap + 1, sliders_gap)]
        param_bounds = []
        param_initial = []
        for param_name in param_names:
            param_bounds.append(tuple(loader['param_bounds'][param_name]))
            param_initial.append(loader['param_initial'][param_name])
        param_step = [round((b[1] - b[0]) / 100, 3) for b in param_bounds]
        param_step[1], param_step[2] = int(param_step[1]), int(param_step[2])
        par4sim = loader['par4sim']
        dec_numbers = [1, 0, 0, 0, 1, 0, 0]

        return param_names, sliders_gap, param_poses, param_bounds, param_initial, param_step, par4sim, dec_numbers

    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self.demo.draw_check(self.demo_params)
        for button in self.buttons:
            button.draw_button()
        for slider in self.sliders[:-1]:
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
        # pygame_widgets.update(events)

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
                if index == 2:
                    self.app.active_screen = self.app.menu_screen

    def _draw_figures(self):
        for fig in self.graphics:
            fig.draw(self.demo_params)


def _init_val_into_unit(initial_val, bounds) -> float:
    if not (bounds[0] <= initial_val <= bounds[1]):
        raise ValueError("Initial val mus be in [bounds[0], bounds[1]]")

    return (initial_val - bounds[0]) / (bounds[1] - bounds[0])
