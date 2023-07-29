import configs
import arcade

class Chicken(arcade.Sprite):
    def on_update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.change_x *= -1
        if self.right > configs.SCREEN_WIDTH:
            self.change_x *= -1
        if self.top > configs.SCREEN_HEIGHT:
            self.change_y *= -1
        if self.bottom < 0:
            self.change_y *= -1

        if self.center_y < 220:
            self.change_y *= -1

        return super().on_update(delta_time)
