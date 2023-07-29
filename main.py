import arcade
import random
import entity
import configs





class MyGame(arcade.Window):

    def __init__(self):

        super().__init__(configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT, configs.SCREEN_TITLE)

        self.scene = None

        self.player_sprite = None

        self.physics_engine = None

        arcade.set_background_color(arcade.csscolor.BLANCHED_ALMOND)

        # self.set_mouse_visible(False)

    def setup(self):

        self.scene = arcade.Scene()

        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        self.player_sprite = arcade.Sprite("./assets/jet.png", configs.JET_CHARACTER_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100
        self.scene.add_sprite("Player", self.player_sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene.get_sprite_list("Walls")
        )
        self.chicken_list = arcade.SpriteList()

        for i in range(15):
            self.chicken = entity.Chicken("./assets/chicken.png", 0.1)
            self.chicken.center_x = random.randrange(20, configs.SCREEN_WIDTH - 20)
            self.chicken.center_y = random.randrange(220, configs.SCREEN_HEIGHT - 20)
            self.chicken.change_x = random.randrange(-1, 3)
            self.chicken.change_y = random.randrange(-1, 3)
            self.chicken_list.append(self.chicken)

    def on_draw(self):

        self.clear()

        self.scene.draw()

        self.chicken_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        if x > configs.SCREEN_WIDTH:
            self.player_sprite.center_x = configs.SCREEN_WIDTH
        elif x < 0:
            self.player_sprite.center_x = 0
        else:
            self.player_sprite.center_x = x

        if y > configs.SCREEN_HEIGHT:  # will be removed in endless level
            self.player_sprite.center_y = configs.SCREEN_HEIGHT
        elif y < 0:
            self.player_sprite.center_y = 0
        else:
            self.player_sprite.center_y = y

    def on_update(self, delta_time: float):

        self.physics_engine.update()
        self.chicken_list.on_update()

        return super().on_update(delta_time)


def main():
    window = MyGame()
    window.setup()
    arcade.run()


main()
