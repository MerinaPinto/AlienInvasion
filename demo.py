import arcade
import random

#Establsing the Constants

#Window size and title
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Alien Invasion"

#Player movement speed and scaling
PLAYER_MOVEMENT_SPEED = 5  #How fast the horse moves horizontally/on the x-axis
PLAYER_SCALE = 0.2         #Scale of the horse sprite

#Apple and tree properties
APPLE_SCALE = 0.15         #Scale of apple sprites
TREE_SCALE = 0.8           #Scale of tree sprites
NUM_TREES = 3              #Number of trees to place in the background
APPLES_PER_TREE = 6        #Number of apples per tree
NUM_SHRUBS = 15            #Decorative shrubs scattered across the screen

#Apple dropping timing
INITIAL_DROP_DELAY = 3     #Wait time before first apple begins falling
MAX_INTERVAL = 3.0         
MIN_INTERVAL = 0.2         #Final short interval between apple drops

#Ground level for apples (stops falling)
GROUND_Y = 0


#Start Screen code
class StartView(arcade.View):
    #Class to display the start screen before gameplay begins 

    def __init__(self):
        super().__init__()
        #Load the background image for the start screen
        bg_path = "Start_background.png"
        self.background_list = arcade.SpriteList()  #Use a sprite list for efficientcy
        background = arcade.Sprite(bg_path)
        #Center the background in the window
        background.center_x = WINDOW_WIDTH // 2
        background.center_y = WINDOW_HEIGHT // 2
        #Stretch the image to fill the entire window
        background.width = WINDOW_WIDTH
        background.height = WINDOW_HEIGHT
        self.background_list.append(background)

    def on_show_view(self):
        #Set background color 
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        #Draw the start screen background
        self.clear()
        self.background_list.draw()

    def on_key_press(self, key, modifiers):
        #Start the game when the user presses ENTER
        if key == arcade.key.ENTER:
            game_view = GameView()
            game_view.setup()             #Initialize the game
            self.window.show_view(game_view)  #switch to the main game view


