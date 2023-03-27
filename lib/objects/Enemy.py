from .Playable import Playable


class Enemy(Playable):
    """
    Generic Enemy Class. Will need simple weapon and AI class
    """
    def __init__(self, name: str = "", pos: tuple = (0, 0), size: tuple = (0, 0),
                 img: str = "resources/images/notfound.png"):
        super().__init__(name, pos, size, img)
