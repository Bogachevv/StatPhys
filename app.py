import pygame
import screeninfo
import sys
from menu_screen import MenuScreen
from authors_screen import AuthorsScreen
from demo_screen import DemoScreen
class App:
    def __init__(self):
        pygame.init()
        monitor = screeninfo.get_monitors()[0]
        self.screen = pygame.display.set_mode((monitor.width, monitor.height))
        self.menu_screen = MenuScreen(self)
        self.authors_screen = AuthorsScreen(self)
        self.demo_screen = DemoScreen(self)
        self.clock = pygame.time.Clock()

        self.active_screen = self.menu_screen

    def run(self):
        """Запуск основного цикла игры."""
        while True:
        # Отслеживание событий клавиатуры и мыши.
            self.active_screen._check_events()
            self.active_screen._update_screen()
            # Отображение последнего прорисованного экрана.
            pygame.display.flip()

            self.clock.tick(20)


if __name__ == '__main__':
    app = App()
    app.run()