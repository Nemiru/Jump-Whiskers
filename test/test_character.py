# tests/test_character.py
import pygame
import pytest
from main import PrinceCat

@pytest.fixture
def cat():
    pygame.init()  # Needed for Surface creation
    return PrinceCat(100, 300)

def test_jump_sets_velocity_and_flag(cat):
    cat.jump()
    assert cat.velocity_y == -15
    assert cat.is_jumping is True

def test_gravity_applies(cat):
    cat.velocity_y = 0
    cat.update()
    assert cat.velocity_y > 0

def test_lands_on_ground(cat):
    cat.rect.y = 250
    cat.velocity_y = 20
    for _ in range(10):
        cat.update()
    assert cat.rect.y == 300
    assert cat.is_jumping is False
