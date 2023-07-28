import arcade
import random

SCREEN_WIDTH = 650
SCREEN_HEIGHT = 550
SCREEN_TITLE = "chicken invaders"

CHARACTER_SCALING = 0.25

PLAYER_MOVEMENT_SPEED = 5

"""class Chicken(arcade.Sprite):
    def on_update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.left < 0 :
            self.change_x *= -1
        if self.right > SCREEN_WIDTH:
            self.change_x *= -1
        if self.bottom < 0:
            self.change_y *= -1
        if self.top > SCREEN_HEIGHT:
            self.change_y *= -1"""



class MyGame(arcade.Window):

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        self.scene = None
        
        self.player_sprite = None
        
        self.physics_engine = None
        
        arcade.set_background_color(arcade.csscolor.BLANCHED_ALMOND)
        
        self.set_mouse_visible(False)

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
        self.chicken_list = arcade.SpriteList()
        """for i in range(15):
            self.chiken_sprite = arcade.Sprite("chicken-removebg-preview.png")
            self.chicken = Chicken() 
            self.chicken.center_x = random.randrange(SCREEN_WIDTH)
            self.chicken.center_y = random.randrange(SCREEN_HEIGHT)
            self.chicken.change_x = random.randrange(-1,3)
            self.chicken.change_y = random.randrange(-1,3)
            self.chicken_list.append(self.chicken)"""
        for i in range(15):
            self.chicken_sprite = arcade.Sprite("G://AP//ap 2023//chicken-removebg-preview (1).png", 0.1)
            self.chicken_sprite.center_x = random.randrange(20, SCREEN_WIDTH - 20)
            self.chicken_sprite.center_y = random.randrange(220, SCREEN_HEIGHT - 20)
            self.chicken_list.append(self.chicken_sprite) 

    
    def on_draw(self):
        arcade.start_render()
        self.clear()
         
        self.scene.draw()
        
        self.chicken_list.draw()
        
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