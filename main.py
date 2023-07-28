import arcade

SCREEN_WIDTH = 650
SCREEN_HEIGHT = 550
SCREEN_TITLE = "chicken invaders"

CHARACTER_SCALING = 0.25

PLAYER_MOVEMENT_SPEED = 5


class MyGame(arcade.Window):

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        self.scene = None
        
        self.player_sprite = None
        
        self.physics_engine = None
        
        arcade.set_background_color(arcade.csscolor.BLANCHED_ALMOND)

    def setup(self):
        
        self.scene = arcade.Scene()
        
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        
        image_source = "G://AP//ap 2023//pngaaa.com-5463282.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100
        self.scene.add_sprite("Player", self.player_sprite)
        
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene.get_sprite_list("Walls")
        ) 

    
    def on_draw(self):
       
        self.clear()
         
        self.scene.draw()
        
    def on_key_press(self, key, modifiers):
       
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
     
    def on_update(self, delta_time):
    
        self.physics_engine.update()   


def main():
    
    window = MyGame()
    window.setup()
    arcade.run()



main()