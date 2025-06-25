from main import GameState

def test_score_updates():
    state = GameState()
    state.update_score()
    assert state.score == 1

def test_game_starts_running():
    state = GameState()
    assert state.is_running is True
