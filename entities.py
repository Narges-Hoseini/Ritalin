import math
import random
import time
from typing import List

import arcade

import configs


class Jet(arcade.Sprite):
    def __init__(self, character_scaling: float = configs.JET_CHARACTER_SCALING):
        super().__init__(scale=character_scaling)
        self.damage: bool = configs.JET_DAMAGE
        self.moving_state: int = 0
        self.frames: List[arcade.texture.Texture] = []
        self.explode_frames: List[arcade.texture.Texture] = []
        self.explode_sound_track: arcade.Sound = None
        self.sprite_width: float = None
        self.sprite_height: float = None
        self.last_key_press_time: float = None
        self.current_frame: arcade.texture.Texture = None
        self.last_pressed_key: arcade.Key = None
        self.bullet_type: str = "laser_bullet"
        self.scene: arcade.Scene = None
        self.is_dead: bool = False
        self.explode_frame_index: int = None
        self.explode_frame_last_update: float = None
        self.explode_width: float = None
        self.explode_height: float = None
        self.hp: float = configs.JET_HP
        self.game_over: bool = False
        self.last_chicken_damage_time: float = 0

    def set_size(self, sprite_width: float = configs.JET_SPRITE_WIDTH,
                 sprite_height: float = configs.JET_SPRITE_HEIGHT):
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height

    def set_explode_size(self, explode_width: float = configs.EXPLODE_WIDTH,
                         explode_height: float = configs.EXPLODE_HEIGHT):
        self.explode_width = explode_width
        self.explode_height = explode_height

    def load_explode_frames(self, path: str = configs.EXPLODE_ANIMATION_PATH,
                            count_in_row: int = configs.COUNT_EXPLODE_FRAMES_IN_ROW,
                            count_in_column: int = configs.COUNT_EXPLODE_FRAMES_IN_COLUMN):
        for j in range(count_in_column):
            for i in range(count_in_row):
                texture: arcade.texture.Texture = arcade.load_texture(path, x=i * self.explode_width,
                                                                      y=j * self.explode_height,
                                                                      width=self.explode_width,
                                                                      height=self.explode_height
                                                                      )
                self.explode_frames.append(texture)

    def load_frames(self, path: str = configs.JET_ANIMATION_PATH, count: int = configs.COUNT_JET_FRAMES):
        for i in range(count):
            texture: arcade.texture.Texture = arcade.load_texture(path, x=i * self.sprite_width, y=0,
                                                                  width=self.sprite_width, height=self.sprite_height)
            self.frames.append(texture)
        self.current_frame = self.frames[0]
        self.texture = self.current_frame

    def load_explode_sound(self, path: str = configs.EXPLODE_SOUND_TRACK_PATH):
        self.explode_sound_track = arcade.load_sound(path)

    def on_key_press(self, key, modifiers):
        if self.is_dead:
            return
        angle: float = self.angle + 90
        if key == arcade.key.W or key == arcade.key.UP:
            self.change_x = configs.MOVEMENT_SPEED * math.cos(math.radians(angle))
            self.change_y = configs.MOVEMENT_SPEED * math.sin(math.radians(angle))
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.change_x = -configs.MOVEMENT_SPEED * math.cos(math.radians(angle))
            self.change_y = -configs.MOVEMENT_SPEED * math.sin(math.radians(angle))
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.change_x = -configs.MOVEMENT_SPEED
            self.change_y = 0
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.change_x = configs.MOVEMENT_SPEED
            self.change_y = 0
        else:
            return
        self.last_key_press_time = time.time()
        self.last_pressed_key = key

    def on_key_release(self, key: arcade.key, modifiers):
        if self.is_dead:
            return
        if key in [arcade.key.W, arcade.key.S, arcade.key.UP, arcade.key.DOWN, arcade.key.A, arcade.key.D,
                   arcade.key.LEFT, arcade.key.RIGHT]:
            self.last_key_press_time = None
            self.last_pressed_key = None
            self.change_y = 0
            self.change_x = 0

    def on_mouse_motion(self, x, y, dx, dy):
        # Calculate the angle between the mouse position and the jet sprite
        if self.is_dead:
            return
        self.angle = -arcade.get_angle_degrees(self.center_x, self.center_y, x, y)
        angle: float = self.angle + 90
        if self.last_pressed_key:
            key = self.last_pressed_key
            if key == arcade.key.W or key == arcade.key.UP:
                self.change_x = configs.MOVEMENT_SPEED * math.cos(math.radians(angle))
                self.change_y = configs.MOVEMENT_SPEED * math.sin(math.radians(angle))
            elif key == arcade.key.S or key == arcade.key.DOWN:
                self.change_x = -configs.MOVEMENT_SPEED * math.cos(math.radians(angle))
                self.change_y = -configs.MOVEMENT_SPEED * math.sin(math.radians(angle))
            elif key == arcade.key.A or key == arcade.key.LEFT:
                self.change_x = -configs.MOVEMENT_SPEED
                self.change_y = 0
            elif key == arcade.key.D or key == arcade.key.RIGHT:
                self.change_x = configs.MOVEMENT_SPEED
                self.change_y = 0

    def update_animation(self, delta_time: float = 1 / configs.FPS):
        # TODO: refactor this to have animation with high percision
        if self.is_dead:
            if self.explode_frame_index is None:
                self.explode_frame_index = 0
                self.explode_frame_last_update = time.time()
                self.current_frame = self.explode_frames[self.explode_frame_index]
                arcade.play_sound(self.explode_sound_track)
            elif time.time() - self.explode_frame_last_update - configs.EXPLODE_DELAY >= 0:
                if self.explode_frame_index >= configs.COUNT_EXPLODE_FRAMES_IN_COLUMN * configs.COUNT_EXPLODE_FRAMES_IN_ROW - 1:
                    self.game_over = True
                    self.current_frame = self.explode_frames[self.explode_frame_index]
                else:
                    self.explode_frame_index += 1
                    self.explode_frame_last_update = time.time()
                    self.current_frame = self.explode_frames[self.explode_frame_index]

            else:
                self.current_frame = self.explode_frames[self.explode_frame_index]


        else:
            if (self.change_x != 0 or self.change_y != 0) and self.last_key_press_time:
                if time.time() - self.last_key_press_time >= 0.3:
                    self.current_frame = self.frames[2]
                else:
                    self.current_frame = self.frames[1]
            else:
                self.current_frame = self.frames[0]

        self.texture = self.current_frame

    def on_mouse_press(self, x, y, button, modifiers):
        if self.is_dead:
            return
        bullet: Bullet = BULLET_TYPE_MAPPING[self.bullet_type]()
        bullet.center_x = self.center_x
        bullet.center_y = self.center_y
        bullet.angle = self.angle + 90
        self.scene.add_sprite(configs.BULLET_LIST_NAME, bullet)
        bullet.play_sound()

    def check_collision(self):
        if self.is_dead:
            return
        hit_list: List[Egg] = arcade.check_for_collision_with_list(self,
                                                                   self.scene[
                                                                       configs.EGG_LIST_NAME])  # refactor type to Egg list

        if hit_list:
            # self.remove_from_sprite_lists()

            for collision in hit_list:
                self.hp -= collision.damage
                collision.remove_from_sprite_lists()
            if self.hp <= 0:
                self.is_dead = True
                self.change_x = 0
                self.change_y = 0
                return

        if time.time() - self.last_chicken_damage_time < configs.CHICKEN_DAMAGE_COOLDOWN:
            return

        hit_list: List[Chicken] = arcade.check_for_collision_with_list(self,
                                                                       self.scene[
                                                                           configs.CHICKEN_LIST_NAME])  # refactor type to Chivken list

        if hit_list:
            # self.remove_from_sprite_lists()
            for collision in hit_list:
                self.hp -= collision.damage
                collision.hp -= self.damage
                if collision.hp <= 0:
                    collision.remove_from_sprite_lists()

                self.last_chicken_damage_time = time.time()

            if self.hp <= 0:
                self.is_dead = True
                self.change_x = 0
                self.change_y = 0
                return


