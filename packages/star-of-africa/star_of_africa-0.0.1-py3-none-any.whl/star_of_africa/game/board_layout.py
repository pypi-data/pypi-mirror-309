from pathlib import Path

import pygame

from star_of_africa.game.cities import CITIES
from star_of_africa.game.players import Player
from star_of_africa.game.roads import AIRPORTS, BOATS, ROADS


class BoardLayout:
    def __init__(self, res_x: int, res_y: int) -> None:
        self.res_x = res_x
        self.res_y = res_y
        self.screen = pygame.display.set_mode((res_x, res_y))

    def initialize_layout(self) -> None:
        """ """
        self.display_background("images/background.png")
        self.display_cities()
        self.display_paths(BOATS)
        self.display_paths(ROADS)
        self.display_paths(AIRPORTS)
        self.display_players()

    def display_background(self, path: str) -> None:
        """ """
        abs_path = Path(__package__.split(".")[0]) / path
        background = pygame.image.load(abs_path)
        background = pygame.transform.scale(background, (self.res_x, self.res_y))
        self.screen.blit(background, (0, 0))

    def display_cities(self) -> None:
        """ """
        for city in CITIES:
            city.display(self.screen, (self.res_x, self.res_y))

    def display_paths(self, group) -> None:
        """ """
        for path in group:
            path.display(self.screen, (self.res_x, self.res_y))

    def display_players(self) -> None:
        """ """
        for player in [Player("Cairo")]:
            player.display(self.screen, (self.res_x, self.res_y))
