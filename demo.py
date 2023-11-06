import pygame
import numpy as np
from simulation import Simulation

R_SIZE = 0.01
R_MASS = 10e-5

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


        self.params = params
        # self.simulation = Simulation(1, params['k'], params['l_0'], params['R'] / 1000, 0.05,
        #                              r_init, np.random.uniform(size=(2, 2)),
        #                              np.random.uniform(size=(2, int(params['r']))), np.random.uniform(size=(2, 2)),
        #                              np.full((int(params['r']), ), 10 ** (-5)),
        #                              np.full((2, ), params['m_spring'] * (10 ** (-5))))
        r_init = np.random.uniform(size=(2, params['r'] + 2))
        v_init = np.random.uniform(low=-500, high=500, size=(2, params['r'] + 2))
        m = np.ones((params['r'] + 2, )) * R_MASS
        m_spring = m[:2] * params['m_spring']
        m = m[2:]
        r, r_spring = r_init[:, 2:], r_init[:, :2]
        v, v_spring = v_init[:, 2:], v_init[:, :2]
        # Размер броуновских частиц

        self.simulation = Simulation(
            gamma=params['gamma'], k=params['k'], l_0=0.1, R=R_SIZE, R_spring=R_SIZE * params['R'],
            r=r, r_spring=r_spring,
            v=v, v_spring=v_spring,
            m=m, m_spring=m_spring,
        )

    def set_params(self, params, par):
        if par == 'gamma':
            self.simulation.set_params(gamma=params['gamma'])
        elif par == 'k':
            self.simulation.set_params(k=params['k'])
        elif par == 'R':
            self.simulation.set_params(R_spring=params['R'] * R_SIZE)
        elif par == 'T':
            self.simulation.set_params(T=params['T'])
        elif par == 'r':
            self.simulation.set_params(particles_cnt=params['r'])
        elif par == 'm_spring':
            self.simulation.set_params(m_spring=params['m_spring'] * R_MASS)

    def draw_check(self, params):
        pygame.draw.rect(self.screen, self.bg_color, self.main)
        # updating params
        modified_par = None
        for i, par1, par2 in zip(range(len(self.params)), params['params'].values(), self.params.values()):
            if abs(par1 - par2) > 1e-4:
                modified_par = list(self.params.keys())[i]
                break

        if modified_par is not None:
            self.set_params(params['params'], modified_par)
            self.params[modified_par] = params['params'][modified_par]

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
