import pygame
from pygame.rect import Rect


def correct_wall_collide(rect: Rect) -> Rect:
    test_display = pygame.Surface((500, 500)).get_rect()  # Game window size is constant

    return rect.clamp(test_display)


def correct_player_collide(p1: Rect, p2: Rect):
    if p1.colliderect(p2):
        pass