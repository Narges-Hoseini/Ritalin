import arcade
import random
import entity
import configs


class MyGame(arcade.Window):

    def __init__(self):

        super().__init__(configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT, configs.SCREEN_TITLE)

        self.scene: arcade.Scene = None

        self.player_sprite = None

        self.physics_engine = None

        arcade.set_background_color(arcade.csscolor.BLANCHED_ALMOND)

        # self.set_mouse_visible(False)

    def setup(self):

        self.scene = arcade.Scene()

        self.scene.add_sprite_list("Player")

        self.player_sprite = arcade.Sprite(configs.JET_ASSET_PATH, configs.JET_CHARACTER_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100
        self.scene.add_sprite("Player", self.player_sprite)

        self.scene.add_sprite_list("Chickens")

        for i in range(15):
            chicken = entity.Chicken(configs.CHICKEN_ASSET_PATH, 0.1)
            chicken.center_x = random.randrange(20, configs.SCREEN_WIDTH - 20)
            chicken.center_y = random.randrange(220, configs.SCREEN_HEIGHT - 20)


            chicken.change_x = random.uniform(-1, 3)
            chicken.change_y = random.uniform(-1, 3)

            self.scene.add_sprite("Chickens", chicken)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene.get_sprite_list("Chickens")
        )

    def on_draw(self):

        self.clear()

        self.scene.draw()

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = configs.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -configs.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -configs.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = configs.PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    """def on_mouse_motion(self, x, y, dx, dy):

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
            self.player_sprite.center_y = y"""

    def on_update(self, delta_time: float):

        self.scene.on_update(delta_time)
        self.physics_engine.update()

        return super().on_update(delta_time)


def main():
    window = MyGame()
    window.setup()
    arcade.run()


main()
