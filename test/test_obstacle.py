# tests/test_obstacle.py
import pygame
from main import Obstacle

def test_obstacle_moves_left():
    pygame.init()
    obstacle = Obstacle(800)
    initial_x = obstacle.rect.x
    obstacle.update()
    assert obstacle.rect.x < initial_x
