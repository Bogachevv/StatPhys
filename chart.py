import pygame
import pygame_chart as pyc


class ListBuff:
    def __init__(self, size):
        self.size = size
        self.buff = [0] * size
        self.main = []
        self.ind = 0

    def append(self, other):
        self.buff[self.ind] = other
        self.ind += 1
        if self.ind == self.size:
            self.main.extend(self.buff)
            self.ind = 0

    def __len__(self):
        return len(self.main)


class Chart:
    def __init__(self, app, name, position, size, border_color, len_buf=10, bd_width=3):
        self.screen = app.screen
        self.name = name
        self.chart = pyc.Figure(self.screen, position[0], position[1], size[0], size[1])
        self.border = pygame.Rect(*position, *size)
        self.bd_params = border_color, bd_width
        self.buf = ListBuff(len_buf)

    def draw(self, params):
        self.buf.append(params[self.name])
        if len(self.buf) > 1:
            self.chart.add_title(f'{self.name}_energy')
            self.chart.line(self.name, list(range(1, len(self.buf) + 1)), self.buf.main, line_width=10)
            self.chart.draw()
            pygame.draw.rect(self.screen, self.bd_params[0], self.border, self.bd_params[1])