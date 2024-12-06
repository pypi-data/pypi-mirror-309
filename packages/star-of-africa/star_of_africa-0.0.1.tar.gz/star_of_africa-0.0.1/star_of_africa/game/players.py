import pygame
from pygame.sprite import Sprite

from star_of_africa.game.cities import ALL_CITIES


class Player(Sprite):

    COLOR = (0, 0, 255, 255)

    def __init__(self, starting_city="Cairo", *groups) -> None:
        super().__init__(*groups)
        self.set_initial_position(starting_city)
        self.surface = self._create_surface(visible=True)

    def set_initial_position(self, starting_city):
        starting_city = ALL_CITIES[starting_city]
        self.x = starting_city.x
        self.y = starting_city.y

    def _create_surface(self, visible: bool) -> pygame.Surface:
        surface = pygame.Surface((50, 50), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        color = self.COLOR
        pygame.draw.rect(surface, color, (self.x - 25, self.y - 25, 50, 50))
        return surface

    def display(self, screen, resolution) -> None:
        x = self.x * resolution[0]
        y = self.y * resolution[1]
        screen.blit(self.surface, (x, y))
