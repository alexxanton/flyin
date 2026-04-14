import pygame


class Renderer:
    """Renders the drone network using pygame"""
    def __init__(self, width: int, height: int) -> None:
        pygame.init()
        self._width: int = width
        self._height: int = height
        self._screen: pygame.Surface = pygame.display.set_mode((width, height))
        self._clock: pygame.time.Clock = pygame.time.Clock()
        self._fps: int = 60

    def display(self) -> None:
        pygame.display.flip()

    def handle_events(self) -> str:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"

        return ""
