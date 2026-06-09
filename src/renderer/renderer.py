import pygame
from pathlib import Path
from typing import List, Tuple, Dict, Union
from src.network import DroneNetwork
from .menu import Menu
import sys
from math import sin


class Renderer:
    """Renders the drone network using pygame"""
    def __init__(self) -> None:
        """Initialize the renderer."""
        pygame.init()
        pygame.display.set_caption("Fly-in Drone-out")
        screen_size = pygame.display.get_desktop_sizes()[0]

        big_screen = screen_size[0] > 2000
        self._width = 800 * (big_screen + 1)
        self._height = 600 * (big_screen + 1)
        self._screen = pygame.display.set_mode(
            (self._width, self._height), pygame.RESIZABLE
        )
        self._menu = Menu(self._screen)
        self._clock = pygame.time.Clock()
        self._fps = 60
        self._frame = 0.0

        self._drone_sprites: List[pygame.Surface] = self._load_sprites("drone")
        self._bg_sprites: List[pygame.Surface] = self._load_sprites("bg")
        self._hub_sprites: Dict[str, pygame.Surface] = self._load_hub_sprites()

        self._sprite_size = (128 if big_screen else 64)
        self._font = pygame.font.SysFont("Consolas", 35 if big_screen else 20)

    def start(self, network: DroneNetwork) -> None:
        """Start the rendering interface."""
        self._network = network
        xs, ys = zip(*(hub.pos for hub in network.hubs))
        self._max_x = max(xs)
        self._min_x = min(xs)
        self._max_y = max(ys)
        self._min_y = min(ys)
        self._diff_x = abs(self._min_x) if self._min_x < 0 else 0
        self._diff_y = abs(self._min_y) if self._min_y < 0 else 0
        self._max_x += self._diff_x
        self._max_y += self._diff_y
        if self._diff_x:
            self._min_x = 0
        if self._diff_y:
            self._min_y = 0

    def _load_hub_sprites(self) -> Dict[str, pygame.Surface]:
        """Load hub sprites from folder as a dict."""
        path = Path("sprites/hub_sprites")
        files: List[Path] = sorted(path.glob("*.png"))
        return {
            file.stem: pygame.image.load(file).convert_alpha()
            for file in files
        }

    def _load_sprites(self, name: str) -> List[pygame.Surface]:
        """Load any sprites from folder as a list."""
        path = Path(f"sprites/{name}_sprites")
        files: List[Path] = sorted(path.glob("*.png"))
        return [
            pygame.image.load(file).convert_alpha()
            for file in files
        ]

    def _translate_pos(
        self,
        screen_size: Tuple[int, int],
        pos: Tuple[float, float],
        line: bool = False
    ) -> Tuple[float, float]:
        """Translate the position according to the screen size."""
        x, y = pos
        width, height = screen_size
        max_x, max_y = self._max_x, self._max_y
        min_x, min_y = self._min_x, self._min_y
        offset = self._sprite_size
        x += self._diff_x
        y += self._diff_y
        line_offset = self._sprite_size // 2 if line else 0

        range_x = max_x - min_x
        range_y = max_y - min_y

        if range_x == 0:
            range_x = 1
        if range_y == 0:
            range_y = 1

        py = 50
        scale_x = (width - offset) / range_x
        scale_y = (height - offset - py) / range_y

        x = int((x - min_x) * scale_x + line_offset)
        y = int((y - min_y) * scale_y + line_offset + py)
        return x, y

    def choose_file(self) -> str:
        """Render the menu until a file is chosen."""
        file = ""
        while not file:
            file = self._menu.display_menu()
        return file

    def display(self) -> None:
        """Display the drone network."""
        self._screen.fill("0x222034")
        screen_size = self._screen.get_size()

        def draw_edges() -> None:
            """Draw edges from the drone network."""
            edges = self._network.edges
            lines_surface = pygame.Surface(
                self._screen.get_size(), pygame.SRCALPHA
            )
            for edge in edges:
                start, end = [
                    self._translate_pos(screen_size, hub.pos, line=True)
                    for hub in edge.hubs
                ]
                try:
                    color = pygame.Color(edge.hubs[1].color)
                    color.a = 50
                except (ValueError, TypeError):
                    color = pygame.Color(255, 255, 255, 50)

                if edge.hubs[1].color == "rainbow":
                    color = pygame.Color(get_rainbow_color())
                    color.a = 50

                pygame.draw.line(lines_surface, color, start, end, 5)

            self._screen.blit(lines_surface, (0, 0))

        def draw_hubs() -> None:
            """Draw hubs from the drone network."""
            for hub in self._network.hubs:
                pos = self._translate_pos(screen_size, hub.pos)
                sprite = self._hub_sprites[
                    hub.zone if hub.max_drones == 1 else f"{hub.zone}_plus"
                ]
                if hub.color == "rainbow":
                    sprite = color_image(sprite, get_rainbow_color())
                else:
                    color = hub.color
                    if hub.color == "black":
                        color = "0x222222"
                    sprite = color_image(sprite, color)
                sprite = pygame.transform.scale(
                    sprite, (self._sprite_size, self._sprite_size)
                )
                self._screen.blit(sprite, pos)

        def draw_drones() -> None:
            """Draw drones from the drone network."""
            sprites_len = len(self._drone_sprites)
            for drone in self._network.drones:
                pos = self._translate_pos(screen_size, drone.pos)
                sprite = (
                    self._drone_sprites[round(self._frame) % sprites_len]
                )
                x, y = pos
                sprite = pygame.transform.scale(
                    sprite, (self._sprite_size, self._sprite_size)
                )
                self._screen.blit(sprite, (x, y - 20))

        def get_rainbow_color() -> Tuple[int, int, int]:
            """Get a color from the current frame and apply a sin wave."""
            frame = self._frame * 0.5
            r = int(sin(frame) * 127 + 128)
            g = int(sin(frame + 2) * 127 + 128)
            b = int(sin(frame + 4) * 127 + 128)
            color = (r, g, b)
            return color

        def color_image(
            image: pygame.Surface, color: Union[str | Tuple[int, int, int]]
        ) -> pygame.Surface:
            """Tint an image."""
            temp = image.copy()
            try:
                temp.fill(color, special_flags=pygame.BLEND_RGB_MULT)
            except (ValueError, TypeError):
                pass
            return temp

        def draw_bg() -> None:
            """Render the background."""
            screen_width, screen_height = screen_size
            sprites_len = len(self._bg_sprites)
            bg = (
                self._bg_sprites[round(self._frame / 10) % sprites_len]
            )

            for y in range(0, screen_height, self._sprite_size):
                for x in range(0, screen_width, self._sprite_size):
                    if (x + y) % 3:
                        continue
                    x_pos = (
                        x + (self._frame % (screen_width + self._sprite_size))
                    )
                    if x_pos > screen_width:
                        x_pos = x_pos - screen_width - self._sprite_size
                    self._screen.blit(bg, (x_pos, y))

        self._clock.tick(self._fps)
        self._frame += 0.2
        draw_bg()
        text_surf = self._font.render(
            f"Turns: {self._network.turn}", True, "white"
        )
        self._screen.blit(text_surf, (10, 10))
        draw_edges()
        draw_hubs()
        draw_drones()
        pygame.display.flip()

    def handle_events(self) -> str:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if len(self._menu.items) == 1:
                        sys.exit()
                    return "quit"

        return ""
