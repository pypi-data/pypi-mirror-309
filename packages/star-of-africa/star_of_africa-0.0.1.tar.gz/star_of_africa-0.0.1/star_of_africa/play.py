import sys

import pygame

from star_of_africa.game.board_layout import BoardLayout

pygame.init()

res_x, res_y = 560, 756
layout = BoardLayout(res_x, res_y)
layout.initialize_layout()


rectangle = pygame.rect.Rect(176, 134, 17, 17)
rectangle_draging = False
pygame.draw.rect(layout.screen, (255, 0, 0), rectangle)


i = 0
while True:
    for event in pygame.event.get():
        pygame.display.update()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if rectangle.collidepoint(event.pos):
                    rectangle_draging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = rectangle.x - mouse_x
                    offset_y = rectangle.y - mouse_y
