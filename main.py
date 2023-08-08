import arcade

from game import ChickenInvaders


def __main__():
    window = ChickenInvaders()
    window.setup()
    arcade.run()

if __name__ == '__main__':
    __main__()
