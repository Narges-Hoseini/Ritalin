import time

import arcade

import configs
import entities


class ChickenInvaders(arcade.Window):

    def __init__(self):
        super().__init__(configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT, configs.SCREEN_TITLE)

        self.scene: arcade.Scene = None
        self.background: arcade.Texture = None
        self.player_sprite: entities.Jet = None
        self.win_time: float = None
        self.physics_engine = None

    def check_game_over(self):
        return self.player_sprite.game_over

    def win_check(self):
        if len(self.scene.get_sprite_list(configs.CHICKEN_LIST_NAME)) == 0:
            if not self.win_time:
                self.win_time = time.time()
                return False
            elif time.time() - self.win_time - configs.WAIT_AFTER_WIN >= 0:
                return True
            else:
                pass

        return False

    def setup(self):
        self.scene = arcade.Scene()

        ### loading background
        self.background = arcade.load_texture(configs.BACKGROUND_2)

        ### Set Some walls
        self.scene.add_sprite_list(configs.WALL_LIST_NAME)

        ### Loading Jet
        self.scene.add_sprite_list(configs.PLAYER_LIST_NAME)  # Create a new list in the scene
        self.player_sprite: entities.Jet = entities.create_jet()
        self.scene.add_sprite(configs.PLAYER_LIST_NAME, self.player_sprite)
        self.player_sprite.scene = self.scene

        self.on_key_press = self.player_sprite.on_key_press
        self.on_key_release = self.player_sprite.on_key_release
        self.on_mouse_motion = self.player_sprite.on_mouse_motion
        self.on_mouse_press = self.player_sprite.on_mouse_press

        ### Setup Chickens
        self.scene.add_sprite_list(configs.CHICKEN_LIST_NAME)
        entities.setup_chickens_into_scene(self.scene)

        ### Setup Bullets
        self.scene.add_sprite_list(configs.BULLET_LIST_NAME)

        ### Setup Eggs
        self.scene.add_sprite_list(configs.EGG_LIST_NAME)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene.get_sprite_list(configs.WALL_LIST_NAME)
        )

        ### previnting lags
        entities.lag_preventor(self.scene)

    def on_draw(self):
        if self.check_game_over():

            arcade.draw_text("Game Over", configs.SCREEN_WIDTH // 2, configs.SCREEN_HEIGHT // 2,
                             arcade.color.RED, font_size=50, anchor_x="center")

        elif self.win_check():
            arcade.draw_text("You Win!", configs.SCREEN_WIDTH // 2, configs.SCREEN_HEIGHT // 2,
                             arcade.color.GREEN, font_size=50, anchor_x="center")
        else:
            self.clear()
            arcade.draw_lrwh_rectangle_textured(0, 0, configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT, self.background)
            self.scene.draw()

    def on_update(self, delta_time: float = 1 / configs.FPS):
        if not self.check_game_over() and not self.win_check():
            self.player_sprite.check_collision()
            self.scene.on_update(delta_time)
            self.physics_engine.update()
            self.scene.update_animation(delta_time)

            super().on_update(delta_time)
            return