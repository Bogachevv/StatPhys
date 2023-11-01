import pygame
import numpy as np
from simulation import Simulation

class Demo:
    def __init__(self, app, position, demo_size, bg_color, border_color, bg_screen_color, params):
        self.screen = app.screen
        self.bg_color = bg_color
        self.bg_screen_color = bg_screen_color
        self.bd_color = border_color
        self.position = position
        self.main = pygame.Rect(*position, *demo_size)
        self.size = demo_size[0]
        self.pos_start = position[0], position[1] + self.size

        print(params)

        self.params = params
        # self.simulation = Simulation(1, params['k'], params['l_0'], params['R'] / 1000, 0.05,
        #                              r_init, np.random.uniform(size=(2, 2)),
        #                              np.random.uniform(size=(2, int(params['r']))), np.random.uniform(size=(2, 2)),
        #                              np.full((int(params['r']), ), 10 ** (-5)),
        #                              np.full((2, ), params['m_spring'] * (10 ** (-5))))
        r_init = np.random.uniform(size=(2, params['r'] + 2))
        v_init = np.random.uniform(low=-500, high=500, size=(2, params['r'] + 2))
        m = np.ones((params['r'] + 2, )) * 10e-5
        m_spring = m[:2] * params['m_spring']
        m = m[2:]
        r, r_spring = r_init[:, 2:], r_init[:, :2]
        v, v_spring = v_init[:, 2:], v_init[:, :2]
        # Размер броуновских частиц
        R_SIZE = 0.01

        self.simulation = Simulation(
            gamma=1.0, k=params['k'], l_0=params['l_0'], R=R_SIZE, R_spring=0.025,
            r=r, r_spring=r_spring,
            v=v, v_spring=v_spring,
            m=m, m_spring=m_spring,
        )

    def draw_check(self, params):
        pygame.draw.rect(self.screen, self.bg_color, self.main)
        if sum(abs(par1 - par2) > 1e-4 for par1, par2 in zip(params['params'].values(), self.params.values())):
            self.simulation.set_params(params)
            self.params = params['params']
        new_args = next(self.simulation)

        params['kinetic'] = self.simulation.calc_kinetic_energy().item()
        params['potential'] = self.simulation.calc_potential_energy().item()

        r, r_spring = new_args[0].copy(), new_args[1].copy()
        r_radius = self.size * self.simulation.R
        r_spring_radius = self.size * self.simulation.R_spring
        r[0], r_spring[0] = self.pos_start[0] + r[0] * self.size, self.pos_start[0] + r_spring[0] * self.size
        r[1], r_spring[1] = self.pos_start[1] - r[1] * self.size, self.pos_start[1] - r_spring[1] * self.size
        r, r_spring, r_radius, r_spring_radius = np.round(r), np.round(r_spring), np.round(r_radius), np.round(r_spring_radius)
        for i in range(r.shape[1]):
            pygame.draw.circle(self.screen, (250, 0, 0), tuple(r[:, i]), r_radius)
        for i in range(r_spring.shape[1]):
            pygame.draw.circle(self.screen, (0, 0, 0), tuple(r_spring[:, i]), r_spring_radius)

        # draw spring
        pygame.draw.line(self.screen, (0, 0, 0), tuple(r_spring[:, 0]), tuple(r_spring[:, 1]), width=2)
        # draw border
        inner_border = 3
        mask_border = 50
        pygame.draw.rect(self.screen, self.bg_screen_color, (self.position[0] - mask_border, self.position[1] - mask_border, self.size + mask_border * 2, self.size + mask_border * 2), mask_border)
        pygame.draw.rect(self.screen, self.bd_color, (
        self.position[0] - inner_border, self.position[1] - inner_border, self.size + inner_border * 2,
        self.size + inner_border * 2), inner_border)

