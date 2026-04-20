import pygame
from pathlib import Path
from typing import List
import sys


class MenuItem:
    def __init__(self, name: str, path: Path, clickable: bool, depth: bool) -> None:
        self._name: str = name
        self._path: Path = path
        self._clickable: bool = clickable
        self._depth: bool = depth
        self._rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)

    @property
    def name(self) -> int:
        return self._name

    @property
    def path(self) -> int:
        return self._path

    @property
    def depth(self) -> int:
        return self._depth

    @property
    def is_clickable(self) -> int:
        return self._clickable


class Menu:
    def __init__(self, screen: pygame.Surface) -> None:
        self._font: pygame.font.Font = pygame.font.SysFont("Consolas", 24)
        self._items: List[MenuItem] = []
        self._screen: pygame.Surface = screen
        self._items: List[MenuItem] = self._get_menu_items()

    def _get_menu_items(self) -> List[MenuItem]:
        if len(sys.argv) < 2:
            sys.exit("Config file not provided.")

        root: Path = Path(sys.argv[1])
        items: List[MenuItem] = []

        if not root.is_dir():
            return []

        for f in root.glob("*.txt"):
            items.append(MenuItem(f.name, f, True, 0))

        for folder in sorted(root.iterdir()):
            if folder.is_dir():
                items.append(MenuItem(folder.name, folder, False, 0))
                for f in sorted(folder.glob("*.txt")):
                    items.append(MenuItem(f.name, f, True, 1))
        return items

    def display_menu(self) -> str:
        screen = self._screen
        screen.fill((30, 30, 30))
        mouse_pos: Tuple[int, int] = pygame.mouse.get_pos()
        menu_items = self._items
        scroll_y: int = 0
        line_height: int = 40
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEWHEEL:
                scroll_y += event.y * 20

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for item in menu_items:
                    if item.is_clickable and item.rect.collidepoint(mouse_pos):
                        return item.path

        for i, item in enumerate(menu_items):
            y_pos: int = (i * line_height) + scroll_y
            x_pos: int = 20 + (item.depth * 20)

            item.rect = pygame.Rect(x_pos, y_pos, 300, line_height)

            color = (255, 255, 255) if item.is_clickable else (150, 150, 150)
            if item.is_clickable and item.rect.collidepoint(mouse_pos):
                color = (0, 255, 100)

            text_surf = self._font.render(item.name, True, color)
            screen.blit(text_surf, (x_pos, y_pos))
        pygame.display.flip()
