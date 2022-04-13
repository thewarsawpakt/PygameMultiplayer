import pygame
from pygame.rect import Rect
from common import WINDOW_SIZE


def correct_wall_collide(rect: Rect) -> Rect:
    test_display = pygame.Surface(WINDOW_SIZE).get_rect()

    return rect.clamp(test_display)


def correct_player_collide(p1: Rect, p2: Rect):
    if p1.colliderect(p2):
        pass