#Main game code
class GameView(arcade.View):
    #Class that contains the main game logic and game elements

    def __init__(self):
        super().__init__()

        #Sprite Lists
        self.shrub_list = arcade.SpriteList(use_spatial_hash=True)   # Background shrubs
        self.player_list = arcade.SpriteList()  # Player sprite (horse)
        self.tree_list = arcade.SpriteList(use_spatial_hash=True)    # Trees that hold apples
        self.apple_list = arcade.SpriteList()   # Apples that fall and can be collected

        #Apple Drop Control
        self.drop_timer = 0
        self.time_elapsed = 0
        self.shuffled_apples = []
        self.current_apple_index = 0
        self.falling_apples = []

        #Score / Missed Counter 
        self.missed = 0
        self.gui_camera = arcade.Camera2D()
        self.score_text = None

        #Level Completion decider
        self.level_completed = False
        self.message = None

        #Player/hourse code
        horse_path = "pngimg.com - horse_PNG321.png"
        self.player_sprite = arcade.Sprite(horse_path, scale=PLAYER_SCALE)
        self.player_sprite.center_x = WINDOW_WIDTH // 2
        self.player_sprite.center_y = 40
        self.player_list.append(self.player_sprite)

        #Physics engine for player movement ( horizontal movement)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, arcade.SpriteList())

        #Sounds/ kierra saying YUMMMM
        self.eat_sound = arcade.load_sound("yum.wav")

        #Shrub Texture background
        self.shrub_texture = "shrub.png"

    def on_show_view(self):
        #Set the background color for gameplay.
        arcade.set_background_color(arcade.csscolor.SKY_BLUE)

    def setup(self):
        #Initialize all sprites, positions, and game state.
        
        #Shrubs 
        self.shrub_list = arcade.SpriteList(use_spatial_hash=True)
        cols = 5
        rows = 3
        x_spacing = WINDOW_WIDTH // (cols + 1)
        y_spacing = (WINDOW_HEIGHT - 150) // (rows + 1)

        shrub_count = 0
        for row in range(rows):
            for col in range(cols):
                if shrub_count >= NUM_SHRUBS:
                    break
                #Create a shrub sprite with random scale for variety
                shrub = arcade.Sprite(self.shrub_texture, scale=random.uniform(0.5, 1.0))
                #position the shrub in a grid with slight random offset to look natural
                shrub.center_x = (col + 1) * x_spacing + random.randint(-20, 20)
                shrub.center_y = (row + 1) * y_spacing + random.randint(-20, 20)
                self.shrub_list.append(shrub)
                shrub_count += 1

        #Trees
        self.tree_list = arcade.SpriteList(use_spatial_hash=True)  #SpriteList to store all tree sprites 
        tree_path = "tree.png"
        spacing = WINDOW_WIDTH // (NUM_TREES + 0.5) #Create a tree sprite with scaling
        for i in range(NUM_TREES):
            tree = arcade.Sprite(tree_path, scale=TREE_SCALE)
            tree.center_x = spacing * (i + 0.75)
            tree.center_y = WINDOW_HEIGHT - 180 if i == 1 else WINDOW_HEIGHT - 200 #middle tree slightly higher
            self.tree_list.append(tree)

        #Apples
        self.apple_list = arcade.SpriteList()
        apple_path = "noFilter.webp" #image used for apples
        for tree in self.tree_list:
            for _ in range(APPLES_PER_TREE):
                apple = arcade.Sprite(apple_path, scale=APPLE_SCALE) #Create scaled apple sprite
                  #randomly position apples near the tree canopy
                apple.center_x = tree.center_x + random.randint(-120, 120)
                apple.center_y = tree.center_y + random.randint(40, 140)
                apple.change_y = 0
                apple.counted = False  #Track if apple already counted as missed
                self.apple_list.append(apple)

        #Shuffle apples to randomize drop order
        self.shuffled_apples = list(self.apple_list)
        random.shuffle(self.shuffled_apples)
        self.current_apple_index = 0
        self.drop_timer = 0
        self.time_elapsed = 0
        self.falling_apples = []

        #Initialize missed counter display
        self.missed = 0
        self.score_text = arcade.Text(
            f"Missed: {self.missed},", 
            x=10, 
            y=5, 
            color=arcade.color.WHITE, 
            font_size=20
        )

        #Reset level completion 
        self.level_completed = False
        self.message = None

    def on_draw(self):
        #Draw all sprites and GUI text on the screen.
        self.clear()
        self.shrub_list.draw()
        self.tree_list.draw()
        self.apple_list.draw()
        self.player_list.draw()

        #Draw GUI elements 
        self.gui_camera.use()
        self.score_text.draw()

        #Message code
        if self.message:
            self.message.draw()

    def on_update(self, delta_time):
        #Update all game elements each frame
        if self.level_completed:
            return

        self.physics_engine.update()
        self.time_elapsed += delta_time

        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        if self.player_sprite.right > WINDOW_WIDTH:
            self.player_sprite.right = WINDOW_WIDTH

        #Apple Drops
        total_apples = len(self.shuffled_apples)
        if total_apples > 1:
            progress = self.current_apple_index / total_apples
            #Gradually decrease the time between drops from MAX_INTERVAL to MIN_INTERVAL
            current_interval = MAX_INTERVAL * (1 - progress) + MIN_INTERVAL * progress
        else:
            current_interval = MAX_INTERVAL

        self.drop_timer += delta_time
       ## Continue dropping apples while conditions are met
        while (self.current_apple_index < total_apples
               and self.drop_timer >= current_interval
               and self.time_elapsed >= INITIAL_DROP_DELAY):
            apple = self.shuffled_apples[self.current_apple_index]
            if apple.change_y == 0:
                #Start the apple falling- later apples fall slightly faster
                apple.change_y = -0.5 - self.current_apple_index * 0.03
                self.falling_apples.append(apple) #Track apples that are currently falling
            self.current_apple_index += 1
            self.drop_timer -= current_interval

        #Move Falling Apples
        for apple in self.falling_apples:
            apple.center_y += apple.change_y
            if apple.center_y <= GROUND_Y:
                apple.change_y = 0
                apple.center_y = GROUND_Y
                #Count the apple as missed only once
                if not apple.counted:
                    self.missed += 1
                    self.score_text.text = f"Missed: {self.missed},"
                    apple.counted = True

        #Player Collects Apple
        apples_collected = arcade.check_for_collision_with_list(self.player_sprite, self.apple_list)
        for apple in apples_collected:
            if apple.change_y != 0:
                apple.remove_from_sprite_lists()
                if apple in self.falling_apples:
                    self.falling_apples.remove(apple)
                arcade.play_sound(self.eat_sound)

        #Check Level Completion
        all_done = all(apple.change_y == 0 for apple in self.apple_list)
        if self.current_apple_index > 0 and all_done and not self.level_completed:
            self.level_completed = True
            text = (f"You Failed! Missed: {self.missed},\nPress ENTER to retry"
                    if self.missed > 5 else
                    f"You Won! Missed: {self.missed},\nPress ENTER to play again")
            self.message = arcade.Text(
                text,
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT // 2,
                color=arcade.color.GREEN,
                font_size=40,
                anchor_x="center",
                anchor_y="center"
            )

    def on_key_press(self, key, modifiers):
        #Handle player movement and restarting the level
        if key in (arcade.key.LEFT, arcade.key.A):
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            self.player_sprite.scale_x = -PLAYER_SCALE
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
            self.player_sprite.scale_x = PLAYER_SCALE

        if key == arcade.key.ENTER and self.level_completed:
            self.setup()

    def on_key_release(self, key, modifiers):
        #Stop horizontal movement when key is released
        if key in (arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D):
            self.player_sprite.change_x = 0


# Main Function
def main():
    #Initialize the window and start the game loop
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
