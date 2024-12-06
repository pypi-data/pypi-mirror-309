""" """

import pygame
from pygame.sprite import Group, Sprite


class City(Sprite):
    """ """

    COLOR = (255, 0, 0, 255)

    def __init__(
        self,
        x: float,
        y: float,
        radius: float = 15,
        width: int = 2,
        visible: bool = True,
        groups: Group | list[Group] = None,
    ):
        if groups is None:
            groups = []
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.radius = radius
        self.width = width
        self.surface = self._create_surface(visible)

    def _create_surface(self, visible: bool) -> pygame.Surface:
        surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        color = self.COLOR if visible else (0, 0, 0, 0)
        pygame.draw.circle(
            surface, color, (self.radius, self.radius), self.radius, self.width
        )
        return surface

    def display(self, screen: pygame.Surface, resolution) -> None:
        x = self.x * resolution[0] - self.radius
        y = self.y * resolution[1] - self.radius
        screen.blit(self.surface, (x, y))


ALL_CITIES = {
    "Congo": City(0.43, 0.63),
    "Kandjama": City(0.449, 0.531),
    "Cape Town": City(0.493, 0.87),
    "Dragon Mountain": City(0.655, 0.786),
    "Victoria Falls": City(0.60, 0.72),
    "Walsfish Bay": City(0.445, 0.755),
    "Cape St Marie": City(0.807, 0.803),
    "Tamatave": City(0.887, 0.717),
    "Mozambique": City(0.773, 0.685),
    "Daressalam": City(0.764, 0.602),
    "Ocomba": City(0.58, 0.608),
    "Lake Victoria": City(0.709, 0.533),
    "Bahr El Ghasal": City(0.643, 0.48),
    "Addis Ababa": City(0.78, 0.467),
    "Cape Guardafui": City(0.92, 0.448),
    "Suakin": City(0.752, 0.37),
    "Egypt": City(0.634, 0.332),
    "Darfur": City(0.593, 0.423),
    "Ain Galaka": City(0.471, 0.374),
    "Slave Coast": City(0.354, 0.484),
    "Gold Coast": City(0.252, 0.476),
    "St Helena": City(0.195, 0.675),
    "Sierra Leone": City(0.120, 0.446),
    "Cape Verde": City(0.07, 0.374),
    "Timbuktu": City(0.271, 0.365),
    "Sahara": City(0.359, 0.29),
    "Tripoli": City(0.477, 0.239),
    "Tunis": City(0.434, 0.188),
    "Morocco": City(0.209, 0.228),
    "Canary Islands": City(0.109, 0.218),
    "Tangier": City(0.259, 0.149, radius=35),
    "Cairo": City(0.662, 0.22, radius=35),
}

CITIES = Group(ALL_CITIES.values())
STARTING_CITY = Group(ALL_CITIES["Tangier"], ALL_CITIES["Cairo"])