class Chicken(arcade.Sprite):
    def __init__(self, scene: arcade.Scene, character_scaling: float = configs.CHICKEN_SCALING,
                 path: str = configs.CHICKEN_ASSET_PATH,
                 hp: float = configs.CHICKEN_HP, shooting_cooldown: float = configs.CHICKEN_COOLDOWN):
        self.damage: bool = configs.CHICKEN_DAMAGE
        self.hp: float = hp
        self.shooting_cooldown: float = shooting_cooldown
        self.last_shot_time: float = time.time()
        self.scene: arcade.Scene = scene
        super().__init__(filename=path, scale=character_scaling)

    def check_collision(self):

        hit_list: List[Bullet] = arcade.check_for_collision_with_list(self,
                                                                      self.scene[
                                                                          configs.BULLET_LIST_NAME])  # refactor type to Buller list

        if hit_list:
            # self.remove_from_sprite_lists()

            for collision in hit_list:
                self.hp -= collision.damage
                collision.remove_from_sprite_lists()
            if self.hp <= 0:
                self.remove_from_sprite_lists()
                return

    def on_update(self, delta_time: float = 1 / configs.FPS):
        self.check_collision()
        self.center_x += self.change_x
        self.center_y += self.change_y

        ### check for shooting
        if random.random() <= math.exp(time.time() - self.last_shot_time - self.shooting_cooldown):
            egg: Egg = Egg()
            egg.center_x = self.center_x
            egg.center_y = self.center_y
            self.last_shot_time = time.time()
            self.scene.add_sprite(configs.EGG_LIST_NAME, egg)

        if self.left < 0:
            self.change_x *= -1
        if self.right > configs.SCREEN_WIDTH:
            self.change_x *= -1
        if self.top > configs.SCREEN_HEIGHT:
            self.change_y *= -1
        if self.bottom < 0:
            self.change_y *= -1
        if self.center_y < configs.CHICKEN_MINIMUM_HEIGHT_LIMIT:
            self.change_y *= -1

        super().on_update(delta_time)
        return

