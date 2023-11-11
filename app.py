import pygame
import screeninfo
from menu_screen import MenuScreen
from authors_screen import AuthorsScreen
from demo_screen import DemoScreen
import config


class App:
    def __init__(self):
        pygame.init()
        monitor = screeninfo.get_monitors()[0]
        monitor.height -= 1
        self.monitor = monitor
        self.screen = pygame.display.set_mode((monitor.width, monitor.height), pygame.NOFRAME)
        self.menu_screen = MenuScreen(self)
        self.authors_screen = AuthorsScreen(self)
        self.demo_screen = DemoScreen(self)
        self.clock = pygame.time.Clock()

        self.active_screen = self.menu_screen

        self._config = config.ConfigLoader()

    def run(self):
        """Запуск основного цикла игры."""
        while True:
            # Mouse and keyboard events handling
            self.active_screen._check_events()
            self.active_screen._update_screen()
            # Отображение последнего прорисованного экрана.
            pygame.display.flip()

            fps = self._config['FPS']
            self.clock.tick(fps)


if __name__ == '__main__':
    app = App()
    app.run()
