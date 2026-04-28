import pygame
from pathlib import Path
from typing import List, Tuple, Dict
from src.network import DroneNetwork
from .menu import Menu
import sys
from math import sin


class Renderer:
    """Renders the drone network using pygame"""
    def __init__(self, width: int, height: int) -> None:
        pygame.init()
        pygame.display.set_caption("Fly-in Drone-out")
        self._width: int = width
        self._height: int = height
        self._screen: pygame.Surface = pygame.display.set_mode(
            (width, height), pygame.RESIZABLE
        )
        self._menu = Menu(self._screen)
        self._clock: pygame.time.Clock = pygame.time.Clock()
        self._fps: int = 60
        self._frame: float = 0.0

        self._drone_sprites: List[pygame.Surface] = self._load_sprites("drone")
        self._bg_sprites: List[pygame.Surface] = self._load_sprites("bg")
        self._hub_sprites: Dict[str, pygame.Surface] = self._load_hub_sprites()
        self._sprite_size: int = 64
        self._font: pygame.font.Font = pygame.font.SysFont("Consolas", 20)

    def start(self, network: DroneNetwork) -> None:
        self._network = network
        xs, ys = zip(*(hub.pos for hub in network.hubs))
        self._max_x: int = max(xs)
        self._min_x: int = min(xs)
        self._max_y: int = max(ys)
        self._min_y: int = min(ys)
        self._diff_x: int = abs(self._min_x) if self._min_x < 0 else 0
        self._diff_y: int = abs(self._min_y) if self._min_y < 0 else 0
        self._max_x += self._diff_x
        self._max_y += self._diff_y
        if self._max_x:
            self._min_x = 0
        if self._max_y:
            self._min_y = 0

    def _load_hub_sprites(self) -> Dict[str, pygame.Surface]:
        path: Path = Path("src/renderer/sprites/hub_sprites")
        files: List[Path] = sorted(path.glob("*.png"))
        return {
            file.stem: pygame.image.load(file).convert_alpha()
            for file in files
        }

    def _load_sprites(self, name: str) -> List[pygame.Surface]:
        path: Path = Path(f"src/renderer/sprites/{name}_sprites")
        files: List[Path] = sorted(path.glob("*.png"))
        return [
            pygame.image.load(file).convert_alpha()
            for file in files
        ]

    def _translate_pos(
        self,
        screen_size: Tuple[int, int],
        pos: Tuple[int, int],
        line: bool=False
    ) -> Tuple[int, int]:
        x, y = pos
        width, height = screen_size
        max_x, max_y = self._max_x, self._max_y
        min_x, min_y = self._min_x, self._min_y
        offset = self._sprite_size
        x += self._diff_x
        y += self._diff_y
        line_offset = self._sprite_size // 2 if line else 0
        if max_x == 0:
            max_x = 1
        if max_y == 0:
            max_y = 1

        py = 50
        x = (x - min_x) * ((width - offset) // max_x) + line_offset
        y = (y - min_y) * ((height - offset - py) // max_y) + line_offset + py
        return x, y

    def choose_file(self) -> str:
        file = ""
        while not file:
            file = self._menu.display_menu()
        return file

    def display(self) -> None:
        self._screen.fill("0x222034")
        screen_size = self._screen.get_size()

        def draw_edges() -> None:
            edges = self._network.edges
            lines_surface: pygame.Surface = pygame.Surface(
                self._screen.get_size(), pygame.SRCALPHA
            )
            for edge in edges:
                start, end = [
                    self._translate_pos(screen_size, hub.pos, line=True)
                    for hub in edge.hubs
                ]
                try:
                    color: pygame.Color = pygame.Color(edge.hubs[1].color)
                    color.a = 50
                except (ValueError, TypeError):
                    color = "0x111111"

                if edge.hubs[1].color == "rainbow":
                    color = pygame.Color(get_rainbow_color())
                    color.a = 50

                pygame.draw.line(lines_surface, color, start, end, 5)

            self._screen.blit(lines_surface, (0, 0))

        def draw_hubs() -> None:
            for hub in self._network.hubs:
                pos: Tuple[int, int] = self._translate_pos(
                    screen_size, hub.pos
                )
                sprite = self._hub_sprites[
                    hub.zone if hub.max_drones == 1 else f"{hub.zone}_plus"
                ]
                if hub.color == "rainbow":
                    sprite = color_image(sprite, get_rainbow_color())
                else:
                    color: str = hub.color
                    if hub.color == "black":
                        color = "0x222222"
                    sprite = color_image(sprite, color)
                #sprite = pygame.transform.scale(sprite, (128, 128))
                self._screen.blit(sprite, pos)

        def draw_drones() -> None:
            sprites_len: int = len(self._drone_sprites)
            for drone in self._network.drones:
                pos: Tuple[int, int] = self._translate_pos(
                    screen_size, drone.pos
                )
                sprite: pygame.Surface = (
                    self._drone_sprites[round(self._frame) % sprites_len]
                )
                x, y = pos
                self._screen.blit(sprite, (x, y - 20))

        def get_rainbow_color() -> Tuple[int, int, int]:
            frame: float = self._frame * 0.5
            r: int = int(sin(frame) * 127 + 128)
            g: int = int(sin(frame + 2) * 127 + 128)
            b: int = int(sin(frame + 4) * 127 + 128)
            color: Tuple[int, int, int] = (r, g, b)
            # print(color)
            return color

        def color_image(image: pygame.Surface, color: str) -> pygame.Surface:
            temp: pygame.Surface = image.copy()
            try:
                temp.fill(color, special_flags=pygame.BLEND_RGB_MULT)
            except (ValueError, TypeError):
                pass
            return temp

        def draw_bg() -> None:
            screen_width, screen_height = screen_size
            sprites_len: int = len(self._bg_sprites)
            bg: pygame.Surface = (
                self._bg_sprites[round(self._frame / 10) % sprites_len]
            )

            for y in range(0, screen_height, self._sprite_size):
                for x in range(0, screen_width, self._sprite_size):
                    if (x + y) % 3:
                        continue
                    x_pos = x + (self._frame % (screen_width + self._sprite_size))
                    if x_pos > screen_width:
                        x_pos = x_pos - screen_width - self._sprite_size
                    self._screen.blit(bg, (x_pos, y))

        self._clock.tick(self._fps)
        self._frame += 0.2
        draw_bg()
        text_surf: pygame.Surface = self._font.render(
            f"Turns: {self._network.turns}", True, "white"
        )
        self._screen.blit(text_surf, (10, 10))
        draw_edges()
        draw_hubs()
        draw_drones()
        pygame.display.flip()

    def handle_events(self) -> str:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if len(self._menu.items) == 1:
                    sys.exit()
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if len(self._menu.items) == 1:
                        sys.exit()
                    return "quit"

        return ""
