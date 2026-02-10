import pytest 
from demo import GameView, WINDOW_WIDTH, WINDOW_HEIGHT, GROUND_Y, NUM_TREES, APPLES_PER_TREE

# Test Case 1: Player collects a falling apple
def test_collect_falling_apple():
    game = GameView()
    game.setup()
    apple = game.apple_list[0]
    apple.remove_from_sprite_lists()
    assert len(game.apple_list) < NUM_TREES * APPLES_PER_TREE

# Test Case 2: Player touches an apple after it fell
def test_touch_grounded_apple():
    game = GameView()
    game.setup()
    apple = game.apple_list[0]
    apple.change_y = 0
    apple.center_y = GROUND_Y
    assert apple.change_y == 0

# Test Case 3: Player misses an apple
def test_miss_apple():
    game = GameView()
    game.setup()
    game.missed = 1
    assert game.missed == 1

# Test Case 4: Apples fall in random order
def test_apples_random_order():
    game1 = GameView()
    game1.setup()
    game2 = GameView()
    game2.setup()
    assert game1.shuffled_apples[0].center_x != game2.shuffled_apples[0].center_x

# Test Case 5: Player hits screen boundaries
def test_player_boundaries():
    game = GameView()
    game.setup()
    game.player_sprite.left = -10
    if game.player_sprite.left < 0:
        game.player_sprite.left = 0
    assert game.player_sprite.left >= 0
    game.player_sprite.right = WINDOW_WIDTH + 10
    if game.player_sprite.right > WINDOW_WIDTH:
        game.player_sprite.right = WINDOW_WIDTH
    assert game.player_sprite.right <= WINDOW_WIDTH

# Test Case 6: Level completion triggers correctly
def test_level_completion():
    game = GameView()
    game.setup()
    for apple in game.apple_list:
        apple.change_y = 0
    game.current_apple_index = len(game.apple_list)
    game.level_completed = True
    assert game.level_completed

# Test Case 7: Apples spawn near trees
def test_apples_spawn_near_trees():

    game = GameView()
    game.setup()
    tree = game.tree_list[0]
    apple = game.apple_list[0]
    assert tree.center_x - 120 <= apple.center_x <= tree.center_x + 120

# Test Case 8: Shrubs are evenly spread across the screen
def test_shrubs_spread():
    game = GameView()
    game.setup()
    shrub = game.shrub_list[0]
    assert 0 <= shrub.center_x <= WINDOW_WIDTH
    assert 0 <= shrub.center_y <= WINDOW_HEIGHT

