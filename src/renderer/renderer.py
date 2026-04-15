import pygame
from pathlib import Path
from typing import List, Tuple, Dict
from src.network import DroneNetwork


class Renderer:
    """Renders the drone network using pygame"""
    def __init__(self, width: int, height: int, network: DroneNetwork) -> None:
        pygame.init()
        pygame.display.set_caption("Fly-in Drone-out")
        self._width: int = width
        self._height: int = height
        self._network: DroneNetwork = network
        self._screen: pygame.Surface = pygame.display.set_mode((width, height))
        self._clock: pygame.time.Clock = pygame.time.Clock()
        self._fps: int = 60
        self._frame: float = 0.0

        self._max_x: int = max([hub.get_pos()[0] for hub in network.hubs])
        self._max_y: int = max([hub.get_pos()[1] for hub in network.hubs])
        self._min_x: int = min([hub.get_pos()[0] for hub in network.hubs])
        self._min_y: int = min([hub.get_pos()[1] for hub in network.hubs])

        self._drone_frames: List[pygame.Surface] = self._load_drone_sprites()
        self._hub_frames: Dict[str, pygame.Surface] = self._load_hub_sprites()

    def _load_hub_sprites(self) -> Dict[str, pygame.Surface]:
        path: Path = Path("src/renderer/sprites/hub_sprites")
        files: List[Path] = sorted(path.glob("*.png"))
        return {
            file.stem: pygame.image.load(file).convert_alpha()
            for file in files
        }

    def _load_drone_sprites(self) -> List[pygame.Surface]:
        path: Path = Path("src/renderer/sprites/drone_sprites")
        files: List[Path] = sorted(path.glob("*.png"))
        return [
            pygame.image.load(file).convert_alpha()
            for file in files
        ]

    def display(self) -> None:
        self._screen.fill((0, 0, 0))
        width, height = self._screen.get_size()

        def translate_pos(pos: Tuple[int, int]) -> Tuple[int, int]:
            x, y = pos
            x = (x - self._min_x) * ((width - 64) // self._max_x)
            y = (y - self._min_y) * ((height - 64) // self._max_y)
            return x, y

        def color_image(image: pygame.Surface, color: str) -> pygame.Surface:
            temp: pygame.Surface = image.copy()
            try:
                temp.fill(color, special_flags=pygame.BLEND_RGB_MULT)
            except (ValueError, TypeError):
                pass
            return temp

        self._clock.tick(self._fps)
        self._frame += 0.2
        for hub in self._network.hubs:
            pos: Tuple[int, int] = translate_pos(hub.get_pos())
            sprite: pygame.Surface = self._drone_frames[round(self._frame) % 4]
            sprite = self._hub_frames["hub_planet"]
            sprite = color_image(sprite, hub.color)
            self._screen.blit(sprite, pos)

        pygame.display.flip()

    def handle_events(self) -> str:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"

        return ""
