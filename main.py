import arcade

SCREEN_WIDTH = 650
SCREEN_HEIGHT = 550
SCREEN_TITLE = "chicken invaders"


class MyGame(arcade.Window):

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.BLANCHED_ALMOND)

    def setup(self):
    
        pass

    def on_draw(self):
       
        self.clear()
        


def main():
    
    window = MyGame()
    window.setup()
    arcade.run()



main()
