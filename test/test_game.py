import pytest
import pygame
from main import PrinceCat, Obstacle, GameState

pygame.init()  

# --- PrinceCat Tests ---
@pytest.fixture
def prince_cat():
    return PrinceCat(100, 300)

def test_jump_sets_velocity_and_flag(prince_cat):
    prince_cat.is_jumping = False
    prince_cat.jump()
    assert prince_cat.velocity_y == -15
    assert prince_cat.is_jumping is True

def test_jump_does_nothing_if_already_jumping(prince_cat):
    prince_cat.is_jumping = True
    initial_velocity = prince_cat.velocity_y
    prince_cat.jump()
    # velocity_y should not change because jump ignored
    assert prince_cat.velocity_y == initial_velocity

def test_update_applies_gravity_and_limits(prince_cat):
    prince_cat.rect.y = 290
    prince_cat.velocity_y = 5
    prince_cat.is_jumping = True
    prince_cat.update()
    # velocity_y increased by 1
    assert prince_cat.velocity_y == 6
    # position increased by velocity_y
    assert prince_cat.rect.y == 295

def test_update_resets_jump_when_on_ground(prince_cat):
    prince_cat.rect.y = 310  # below ground level
    prince_cat.velocity_y = 10
    prince_cat.is_jumping = True
    prince_cat.update()
    # Should reset y to ground level
    assert prince_cat.rect.y == 300
    # is_jumping reset
    assert prince_cat.is_jumping is False

# --- Obstacle Tests ---
@pytest.fixture
def obstacle():
    return Obstacle(200)

def test_obstacle_moves_left_and_kills_when_offscreen(obstacle):
    initial_x = obstacle.rect.x
    obstacle.update()
    # Obstacle moves left by 5
    assert obstacle.rect.x == initial_x - 5

    # Move obstacle off screen and verify kill
    obstacle.rect.right = -1
    obstacle.update()
    assert not obstacle.alive()  # Should be killed

# --- GameState Tests ---
def test_score_increments():
    state = GameState()
    initial_score = state.score
    state.update_score()
    assert state.score == initial_score + 1


