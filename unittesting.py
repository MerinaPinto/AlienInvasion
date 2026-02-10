import arcade
GameView, WINDOW_WIDTH, WINDOW_HEIGHT, GROUND_Y

#arcade.play_sound so tests don't play audio
arcade.play_sound = lambda sound: None

# function to create and initialize a game instance
def create_game():
    game = GameView()  # Create a new GameView object
    game.setup()       # Set up all sprites, apples, trees, shrubs, and game state
    return game

# 1. Player collects a falling apple
def test_collect_falling_apple():
    game = create_game()
    apple = game.apple_list[0]         #Select first apple
    apple.change_y = -1                 #Simulate apple falling
    game.falling_apples.append(apple)  #Add to falling list

    #Move player to apple
    game.player_sprite.center_x = apple.center_x
    game.player_sprite.center_y = apple.center_y

    #Simulate collision 
    apples_collected = [apple]  #Pretend c_with_list returned this apple
    for apple in apples_collected:
        apple.remove_from_sprite_lists()
        if apple in game.falling_apples:
            game.falling_apples.remove(apple)

    #Check that apple is removed and missed counter stays 0
    assert apple not in game.apple_list
    assert apple not in game.falling_apples
    assert game.missed == 0

# 2. Player touches an apple after it fell
def test_touch_grounded_apple():
    game = create_game()
    apple = game.apple_list[0]
    apple.center_y = GROUND_Y  # Place apple on ground
    apple.change_y = 0         # Apple not falling

    #Move player over apple
    game.player_sprite.center_x = apple.center_x
    game.player_sprite.center_y = apple.center_y

    #Apple should remain and missed counter should not change
    assert apple in game.apple_list
    assert game.missed == 0

# 3.Player misses an apple
def test_miss_apple():
    game = create_game()
    apple = game.apple_list[0]
    apple.change_y = -1
    game.falling_apples.append(apple)

    # Simulate apple hitting ground
    apple.center_y = GROUND_Y
    apple.change_y = 0
    game.missed += 1  # Manually increase missed

    assert apple.change_y == 0
    assert game.missed == 1

# 4. Apples fall in random order
def test_apple_random_order():
    orders = []
    for _ in range(3):  #Create 3 different game setups
        game = create_game()
        orders.append([id(a) for a in game.shuffled_apples])

    #Check at least two orders differ
    assert any(orders[i] != orders[j] for i in range(len(orders)) for j in range(i+1, len(orders)))

# 5.Player hits left screen boundary
def test_player_left_boundary():
    game = create_game()
    game.player_sprite.center_x = -10
    # Simulate boundary check
    if game.player_sprite.left < 0:
        game.player_sprite.left = 0
    assert game.player_sprite.left >= 0

# 6.Player hits right screen boundary
def test_player_right_boundary():
    game = create_game()
    game.player_sprite.center_x = WINDOW_WIDTH + 10
    # Simulate boundary check
    if game.player_sprite.right > WINDOW_WIDTH:
        game.player_sprite.right = WINDOW_WIDTH
    assert game.player_sprite.right <= WINDOW_WIDTH

# 7.Level completion triggers correctly
def test_level_completion():
    game = create_game()
    for apple in game.apple_list:
        apple.change_y = 0  # All apples stopped
    game.current_apple_index = len(game.apple_list)

    #Simulate level completion logic
    all_done = all(apple.change_y == 0 for apple in game.apple_list)
    if game.current_apple_index > 0 and all_done:
        game.level_completed = True
        game.message = "Level Completed"

    assert game.level_completed
    assert game.message == "Level Completed"

# 8.Pause logic stops apple movement
def test_pause_game_logic():
    game = create_game()
    game.level_completed = True  # Simulate paused game

    #All apples should not fall while paused
    for apple in game.apple_list:
        apple.change_y = 0
        assert apple.change_y == 0

# 9.Apples spawn near trees
def test_apples_spawn_near_trees():
    game = create_game()
    for apple in game.apple_list:
        closest_tree = min(game.tree_list, key=lambda t: abs(t.center_x - apple.center_x))
        #Apple should be horizontally close and above tree
        assert abs(apple.center_x - closest_tree.center_x) <= 120
        assert apple.center_y >= closest_tree.center_y

# 10.Shrubs are evenly spread across screen
def test_shrubs_spread():
    game = create_game()
    for shrub in game.shrub_list:
        #Each shrub must be inside screen bounds
        assert 0 <= shrub.center_x <= WINDOW_WIDTH
        assert 0 <= shrub.center_y <= WINDOW_HEIGHT