class Bullet(arcade.Sprite):
    def __init__(self, damage: float, asset_path: str, character_scaling: float):
        self.damage: float = damage
        super().__init__(filename=asset_path, scale=character_scaling)

    def load_sound_track(self, sound_track_path: str):
        self.sound_track: arcade.Sound = arcade.load_sound(sound_track_path)

    def play_sound(self):
        arcade.play_sound(self.sound_track)


class Egg(Bullet):
    def __init__(self):
        super().__init__(configs.EGG_DAMAGE, configs.EGG_ASSET_PATH, configs.EGG_SCALE)

    def on_update(self, delta_time: float = 1 / configs.FPS):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.change_x = 0
        self.change_y = -configs.EGG_SPEED
        super().on_update(delta_time)
        return

class LaserBullet(Bullet):
    def __init__(self):
        super().__init__(configs.LASER_DAMAGE, configs.LASER_BULLET_ASSET_PATH, configs.LASER_SCALE)
        self.load_sound_track(configs.LASER_BULLET_SOUND_TRACK_PATH)

    def on_update(self, delta_time: float = 1 / configs.FPS):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.change_x = configs.LASER_SPEED * math.cos(math.radians(self.angle))
        self.change_y = configs.LASER_SPEED * math.sin(math.radians(self.angle))
        super().on_update(delta_time)
        return

def create_jet() -> Jet:
    jet: Jet = Jet()  # create new arcade.sprite object
    jet.set_size()  # set some sizes to load frames from a sprite sheet
    jet.load_frames()  # load frames from a sprite sheet
    jet.set_explode_size()
    jet.load_explode_frames()
    jet.load_explode_sound()
    jet.center_x = configs.JET_START_CENTER_X
    jet.center_y = configs.JET_START_CENTER_Y

    return jet


def create_random_chicken(scene: arcade.Scene) -> Chicken:
    chicken = Chicken(scene)
    chicken.center_x = random.uniform(*configs.CHICKEN_START_WIDTH_RANGE)
    chicken.center_y = random.uniform(*configs.CHICKEN_START_HEIGHT_RANGE)

    chicken.change_x = random.uniform(*configs.CHICKEN_SPEED_RANGE)
    chicken.change_y = random.uniform(*configs.CHICKEN_SPEED_RANGE)
    return chicken


def setup_chickens_into_scene(scene: arcade.Scene, list_name: str = configs.CHICKEN_LIST_NAME,
                              init_chickens_count: int = configs.INIT_CHICKENS_COUNT) -> None:
    for _ in range(init_chickens_count):
        chicken: Chicken = create_random_chicken(scene)
        scene.add_sprite(list_name, chicken)


def lag_preventor(scene: arcade.Scene):
    ### some setups to prevent lag
    sample_bullet = LaserBullet()
    sample_bullet.center_x = configs.SCREEN_HEIGHT
    sample_bullet.center_y = configs.SCREEN_HEIGHT
    scene.add_sprite("Bullets", sample_bullet)

    sample_egg = Egg()
    sample_egg.center_x = 0
    sample_egg.center_y = 0
    scene.add_sprite("Eggs", sample_egg)


BULLET_TYPE_MAPPING = {"laser_bullet": LaserBullet}