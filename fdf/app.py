"""Окно программы. Единственный модуль, который импортирует pygame."""

import pygame

from fdf.model import Map
from fdf.projection import Camera

BACKGROUND = (17, 24, 39)
LINE_COLOR = (220, 225, 235)


class App:
    def __init__(
        self, fdf_map: Map, title: str = "FdF", size: tuple[int, int] = (1024, 768)
    ) -> None:
        self.map = fdf_map
        self.title = title
        self.size = size
        self.camera = Camera()

    def run(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        pygame.display.set_caption(f"FdF — {self.title}")
        clock = pygame.time.Clock()

        width, height = screen.get_size()
        self.camera.fit(self.map, width, height)
        redraw = True
        running = True
        while running:
            new_size = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    new_size = (event.w, event.h)
                elif event.type == pygame.WINDOWEXPOSED:
                    redraw = True

            # при перетаскивании окна событий много — пересчитываем один раз
            if new_size is not None:
                self.camera.fit(self.map, new_size[0], new_size[1])
                redraw = True

            # большие карты рисуются долго, поэтому только при изменениях
            if redraw and running:
                self.draw(screen)
                pygame.display.flip()
                redraw = False
            clock.tick(30)

        pygame.quit()

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND)
        projected = {(p.x, p.y): self.camera.project(p) for p in self.map}
        for a, b in self.map.edges():
            pygame.draw.line(screen, LINE_COLOR, projected[(a.x, a.y)], projected[(b.x, b.y)])
        if len(self.map) == 1:  # рёбер нет — рисуем саму точку
            pygame.draw.circle(screen, LINE_COLOR, projected[(0, 0)], 3)
